from typing import Optional


SYSTEM_PROMPT = """You are a helpful, accurate, polite customer support assistant.
You MUST answer strictly based on the provided training and customer service knowledge.

Guidelines:
- Be concise but helpful.
- Maintain a professional tone.
- Do NOT hallucinate unknown policies or information.
- If unclear, ask for clarification.
"""


def build_prompt(user_query: str, context: Optional[str] = None) -> str:
    """
    Builds the final prompt sent to the LLM.
    Includes system prompt + optional context + user query.
    """

    prompt = f"<system>\n{SYSTEM_PROMPT}\n</system>\n\n"

    if context:
        prompt += f"<context>\n{context}\n</context>\n\n"

    prompt += f"<user>\n{user_query}\n</user>\n\n<assistant>\n"

    return prompt
