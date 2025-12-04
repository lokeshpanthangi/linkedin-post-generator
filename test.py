from evals.prompts import hiring_manager_perspective
from config import model




# ----------------------------------------

response = model.invoke(
    hiring_manager_perspective.format(post="I have 10 years of experience in software development and have led multiple successful projects.")
)

print(response.content)