# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.code_executors.agent_engine_sandbox_code_executor import (
    AgentEngineSandboxCodeExecutor,
)
from google.adk.models import Gemini
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from app.financial_tools import calculate_total_occupancy_cost
from app.geocoding_tools import lookup_neighborhood_location
from app.image_tools import generate_property_image
from app.properties_db import (
    add_property_listing,
    get_property_details,
    schedule_tour,
    search_properties,
)


MODEL = "gemini-3.8-flash"


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


SANDBOX_RESOURCE_NAME = (
    "projects/705176769612/locations/us-east1/reasoningEngines/1137349121422655488"
    "/sandboxEnvironments/2631131325267968000"
)


# WRITE: after each turn, send the session to Memory Bank for extraction.
async def generate_memories_callback(callback_context: CallbackContext):
    try:
        await callback_context.add_session_to_memory()
    except ValueError:
        # No-op if memory service is not configured (e.g. in standalone tests)
        pass
    return None


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        client_kwargs={
            "location": "global",
            "vertexai": True,
            "project": "qwiklabs-gcp-04-6db14bebe7b8",
        },
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are UrbanNest, an intelligent real estate and apartment finding assistant. "
        "You help apartment hunters discover, compare, and schedule tours for verified housing listings. "
        "You specifically remember the user's stated preferences, budget limits (rent and total monthly occupancy costs), "
        "pet details (dog/cat, breed, weight, pet fee constraints), target neighborhoods, and must-have amenities "
        "(in-unit laundry, parking, balcony, elevator) across conversations and use them to personalize your answers. "
        "Use your tools to search available properties by neighborhood, price, bedrooms, or pet policies, "
        "fetch detailed listing specs, look up real geographic coordinates and neighborhood details on OpenStreetMap, "
        "calculate total monthly costs and income affordability, generate visual staging or exterior concept images "
        "for properties, add new listings, and schedule in-person tours. "
        "You also have a secure Python sandbox code executor to compute exact financial calculations, compound interest, "
        "or data analysis when needed."
    ),
    code_executor=AgentEngineSandboxCodeExecutor(
        sandbox_resource_name=SANDBOX_RESOURCE_NAME,
    ),
    tools=[
        PreloadMemoryTool(),
        search_properties,
        get_property_details,
        add_property_listing,
        schedule_tour,
        calculate_total_occupancy_cost,
        lookup_neighborhood_location,
        generate_property_image,
        get_weather,
        get_current_time,
    ],
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
