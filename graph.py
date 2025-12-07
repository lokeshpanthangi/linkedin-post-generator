from state import State
from evals.nodes import linkedin_expert_evaluation, devops_engineer_evaluation, genai_engineer_evaluation, backend_engineer_evaluation, hiring_manager_evaluation
from langgraph.graph import StateGraph, START, END
from generator.nodes import generate_post
from langgraph.prebuilt import interrupt
import asyncio





def human_interupt_confirmation(state: State) -> bool:
    """Check if human interruption confirmed"""
    return state.get("human_interrupt_confirmed", False)



def human_interupt_reason(state: State) -> str:
    """Get human interruption reason"""
    return state.get("human_interrupt_reason", "No reason provided.")





async def evaluation_node(state: State) -> State:
    """Decide which evaluator to use next based on state"""
    evaluators = state.get("evaluators", [])
    evaluations = state.get("evaluations", {})
    temp = []
    # call the function in the evaluators and save the result in the evaluations dict
    for i in range(len(evaluators)):
        temp.append()
        if evaluators[i] == "linkedin_expert_evaluation":
            temp.append(linkedin_expert_evaluation(state["generated_post"]))
        if evaluators[i] == "devops_engineer_evaluation":
            temp.append(devops_engineer_evaluation(state["generated_post"]))
        if evaluators[i] == "genai_engineer_evaluation":
            temp.append(genai_engineer_evaluation(state["generated_post"]))
        if evaluators[i] == "backend_engineer_evaluation":
            temp.append(backend_engineer_evaluation(state["generated_post"]))
        if evaluators[i] == "hiring_manager_evaluation":
            temp.append(hiring_manager_evaluation(state["generated_post"]))
    
    evaluations = await asyncio.gather(*temp)
    # Map evaluator names to their results
    eval = {}
    for i in range(len(temp)):
        eval[temp[i]] = evaluations[i]
    state["evaluations"] = eval
    return state




# Define the graph structure
graph = StateGraph(State)



# Start node: Interrupt to get user input
graph.add_node("human_bool_interrupt", human_interupt_confirmation)
graph.add_node("human_interrupt_reason", human_interupt_reason)
graph.add_node("evaluation_node", evaluation_node)
graph.add_node("generate", generate_post)




### Orchestrator NODE ###


def orchestrator_node(state: State):
    """Orchestrator node to manage the workflow"""
    if state["generated_post"] is None:
        return "generate"
    else:
        if state["evaluations"] is None:
            return "evaluaton_node"
        else:
            if state["human_bool_interrupt"] == True:
                return END
            else:
                return "human_interrupt_reason"
            
                
                


graph.add_node("orchestrator", orchestrator_node)


# Define edges

graph.add_edge(START, "orchestrator")
graph.add_conditional_edges("orchestrator", orchestrator_node,{
    "generate": "generate",
    "evaluaton_node": "evaluation_node",
    "human_bool_interrupt": "human_bool_interrupt",
    "human_interrupt_reason": "human_interrupt_reason"
    })
graph.add_edge("generate", "orchestrator")
graph.add_edge("evaluation_node", "orchestrator")
graph.add_edge("human_bool_interrupt", "orchestrator")
graph.add_edge("human_interrupt_reason", "generate")


app = graph.compile()