import json
from config import API_URL, CHAT_COMPLETIONS_API_KEY, LLM_MODEL_NAME, LLM_TEMPERATURE, MAX_TOKEN
import openai

openai.api_key = CHAT_COMPLETIONS_API_KEY
openai.base_url = API_URL


def _normalize_message(message):
    if isinstance(message, dict):
        role = message.get("role")
        content = message.get("content")
        if role is None or content is None:
            return []
        return [{"role": role, "content": content}]

    if isinstance(message, (list, tuple)) and len(message) == 2:
        user_content, assistant_content = message
        if isinstance(user_content, str) and isinstance(assistant_content, str):
            return [
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content},
            ]

    if isinstance(message, (list, tuple)):
        sanitized = []
        for item in message:
            sanitized.extend(_normalize_message(item))
        return sanitized

    return []


def sanitize_messages(messages):
    sanitized = []
    for message in messages:
        sanitized.extend(_normalize_message(message))
    return sanitized


def call_chat_api(messages, tools=[], disable_reasoning=True):
    """
    Calls the LLM API with tools for function calling using OpenAI library.
    Returns the response object or None on failure.
    """
    messages = sanitize_messages(messages)
    payload = json.dumps(messages)
    #print("DEBUG", f"Prompt Length: {len(payload)}")

    extra_body: dict = {}
    if disable_reasoning:
        extra_body["reasoning_effort"] = "none"

    try:
        response = openai.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=messages,
            tools=tools,
            temperature=LLM_TEMPERATURE,
            max_tokens=MAX_TOKEN,
            extra_body=extra_body,
        )

        usage = getattr(response, "usage", None)
        # if usage:
        #     print("DEBUG", f"Usage of LLM API: {usage}")

        return response
    except Exception as e:
        print("ERROR", f"Error calling LLM API with tools: {e}")
        return None

#Test Run
#print(f"Response: {call_chat_api([{'role': 'user', 'content': 'Hello, how are you?'}])}")