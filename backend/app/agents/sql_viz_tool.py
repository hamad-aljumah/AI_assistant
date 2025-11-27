from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.tools import StructuredTool
from langchain.pydantic_v1 import BaseModel, Field
from sqlalchemy import create_engine, text
from app.config import get_settings
from app.agents.dashboard_tool import detect_chart_type
import pandas as pd
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)
settings = get_settings()


class SQLVizInput(BaseModel):
    """Input schema for SQL visualization"""
    query: str = Field(
        description="Natural language question about sales data to query and visualize"
    )
    chart_type: str = Field(
        default="auto",
        description="Type of chart: 'auto', 'bar', 'line', 'pie', or 'scatter'"
    )


def query_and_visualize(query: str, chart_type: str = "auto") -> str:
    """
    Query the database and create a visualization in one step
    
    Args:
        query: Natural language question about sales data
        chart_type: Type of chart to create
        
    Returns:
        JSON string with answer, data, and chart
    """
    try:
        logger.info(f"SQL+Viz Tool received query: {query}")
        
        # Create database connection
        engine = create_engine(settings.database_url)
        
        # Create LLM to convert natural language to SQL
        llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0,
            openai_api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
        
        # Create SQL database wrapper
        db = SQLDatabase(engine, include_tables=["sales"])
        
        # Get table info
        table_info = db.get_table_info()
        
        # Generate SQL query using LLM
        sql_prompt = f"""Given the following database schema:
{table_info}

Write a SQL query to answer this question: {query}

Return ONLY the SQL query, nothing else. The query should return data suitable for visualization.
For aggregations, use clear column aliases."""
        
        response = llm.invoke(sql_prompt)
        sql_query = response.content.strip()
        
        # Clean up the SQL query
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        
        logger.info(f"Generated SQL: {sql_query}")
        
        # Execute the query
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            columns = list(result.keys())
            
            # Convert to list of dicts with proper type handling
            data = []
            for row in rows:
                row_dict = {}
                for col, val in zip(columns, row):
                    # Convert Decimal to float for JSON serialization
                    if hasattr(val, '__float__'):
                        row_dict[col] = float(val)
                    elif hasattr(val, '__str__') and not isinstance(val, str):
                        row_dict[col] = str(val)
                    else:
                        row_dict[col] = val
                data.append(row_dict)
        
        logger.info(f"Query returned {len(data)} rows")
        
        if not data:
            return json.dumps({
                "success": False,
                "answer": "No data found for your query.",
                "data": [],
                "chart": None
            })
        
        # Detect chart type if auto
        final_chart_type = chart_type if chart_type != "auto" else detect_chart_type(data)
        
        # Determine axes from data
        columns = list(data[0].keys()) if data else []
        x_axis = columns[0] if len(columns) > 0 else "x"
        y_axis = columns[1] if len(columns) > 1 else columns[0] if len(columns) > 0 else "y"
        
        # Create chart configuration for frontend
        chart_config = {
            "type": final_chart_type,
            "x_axis": x_axis,
            "y_axis": y_axis,
            "title": f"{y_axis.replace('_', ' ').title()} by {x_axis.replace('_', ' ').title()}"
        }
        
        # Generate natural language answer
        answer_prompt = f"""Based on this data: {json.dumps(data[:5])}...
        
Answer the question: {query}

Provide a clear, concise answer with key insights.
DO NOT include any images, charts, base64 data, or markdown image syntax in your response.
The visualization is handled separately by the frontend."""
        
        answer_response = llm.invoke(answer_prompt)
        answer = answer_response.content
        
        response = {
            "success": True,
            "answer": answer,
            "data": data,
            "chart_config": chart_config,
            "tool": "sql_viz_tool"
        }
        
        logger.info(f"SQL+Viz Tool completed successfully")
        
        return json.dumps(response)
        
    except Exception as e:
        logger.error(f"SQL+Viz Tool error: {e}", exc_info=True)
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Full traceback: {error_details}")
        return json.dumps({
            "success": False,
            "answer": f"I encountered an error while processing your request: {str(e)}",
            "data": [],
            "chart": None,
            "error": str(e)
        })


def create_sql_viz_tool() -> StructuredTool:
    """Create combined SQL query and visualization tool"""
    
    return StructuredTool.from_function(
        func=query_and_visualize,
        name="query_and_visualize",
        description="""
        Use this tool to query sales data AND create visualizations in one step.
        This tool will:
        1. Convert your natural language question to SQL
        2. Execute the query against the sales database
        3. Create an appropriate visualization
        4. Provide a natural language answer
        
        Use this when the user wants to see visualized sales data.
        
        Examples:
        - "Visualize sales by branch"
        - "Show me a chart of top products"
        - "Plot revenue over time"
        """,
        args_schema=SQLVizInput
    )
