from evals.prompts import linkedin_expert_perspective, devops_engineer_perspective, genai_engineer_perspective, backend_engineer_perspective, hiring_manager_perspective
from config import model




# ----------------------------------------

async def linkedin_expert_evaluation(post: str):
    response = model.invoke(
        linkedin_expert_perspective.format(post=post)
    )
    return response.content


async def devops_engineer_evaluation(post: str):
    response = model.invoke(
        devops_engineer_perspective.format(post=post)
    )
    return response.content


async def genai_engineer_evaluation(post: str):
    response = model.invoke(
        genai_engineer_perspective.format(post=post)
    )
    return response.content


async def backend_engineer_evaluation(post: str):
    response = model.invoke(
        backend_engineer_perspective.format(post=post)
    )
    return response.content


async def hiring_manager_evaluation(post: str):
    response = model.invoke(
        hiring_manager_perspective.format(post=post)
    )
    return response.content