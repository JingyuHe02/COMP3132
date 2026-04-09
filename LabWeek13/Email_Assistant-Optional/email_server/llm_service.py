import os

import aisuite as ai
import markdown
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .display_functions import pretty_print_chat_completion_html
from .email_tools import (
    delete_email,
    filter_emails,
    get_email,
    list_all_emails,
    list_unread_emails,
    mark_email_as_read,
    mark_email_as_unread,
    search_emails,
    search_unread_from_sender,
    send_email,
)

load_dotenv()
client = ai.Client()
DEFAULT_MODEL = os.getenv("EMAIL_ASSISTANT_MODEL", "openai:gpt-4.1")

app = FastAPI(title="LLM Email Prompt Executor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptInput(BaseModel):
    prompt: str


@app.post("/prompt")
async def handle_prompt(payload: PromptInput):
    prompt_ = f"""
        - You are an AI assistant specialized in managing emails.
        - You can perform various actions such as listing, searching, filtering, and manipulating emails.
        - Use the provided tools to interact with the email system.
        - Never ask the user for confirmation before performing an action.
        - If needed, my email address is "you@email.com" so you can use it to send emails or perform actions related to my account.
        {payload.prompt}
        """

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt_}],
            tools=[
                list_all_emails,
                list_unread_emails,
                search_emails,
                filter_emails,
                get_email,
                mark_email_as_read,
                mark_email_as_unread,
                send_email,
                delete_email,
                search_unread_from_sender,
            ],
            max_turns=20,
        )
    except Exception as exc:
        message = str(exc)
        lowered = message.lower()
        status_code = 502

        if "quota" in lowered or "rate limit" in lowered or "429" in lowered:
            status_code = 503
        elif "api key" in lowered or "authentication" in lowered:
            status_code = 401

        raise HTTPException(
            status_code=status_code,
            detail=f"LLM request failed: {message}",
        ) from exc

    html_response = pretty_print_chat_completion_html(response)
    final_text = markdown.markdown(response.choices[0].message.content)

    return {
        "model": DEFAULT_MODEL,
        "response": final_text,
        "html_response": html_response,
    }
