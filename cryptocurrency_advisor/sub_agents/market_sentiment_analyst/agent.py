"""
This is the market sentiment analyst agent that provides insights on the cryptocurrency market.
"""

import os
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from . import prompt

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

market_sentiment_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='market_sentiment_agent',
    description='An agent that provides insights on the cryptocurrency market.',
    instruction=prompt.MARKET_SENTIMENT_PROMPT,
    tools=[
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=f"https://mcp.alphavantage.co/mcp?categories=alpha_intelligence&apikey={ALPHAVANTAGE_API_KEY}"),
                tool_filter=["NEWS_SENTIMENT"] )
    ]
)