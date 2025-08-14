from smolagents import (
    CodeAgent,
    InferenceClientModel,
    DuckDuckGoSearchTool,
    VisitWebpageTool,
)
from smolagents import LiteLLMModel
from smolagents import TransformersModel

# Free Mistral models available via LiteLLM
# mistral/mistral-7b-instruct - free via API
# mistral/mistral-7b-instruct-v0.2 - free via API
# mistral/mistral-medium - free tier available
# mistral/mistral-large - free tier available

devstral_small = "mistral/devstral-small-latest"
small_model = "mistral/mistral-small-latest"
large_model = "mistral/mistral-large-latest"

# Using Mistral Large 2411
mistral_model = LiteLLMModel(model_id=small_model)

# Alternative models (require higher tier):
# mistral_small = LiteLLMModel(model_id="mistral/devstral-small-2507")
# mistral_medium = LiteLLMModel(model_id="mistral/mistral-medium")

model = mistral_model

# visit webpage is needed for the agent to see the contents
# search tools just returns links
duck_tool = DuckDuckGoSearchTool()
visit_webpage_tool = VisitWebpageTool()

agent = CodeAgent(
    tools=[duck_tool, visit_webpage_tool],
    model=model,
)

# sum_command = "Calculate the sum of numbers from 1 to 10"
# result = agent.run(sum_command)
# print(result)

weather_command = "Tokyo weather"
result = agent.run(weather_command)
print(result)
