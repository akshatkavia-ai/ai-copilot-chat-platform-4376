from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatMessageRole(str, Enum):
    """Role of a message in the chat history."""
    user = "user"
    assistant = "assistant"


class HistoryItem(BaseModel):
    """Single turn in chat history."""
    role: ChatMessageRole = Field(..., description="Role of the message author: user or assistant.")
    content: str = Field(..., description="Text content of the message.")


# PUBLIC_INTERFACE
class ChatRequest(BaseModel):
    """Input payload for the /chat endpoint."""
    message: str = Field(..., description="The latest user message to send to Gemini.")
    history: Optional[List[HistoryItem]] = Field(
        default=None,
        description="Optional chat history of prior messages for context."
    )


# PUBLIC_INTERFACE
class ChatResponse(BaseModel):
    """Response from the /chat endpoint containing assistant reply."""
    reply: str = Field(..., description="The assistant's generated reply text.")
