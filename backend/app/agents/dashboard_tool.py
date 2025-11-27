from langchain.tools import StructuredTool
from langchain.pydantic_v1 import BaseModel, Field
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class VisualizationInput(BaseModel):
    """Input schema for data visualization"""
    data: List[Dict[str, Any]] = Field(
        default=[],
        description="List of dictionaries containing the data to visualize"
    )
    chart_type: str = Field(
        default="auto",
        description="Type of chart: 'auto', 'bar', 'line', 'pie', or 'scatter'"
    )


def detect_chart_type(data: List[Dict[str, Any]]) -> str:
    """
    Auto-detect the best chart type based on data structure
    
    Args:
        data: List of dictionaries containing the data
        
    Returns:
        Chart type: 'bar', 'line', 'pie', 'scatter'
    """
    if not data or len(data) == 0:
        return "bar"
    
    df = pd.DataFrame(data)
    
    # Check number of columns
    num_cols = len(df.columns)
    
    # Check if there's a date column
    date_cols = df.select_dtypes(include=['datetime64']).columns
    
    # Check numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    # Decision logic
    if len(date_cols) > 0 and len(numeric_cols) > 0:
        return "line"  # Time series data
    elif num_cols == 2 and len(numeric_cols) == 1:
        # One categorical, one numeric - good for pie or bar
        if len(df) <= 10:
            return "pie"
        else:
            return "bar"
    elif len(numeric_cols) >= 2:
        return "scatter"  # Multiple numeric columns
    else:
        return "bar"  # Default


def create_plotly_chart(data: List[Dict[str, Any]], chart_type: str = "auto") -> go.Figure:
    """
    Create a Plotly chart from data
    
    Args:
        data: List of dictionaries containing the data
        chart_type: Type of chart to create
        
    Returns:
        Plotly Figure object
    """
    if not data:
        # Return empty figure
        fig = go.Figure()
        fig.add_annotation(
            text="No data available to visualize",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    df = pd.DataFrame(data)
    
    # Auto-detect chart type if needed
    if chart_type == "auto":
        chart_type = detect_chart_type(data)
    
    # Get column names
    columns = df.columns.tolist()
    
    try:
        if chart_type == "bar":
            # Bar chart
            x_col = columns[0]
            y_col = columns[1] if len(columns) > 1 else columns[0]
            
            fig = px.bar(
                df, 
                x=x_col, 
                y=y_col,
                title=f"{y_col.title()} by {x_col.title()}",
                template="plotly_dark",
                color_discrete_sequence=['#8b5cf6']  # Purple color
            )
            
            # Update bar styling
            fig.update_traces(
                marker=dict(
                    line=dict(width=0),
                    opacity=0.9
                ),
                hovertemplate='<b>%{x}</b><br>%{y:,.2f}<extra></extra>'
            )
            
        elif chart_type == "line":
            # Line chart
            x_col = columns[0]
            y_col = columns[1] if len(columns) > 1 else columns[0]
            
            fig = px.line(
                df,
                x=x_col,
                y=y_col,
                title=f"{y_col.title()} over {x_col.title()}",
                template="plotly_dark",
                markers=True,
                color_discrete_sequence=['#8b5cf6']
            )
            
            # Update line styling
            fig.update_traces(
                line=dict(width=3),
                marker=dict(size=8),
                hovertemplate='<b>%{x}</b><br>%{y:,.2f}<extra></extra>'
            )
            
        elif chart_type == "pie":
            # Pie chart
            names_col = columns[0]
            values_col = columns[1] if len(columns) > 1 else columns[0]
            
            fig = px.pie(
                df,
                names=names_col,
                values=values_col,
                title=f"Distribution of {values_col.title()}",
                template="plotly_dark",
                color_discrete_sequence=px.colors.sequential.Purples_r
            )
            
            # Update pie styling
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>%{value:,.2f}<br>%{percent}<extra></extra>'
            )
            
        elif chart_type == "scatter":
            # Scatter plot
            x_col = columns[0]
            y_col = columns[1] if len(columns) > 1 else columns[0]
            
            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                title=f"{y_col.title()} vs {x_col.title()}",
                template="plotly_dark",
                color_discrete_sequence=['#8b5cf6']
            )
            
            # Update scatter styling
            fig.update_traces(
                marker=dict(size=12, opacity=0.8),
                hovertemplate='<b>%{x}</b><br>%{y:,.2f}<extra></extra>'
            )
            
        else:
            # Default to bar chart
            fig = px.bar(df, template="plotly_white")
        
        # Update layout for better appearance
        fig.update_layout(
            height=500,
            margin=dict(l=60, r=40, t=80, b=60),
            font=dict(size=14, family='Inter, system-ui, sans-serif'),
            title=dict(
                font=dict(size=18, color='#fff'),
                x=0.5,
                xanchor='center'
            ),
            hovermode='closest',
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.8)",
                font_size=13,
                font_family="Inter, system-ui, sans-serif"
            )
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating chart: {e}")
        # Return error figure
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error creating visualization: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig


def generate_visualization(data: List[Dict[str, Any]], chart_type: str = "auto") -> str:
    """
    Generate interactive chart from data
    
    Args:
        data: List of dictionaries containing the data to visualize
        chart_type: Type of chart ('auto', 'bar', 'line', 'pie', 'scatter')
        
    Returns:
        JSON string with chart configuration
    """
    try:
        logger.info(f"Dashboard Tool received {len(data)} data points, chart_type: {chart_type}")
        
        if not data:
            return json.dumps({
                "success": False,
                "error": "No data provided for visualization",
                "chart": None
            })
        
        # Create chart
        fig = create_plotly_chart(data, chart_type)
        
        # Convert to JSON
        chart_json = fig.to_json()
        
        response = {
            "success": True,
            "chart": json.loads(chart_json),
            "chart_type": chart_type if chart_type != "auto" else detect_chart_type(data),
            "tool": "dashboard_tool"
        }
        
        logger.info(f"Dashboard Tool created {response['chart_type']} chart")
        
        return json.dumps(response)
        
    except Exception as e:
        logger.error(f"Dashboard Tool error: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "chart": None
        })


def create_dashboard_tool() -> StructuredTool:
    """
    Create dashboard tool for data visualization
    Receives data from SQL agent and generates interactive charts
    """
    
    return StructuredTool.from_function(
        func=generate_visualization,
        name="data_visualizer",
        description="""
        Use this tool to create interactive visualizations from data.
        This tool takes structured data (usually from SQL queries) and generates
        appropriate charts (bar, line, pie, scatter).
        
        Use this when:
        - User asks to visualize data
        - User wants to see a chart or graph
        - Data would be better understood visually
        - User says "show me", "visualize", "chart", "graph", "plot"
        
        The tool will automatically select the best chart type if "auto" is specified.
        """,
        args_schema=VisualizationInput
    )
