from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from . import prompt
import os
from dotenv import load_dotenv
load_dotenv()

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

market_sentiment_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='market_sentiment_agent',
    description='An agent that provides insights on the cryptocurrency market.',
    instruction="""
    You are a helpful financial agent with access to market data through Alpha Vantage MCP Server.
    When retrieving sentiment data, examine the Alpha Vantage MCP Server function definitions directly rather than using the SEARCH endpoint.

    **You are only allow to get the news sentiment data.**
    """,
    tools=[
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=f"https://mcp.alphavantage.co/mcp?categories=alpha_intelligence&apikey={ALPHAVANTAGE_API_KEY}"),
                tool_filter=["NEWS_SENTIMENT"] )
    ]
)

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='chief_financial_analyst_coordinator',
    description='A Agent Orchestrator who coordinates with other agents to provide insights on the cryptocurrency market.',
    instruction=prompt.CHIEF_FINANCIAL_ANALYST_PROMPT,
    tools=[AgentTool(agent=market_sentiment_agent)]
)
