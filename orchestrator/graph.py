import asyncio
from typing import TypedDict, Annotated, List
import operator
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from generator.nodes import Niche, i_generate_post, generate_post
from generator.models import openai
from evals.nodes import linkedin_expert_evaluation, devops_engineer_evaluation, genai_engineer_evaluation, backend_engineer_evaluation, hiring_manager_evaluation
from langgraph.checkpoint.memory import MemorySaver

class PostState(TypedDict):
    input_content: str
    niche: Niche
    generated_post: str
    evaluations: Annotated[List[str], operator.add]
    final_post: str

async def generate_node(state: PostState) -> dict:
    """Generate initial post from input content + niche"""
    post_input = i_generate_post(
        content=state["input_content"], 
        niche=state["niche"]
    )
    generated = await generate_post(post_input)
    return {"generated_post": generated}

async def evaluators_node(state: PostState) -> dict:
    """Run all 5 evaluators in parallel on generated post"""
    post = state["generated_post"]
    
    eval_tasks = [
        linkedin_expert_evaluation(post),
        devops_engineer_evaluation(post),
        genai_engineer_evaluation(post),
        backend_engineer_evaluation(post),
        hiring_manager_evaluation(post)
    ]
    
    evaluations = await asyncio.gather(*eval_tasks)
    return {"evaluations": evaluations}

async def synthesizer_node(state: PostState) -> dict:
    """Combine all evaluations into final polished LinkedIn post"""
    post = state["generated_post"]
    feedback = "\n\n".join(state["evaluations"])
    
    synth_prompt = ChatPromptTemplate.from_template("""
    Original post: {post}
    
    Expert feedback:
    {feedback}
    
    Polish this into a final LinkedIn post incorporating the best feedback.
    Keep it engaging, professional, and under 2000 characters.
    """)
    
    chain = synth_prompt | openai
    final_post = await chain.ainvoke({
        "post": post,
        "feedback": feedback
    })
    
    return {"final_post": final_post.content}

def router(state: PostState) -> str:
    """Simple routing: generate → evaluators → synthesizer → END"""
    if not state.get("generated_post"):
        return "generate"
    elif not state.get("evaluations"):
        return "evaluators"
    else:
        return "synthesizer"

async def build_orchestrator():
    workflow = StateGraph(PostState)
    
    workflow.add_node("generate", generate_node)
    workflow.add_node("evaluators", evaluators_node) 
    workflow.add_node("synthesizer", synthesizer_node)
    
    workflow.add_edge(START, "generate")
    workflow.add_conditional_edges("generate", router, {"generate": "generate", "evaluators": "evaluators"})
    workflow.add_edge("evaluators", "synthesizer")
    workflow.add_edge("synthesizer", END)
    
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    return app

async def run_orchestrator(content: str, niche: Niche, config=None):
    app = await build_orchestrator()
    
    inputs: PostState = {
        "input_content": content,
        "niche": niche,
        "generated_post": "",
        "evaluations": [],
        "final_post": ""
    }
    
    result = await app.ainvoke(inputs, config)
    return result["final_post"]

# final_post = await run_orchestrator("Latest trends in React 19", Niche.FULL_STACK_DEV)