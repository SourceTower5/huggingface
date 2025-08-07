from smolagents import CodeAgent, DuckDuckGoSearchTool, FinalAnswerTool, LiteLLMModel, Tool, tool, VisitWebpageTool

import warnings
import statistics

# Ignore httpx Deprecation
warnings.filterwarnings("ignore", category=DeprecationWarning, module="httpx._models")

# Ignore Pydantic serialization warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic.main")

# Using Mistral Small (free tier)
devalstral_small="mistral/devstral-small-latest"
mistral_small="mistral/mistral-small-latest"

model = LiteLLMModel(model_id=mistral_small)
max_steps = 10

@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion: The type of occasion for the party.
    """
    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."

@tool
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest-rated catering service in Gotham City.
    
    Args:
        query: A search term for finding catering services.
    """
    def median_key(d):
        median_val = statistics.median(d.values())
        for k, v in d.items():
            if v == median_val:
                return k
        # If no exact match (e.g., median is float from even count), return closest
        return min(d.items(), key=lambda item: abs(item[1] - median_val))[0]

    # Example list of catering services and their ratings
    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }
    
    # Find the highest rated catering service (simulating search query filtering)
    if "highest".lower() in query:
        service = max(services, key=services.get)
    elif "lowest".lower() in query:
        service = min(services, key=services.get) 
    else:
        service = median_key(services)
    
    return service

class SuperheroPartyThemeTool(Tool):
    name = "superhero_party_theme_generator"
    description = """
    This tool suggests creative superhero-themed party ideas based on a category.
    It returns a unique party theme idea."""
    
    inputs = {
        "category": {
            "type": "string",
            "description": "The type of superhero party (e.g., 'classic heroes', 'villain masquerade', 'futuristic Gotham').",
        }
    }
    
    output_type = "string"

    def forward(self, category: str):
        themes = {
            "classic heroes": "Justice League Gala: Guests come dressed as their favorite DC heroes with themed cocktails like 'The Kryptonite Punch'.",
            "villain masquerade": "Gotham Rogues' Ball: A mysterious masquerade where guests dress as classic Batman villains.",
            "futuristic Gotham": "Neo-Gotham Night: A cyberpunk-style party inspired by Batman Beyond, with neon decorations and futuristic gadgets."
        }
        
        return themes.get(category.lower(), "Themed party idea not found. Try 'classic heroes', 'villain masquerade', or 'futuristic Gotham'.")


# Alfred, the butler, preparing the menu for the party
agent = CodeAgent(
    tools=[
        DuckDuckGoSearchTool(), 
        VisitWebpageTool(),
        suggest_menu,
        catering_service_tool,
        SuperheroPartyThemeTool(),
	    FinalAnswerTool()
    ], 
    model=model,
    max_steps=10,
    verbosity_level=2
)

music_command = "Give me the best playlist for a party at the Wayne's mansion. The party idea is a 'villain masquerade' theme"
catering_command = "Use catering_service_tool to give me highest catering service in Gotham city"
menu_command = "Suggest a menu for a superhero occasion"

agent.run(menu_command)