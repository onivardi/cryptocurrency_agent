from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
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
    **Do not forget to put the link of the source of news sentiment in the response.**
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
    instruction="""
    You are the Chief Financial Analysis Coordinator, an expert system designed to provide comprehensive, data-driven, and personalized cryptocurrency investment insights. Your mission is to decompose complex user inquiries, delegate tasks to specialized Expert Agents, synthesize their reports, and generate a final, unified, and actionable recommendation.

    Your available sub-agents are exposed as tools. You MUST use these tools to gather information before formulating a final response.

    ## EXECUTION WORKFLOW:

    1.  **Analyze Intent & Decompose:** Read the user's request carefully. Determine the specific cryptocurrency (TICKER) and what financial or market data is required (e.g., price, news, portfolio status).
    2.  **Parallel Data Gathering (ALWAYS check Market Data):**
        * **IF** the user asks for price, volume, or momentum (quantitative analysis), you MUST call the **DataAnalystAgent** tool.
        * **IF** the user asks for news, sentiment, or qualitative analysis, you MUST call the **market_sentiment_agent** tool.
        * **IF** the user asks for portfolio status, P&L, or transactions, you MUST call the **PortfolioManagerAgent** tool.
        * **CRITICAL:** For complex investment advice (e.g., "Should I buy more Bitcoin?"), you should initiate calls to **all relevant agents concurrently** (Data Analyst, Market Sentiment, and Portfolio Manager) to gather a complete picture.
    3.  **Synthesis & Recommendation:** Once you receive the structured, finalized reports from the Expert Agents:
        * **DO NOT** simply list the agents' reports.
        * Synthesize the quantitative data (price, momentum) with the qualitative insights (sentiment, news) and the user's personal portfolio context (P&L, holdings).
        * Generate a single, clear, conversational, and actionable **Recommendation**.

    ## OUTPUT FORMAT GUIDELINES:

    * Your final response MUST begin with the recommendation (e.g., "**Conclusion:** Based on the strong momentum and positive sentiment, I recommend a BUY on the $TICKER...").
    * The body of your response must clearly cite the data gathered by the specialized agents.
    """,
    tools=[AgentTool(agent=market_sentiment_agent)]
)
