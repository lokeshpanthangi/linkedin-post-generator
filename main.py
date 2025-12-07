import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Literal
from graph import app as workflow_app
from langgraph.types import Command




class StartRequest(BaseModel):
    user_input: str
    generator : str
    evaluators: List[str] = ["linkedin_expert_evaluation", "genai_engineer_evaluation"]

class FeedbackRequest(BaseModel):
    thread_id: str
    action: Literal["approve", "reject"]
    reason: Optional[str] = None




api = FastAPI(title="LinkedIn Post Generator Agent")

# Add CORS middleware
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



@api.get("/health")
async def health_check():
    return {"status": "ok"}


@api.post("/start_generation")
async def start_generation(request: StartRequest):

    """
    Starts the graph. Runs until it hits the 'human_interupt_confirmation' node and pauses.
    Returns the 'thread_id' which you MUST save to resume later.
    """

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    initial_payload = {
        "user_input": request.user_input,
        "evaluators": request.evaluators,
        "generator": request.generator,
        "generated_post": None,
        "evaluations": {},
        "human_interrupt_confirmed": False,
        "human_interrupt_reason": "No reason provided." 
    }
    final_state = await workflow_app.ainvoke(initial_payload, config=config)
    return {
        "message": "Graph started and paused for feedback.",
        "thread_id": thread_id,
        "current_post": final_state.get("generated_post"),
        "evaluations": final_state.get("evaluations"),
        "next_step": "Call /submit_feedback to approve or reject."
    }


@api.post("/submit_feedback")
async def submit_feedback(request: FeedbackRequest):

    """
    Resumes the graph using the thread_id.
    - If action="approve": Graph finishes.
    - If action="reject": Graph regenerates and pauses again.
    """

    config = {"configurable": {"thread_id": request.thread_id}}
    if request.action == "approve":
        resume_value = True
    else:
        resume_value = request.reason if request.reason else "No specific reason provided."
    try:
        result_state = await workflow_app.ainvoke(Command(resume=resume_value), config=config)  
        status = "finished" if request.action == "approve" else "paused_for_review"
        return {
            "status": status,
            "thread_id": request.thread_id,
            "current_post": result_state.get("generated_post"),
            "evaluations": result_state.get("evaluations", {}),
            "human_feedback_log": result_state.get("human_interrupt_reason")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))