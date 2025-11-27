from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.agents.sql_agent_tool import create_sql_agent_tool
from app.agents.rag_tool import create_rag_tool
from app.agents.dashboard_tool import create_dashboard_tool
from app.agents.sql_viz_tool import create_sql_viz_tool
from app.config import get_settings
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)
settings = get_settings()


class ManagerAgent:
    """Manager Agent that orchestrates SQL, RAG, and Dashboard tools"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0.7,
            openai_api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            streaming=True
        )
        
        self.tools = [
            create_sql_agent_tool(),
            create_rag_tool(),
            create_sql_viz_tool()
        ]
        
        self.prompt = self._create_prompt()
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        self.memories: Dict[str, ConversationBufferMemory] = {}
        logger.info("Manager Agent initialized")
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """Create agent prompt"""
        system_message = """You are an AI assistant with access to:
1. sql_database_query: Query sales data (returns text answers only)
2. document_search: Search uploaded documents
3. query_and_visualize: Query sales data AND create visualizations

**When to use each tool:**
- Use sql_database_query for simple data questions without visualization
  Examples: "What are total sales?", "How many transactions?", "List top 5 products"
  
- Use query_and_visualize when user wants charts, graphs, or visualizations
  Examples: "Visualize sales by branch", "Show me a chart of revenue", "Plot sales over time"
  Keywords: visualize, show, chart, graph, plot, display
  
- Use document_search for questions about uploaded documents

Always provide clear, helpful responses."""
        
        return ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
    
    def _get_memory(self, session_id: str) -> ConversationBufferMemory:
        """Get or create memory for session"""
        if session_id not in self.memories:
            self.memories[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        return self.memories[session_id]
    
    def process_message(self, message: str, session_id: str) -> Dict[str, Any]:
        """Process user message"""
        try:
            memory = self._get_memory(session_id)
            
            executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                memory=memory,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5,
                return_intermediate_steps=True
            )
            
            result = executor.invoke({"input": message})
            
            # Extract chart config, data, and sources from intermediate steps
            chart_config = None
            chart_data = None
            tool_used = None
            sources = None
            
            for step in result.get("intermediate_steps", []):
                if len(step) >= 2:
                    action, observation = step[0], step[1]
                    tool_name = action.tool if hasattr(action, 'tool') else None
                    
                    # Check if this is a visualization tool
                    if tool_name in ['query_and_visualize', 'data_visualizer']:
                        tool_used = tool_name
                        try:
                            tool_output = json.loads(observation)
                            if tool_output.get("chart_config"):
                                chart_config = tool_output.get("chart_config")
                                chart_data = tool_output.get("data", [])
                                logger.info("Extracted chart config and data from tool output")
                        except json.JSONDecodeError:
                            logger.warning("Could not parse tool output as JSON")
                    
                    # Check if this is a RAG/document search tool
                    if tool_name == 'document_search':
                        tool_used = tool_name
                        try:
                            tool_output = json.loads(observation)
                            if tool_output.get("sources"):
                                sources = tool_output.get("sources", [])
                                logger.info(f"Extracted {len(sources)} sources from RAG tool")
                        except json.JSONDecodeError:
                            logger.warning("Could not parse RAG tool output as JSON")
            
            # Clean up the message - remove embedded source references like [^filename^]
            import re
            clean_message = re.sub(r'\[\^[^\]]+\^\]', '', result["output"]).strip()
            
            response = {
                "message": clean_message,
                "session_id": session_id,
                "success": True,
                "tool_used": tool_used,
                "chart_config": chart_config,
                "chart_data": chart_data,
                "sources": sources
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Manager Agent error: {e}")
            return {
                "message": f"Error: {str(e)}",
                "session_id": session_id,
                "success": False
            }
