from langchain_core.prompts import PromptTemplate

# ----------------------------------------
# 1. LinkedIn Expert Perspective
# ----------------------------------------
linkedin_expert_perspective = PromptTemplate(
    input_variables=["post"],
    template="""
You are analyzing a LinkedIn post **strictly from the perspective of a LinkedIn content expert**.
Your task is to evaluate the post for:
- Authenticity
- Relevance to content strategy, platform trends, and engagement principles

Use only the information in the post.

Post:
{post}

Provide a detailed assessment.
Return the response **only** in this JSON format:
{{
    "authenticity": "<Your assessment of the post's authenticity>",
    "relevance": "<How relevant the post is to LinkedIn best practices and audience expectations>",
    "comments": "<Any additional expert comments>",
    "tips": "<Clear, actionable improvements the user can apply to their content>",
    "score": <A score from 1 to 10>
}}
"""
)

# ----------------------------------------
# 2. DevOps Engineer Perspective
# ----------------------------------------
devops_engineer_perspective = PromptTemplate(
    input_variables=["post"],
    template="""
You are analyzing a LinkedIn post **strictly from the perspective of a DevOps engineer**.
Evaluate the post based on:
- Authenticity of technical claims
- Relevance to DevOps topics such as CI/CD, automation, infrastructure, monitoring, or reliability

Use only the information in the post.

Post:
{post}

Provide a detailed assessment.
Return the response **only** in this JSON format:
{{
    "authenticity": "<Your assessment of technical authenticity>",
    "relevance": "<How relevant the post is to DevOps principles and practices>",
    "comments": "<Any additional DevOps-specific comments>",
    "tips": "<Clear, actionable improvements the user can apply to their content>",
    "score": <A score from 1 to 10>
}}
"""
)

# ----------------------------------------
# 3. GenAI Engineer Perspective
# ----------------------------------------
genai_engineer_perspective = PromptTemplate(
    input_variables=["post"],
    template="""
You are analyzing a LinkedIn post **strictly from the perspective of a Generative AI engineer**.
Evaluate the post based on:
- Authenticity of claims related to LLMs, embeddings, training, inference, agents, or pipelines
- Relevance to modern GenAI concepts and practices

Use only the information in the post.

Post:
{post}

Provide a detailed assessment.
Return the response **only** in this JSON format:
{{
    "authenticity": "<Your assessment of AI-related authenticity>",
    "relevance": "<How relevant the post is to GenAI engineering topics>",
    "comments": "<Any additional GenAI-specific comments>",
    "tips": "<Clear, actionable improvements the user can apply to their content>",
    "score": <A score from 1 to 10>
}}
"""
)

# ----------------------------------------
# 4. Backend Engineer / SDE2 Perspective
# ----------------------------------------
backend_engineer_perspective = PromptTemplate(
    input_variables=["post"],
    template="""
You are analyzing a LinkedIn post **strictly from the perspective of a backend engineer / SDE2**.
Evaluate the post for:
- Authenticity of engineering claims
- Relevance to backend topics such as system design, APIs, scalability, performance, databases, distributed systems

Use only the information in the post.

Post:
{post}

Provide a detailed assessment.
Return the response **only** in this JSON format:
{{
    "authenticity": "<Your assessment of engineering authenticity>",
    "relevance": "<How relevant the post is to backend engineering topics>",
    "comments": "<Any additional backend-specific comments>",
    "tips": "<Clear, actionable improvements the user can apply to their content>",
    "score": <A score from 1 to 10>
}}
"""
)

# ----------------------------------------
# 5. Hiring Manager Perspective
# ----------------------------------------
hiring_manager_perspective = PromptTemplate(
    input_variables=["post"],
    template="""
You are analyzing a LinkedIn post **strictly from the perspective of a hiring manager**.
Evaluate the post for:
- Authenticity of communication and experience
- Relevance to professional maturity, leadership signals, decision-making, and candidate potential

Use only the information in the post.

Post:
{post}

Provide a detailed assessment.
Return the response **only** in this JSON format:
{{
    "authenticity": "<Your assessment of authenticity and professional credibility>",
    "relevance": "<How relevant the post is to hiring expectations and professional evaluation>",
    "comments": "<Additional notes from a hiring manager's point of view>",
    "tips": "<Clear, actionable improvements the user can apply to their content>",
    "score": <A score from 1 to 10>
}}
"""
)
