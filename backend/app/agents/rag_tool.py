from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import Tool
from langchain.docstore.document import Document as LangChainDocument
from app.config import get_settings
import os
import json
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class RAGService:
    """Service for managing RAG operations"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0,
            openai_api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
        self.vector_store_path = os.path.join(settings.vector_store_dir, "faiss_index")
        self.vector_store = None
        self._load_vector_store()
    
    def _load_vector_store(self):
        """Load existing vector store or create empty one"""
        try:
            if os.path.exists(self.vector_store_path):
                self.vector_store = FAISS.load_local(
                    self.vector_store_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("Loaded existing FAISS vector store")
            else:
                logger.info("No existing vector store found")
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            self.vector_store = None
    
    def add_documents(self, texts: list[str], metadatas: list[dict]):
        """Add documents to vector store"""
        try:
            # Create LangChain documents
            documents = [
                LangChainDocument(page_content=text, metadata=metadata)
                for text, metadata in zip(texts, metadatas)
            ]
            
            if self.vector_store is None:
                # Create new vector store
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
            else:
                # Add to existing vector store
                self.vector_store.add_documents(documents)
            
            # Save vector store
            os.makedirs(os.path.dirname(self.vector_store_path), exist_ok=True)
            self.vector_store.save_local(self.vector_store_path)
            
            logger.info(f"Added {len(documents)} documents to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False
    
    def query(self, question: str, k: int = 4) -> dict:
        """Query the vector store"""
        try:
            if self.vector_store is None:
                return {
                    "answer": "No documents have been uploaded yet. Please upload documents first.",
                    "sources": [],
                    "success": False
                }
            
            # Create retrieval QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(
                    search_kwargs={"k": k}
                ),
                return_source_documents=True
            )
            
            # Run query with instruction to not cite sources (they're shown separately)
            modified_query = f"{question}\n\nIMPORTANT: Answer the question directly without mentioning or citing the source document names, filenames, or where the information comes from. Do not say 'according to', 'sourced from', or similar phrases."
            result = qa_chain.invoke({"query": modified_query})
            
            # Extract sources with deduplication
            sources = []
            seen_sources = set()  # Track unique source+chunk combinations
            
            for doc in result.get("source_documents", []):
                # Create unique key from source file and chunk number
                source_file = doc.metadata.get("source", "unknown")
                chunk_num = doc.metadata.get("chunk", 0)
                source_key = f"{source_file}_{chunk_num}"
                
                # Skip if we've already seen this source+chunk
                if source_key in seen_sources:
                    continue
                seen_sources.add(source_key)
                
                sources.append({
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                })
            
            return {
                "answer": result["result"],
                "sources": sources,
                "success": True,
                "tool": "rag_tool"
            }
            
        except Exception as e:
            logger.error(f"Error querying vector store: {e}")
            return {
                "answer": f"Error querying documents: {str(e)}",
                "sources": [],
                "success": False,
                "error": str(e)
            }
    
    def delete_all(self):
        """Delete all documents from vector store"""
        try:
            if os.path.exists(self.vector_store_path):
                import shutil
                shutil.rmtree(os.path.dirname(self.vector_store_path))
            self.vector_store = None
            logger.info("Deleted all documents from vector store")
            return True
        except Exception as e:
            logger.error(f"Error deleting vector store: {e}")
            return False


# Global RAG service instance
rag_service = RAGService()


def create_rag_tool() -> Tool:
    """Create RAG tool for document Q&A"""
    
    def run_rag_query(query: str) -> str:
        """
        Answer questions based on uploaded documents
        
        Args:
            query: Question about the uploaded documents
            
        Returns:
            JSON string with answer and source citations
        """
        try:
            logger.info(f"RAG Tool received query: {query}")
            
            result = rag_service.query(query)
            
            logger.info(f"RAG Tool response: {result['answer'][:200]}...")
            
            return json.dumps(result)
            
        except Exception as e:
            logger.error(f"RAG Tool error: {str(e)}")
            error_response = {
                "answer": f"Error processing your question: {str(e)}",
                "sources": [],
                "success": False,
                "error": str(e)
            }
            return json.dumps(error_response)
    
    return Tool(
        name="document_search",
        func=run_rag_query,
        description="""
        Use this tool to answer questions about uploaded documents.
        This tool searches through the document knowledge base and provides
        answers with source citations.
        
        Use this when:
        - User asks about content in uploaded documents
        - User wants information from their knowledge base
        - User references "documents", "files", or "uploaded content"
        
        Input should be a clear question about the document content.
        """
    )
