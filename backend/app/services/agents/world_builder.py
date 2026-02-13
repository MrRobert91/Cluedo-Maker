from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.core.config import settings

class WorldBuilderAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY, temperature=0.7)
        
    async def generate(self, theme: str, tone: str) -> dict:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a master game designer for Live Action Cluedo games. You output STRICT JSON."),
            ("user", "Create a setting for a Cluedo game.\nTheme: {theme}\nTone: {tone}\n\nOutput fields:\n- intro: A compelling 2 paragraph story introduction.\n- factions: List of 2 groups with 'name', 'description', 'objectives'.\n- roles: List of 6 generic visual archetypes suitable for this setting.")
        ])
        
        chain = prompt | self.llm | JsonOutputParser()
        
        try:
            return chain.invoke({"theme": theme, "tone": tone})
        except Exception as e:
            print(f"LLM Error: {e}")
            # Fallback for dev without keys
            return {
                "intro": "A dark and stormy night...",
                "factions": [{"name": "Global Corp", "description": "Evil corp", "objectives": "Profit"}, {"name": "Resistance", "description": "Rebels", "objectives": "Freedom"}],
                "roles": ["The CEO", "The Hacker", "The Guard", "The Scientist"]
            }
