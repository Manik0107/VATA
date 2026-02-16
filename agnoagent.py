from agno.team import Team
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.utils.log import logger
import os

document_extractor = Agent(
    id="document-extractor-agent",
    name="Document Extractor Agent", 
    role="Extract structured information from documents such as PDFs and PowerPoint presentations",
    tools=[DuckDuckGoTools()]
)

weather_agent = Agent(
    id="weather-agent",
    name="Weather Agent", 
    role="Get weather information and forecasts",
    tools=[DuckDuckGoTools()]
)