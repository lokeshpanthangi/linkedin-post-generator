from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from dataclasses import dataclass
from enum import Enum
from generator.models import openai
from generator.prompts import GENERATE_POST_PROMPT, GENERATE_NEW_POST_WITH_FEEDBACK_PROMPT

class Niche(Enum):
    AI_ML = 1
    FULL_STACK_DEV = 2
    BLOCKCHAIN = 3

NICHE_LABELS = {
    Niche.AI_ML: "AI/ML",
    Niche.FULL_STACK_DEV: "Full Stack Development",
    Niche.BLOCKCHAIN: "Blockchain"
}

@dataclass
class i_generate_post:
    content: str
    niche: Niche

async def generate_post(state: Dict[str, Any]):
    """Generate post using user_input and generator fields."""
    try:
        user_input = state.get("user_input", "")
        generator = state.get("generator", "")
        
        if not user_input:
            return {"generated_post": "", "user_feedback": "Error: No user input provided"}
        
        niche_map = {
            "ai": Niche.AI_ML,
            "ml": Niche.AI_ML,
            "devops": Niche.FULL_STACK_DEV,
            "backend": Niche.FULL_STACK_DEV,
            "fullstack": Niche.FULL_STACK_DEV,
            "blockchain": Niche.BLOCKCHAIN
        }

        niche = niche_map.get(generator.lower(), Niche.FULL_STACK_DEV)
        
        system_msg = SystemMessage(content=GENERATE_POST_PROMPT)
        human_msg = HumanMessage(
            content=f"Niche: {NICHE_LABELS[niche]}, Content: {user_input}"
        )

        messages = [system_msg, human_msg]
        full_post = await openai.ainvoke(messages)
        
        # async for chunk in openai.astream(messages):
        #     if chunk.content:
        #         full_post += chunk.content
        
        return {"generated_post": full_post}
        
    except Exception as e:
        return {
            "generated_post": "",
            "user_feedback": f"Generation failed: {str(e)}"
        }



async def generate_new_post_with_feedback(state: Dict[str, Any]):
    """Generate post using user_input and generator fields."""
    try:
        user_input = state.get("user_input", "")
        generator = state.get("generator", "")
        user_feedback = state.get("user_feedback", "")
        
        if not user_input:
            return {"generated_post": "", "user_feedback": "Error: No user input provided"}
        
        niche_map = {
            "ai": Niche.AI_ML,
            "ml": Niche.AI_ML,
            "devops": Niche.FULL_STACK_DEV,
            "backend": Niche.FULL_STACK_DEV,
            "fullstack": Niche.FULL_STACK_DEV,
            "blockchain": Niche.BLOCKCHAIN
        }
        
        niche = niche_map.get(generator.lower(), Niche.FULL_STACK_DEV)
        
        system_msg = SystemMessage(content=GENERATE_NEW_POST_WITH_FEEDBACK_PROMPT)
        human_msg = HumanMessage(
            content=f"Niche: {NICHE_LABELS[niche]}, Content: {user_input}, Feedback: {user_feedback}"
        )

        messages = [system_msg, human_msg]
        full_post = await openai.ainvoke(messages)
        
        # async for chunk in openai.astream(messages):
        #     if chunk.content:
        #         full_post += chunk.content
        
        return {"generated_post": full_post}
        
    except Exception as e:
        return {
            "generated_post": "",
            "user_feedback": f"Generation failed: {str(e)}"
        }