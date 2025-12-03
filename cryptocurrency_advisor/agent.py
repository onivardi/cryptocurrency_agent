from cryptocurrency_advisor.sub_agents.market_sentiment_analyst.agent import market_sentiment_agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents.llm_agent import LlmAgent
from . import prompt

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='chief_financial_analyst_coordinator',
    description='A Agent Orchestrator who coordinates with other agents to provide insights on the cryptocurrency market.',
    instruction=prompt.CHIEF_FINANCIAL_ANALYST_PROMPT,
    tools=[AgentTool(agent=market_sentiment_agent)]
)
