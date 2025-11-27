from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType
from langchain.tools import Tool
from sqlalchemy import create_engine
from app.config import get_settings
import json
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


def create_sql_agent_tool() -> Tool:
    """
    Create SQL agent tool for natural language to SQL queries
    Uses the latest LangChain SQL agent implementation
    """
    
    # Create database connection
    engine = create_engine(settings.database_url)
    db = SQLDatabase(engine, include_tables=["sales"])
    
    # Create ChatOpenAI instance
    llm = ChatOpenAI(
        model=settings.openai_model,
        temperature=0,
        openai_api_key=settings.openai_api_key,
        base_url=settings.openai_base_url
    )
    
    # Create SQL agent
    sql_agent = create_sql_agent(
        llm=llm,
        db=db,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )
    
    def run_sql_query(query: str) -> str:
        """
        Execute natural language query against sales database
        
        Args:
            query: Natural language question about sales data
            
        Returns:
            JSON string with query results and metadata
        """
        try:
            logger.info(f"SQL Agent received query: {query}")
            
            # Run the agent
            result = sql_agent.invoke({"input": query})
            
            # Extract the output
            output = result.get("output", "")
            
            # Try to parse if it's structured data
            response = {
                "answer": output,
                "tool": "sql_agent",
                "success": True
            }
            
            logger.info(f"SQL Agent response: {output[:200]}...")
            
            return json.dumps(response)
            
        except Exception as e:
            logger.error(f"SQL Agent error: {str(e)}")
            error_response = {
                "answer": f"I encountered an error while querying the database: {str(e)}",
                "tool": "sql_agent",
                "success": False,
                "error": str(e)
            }
            return json.dumps(error_response)
    
    # Create and return the tool
    return Tool(
        name="sql_database_query",
        func=run_sql_query,
        description="""
        Use this tool to answer questions about sales data. 
        The database contains a 'sales' table with columns: 
        - date (DATE): Transaction date
        - branch (VARCHAR): Store branch (A, B, C)
        - customer_type (VARCHAR): Member or Normal
        - gender (VARCHAR): Male or Female
        - product_line (VARCHAR): Product category
        - unit_price (DECIMAL): Price per unit
        - quantity (INTEGER): Number of units sold
        - payment (VARCHAR): Payment method (Cash, Credit card, Ewallet)
        - rating (DECIMAL): Customer rating (1-10)
        - total (DECIMAL): Total amount (unit_price * quantity)
        
        Examples of questions you can answer:
        - "What are the total sales by branch?"
        - "Show me the top 5 product lines by revenue"
        - "What's the average rating for each payment method?"
        - "Compare sales between male and female customers"
        
        Input should be a natural language question about the sales data.
        """
    )
