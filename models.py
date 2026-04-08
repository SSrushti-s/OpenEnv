
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# 1. What the AI sees (The View)
class EmailSnippet(BaseModel):
    id: int
    sender: str
    subject: str
    body_preview: str
    timestamp: str
    priority: Literal["low", "medium", "high"]

class EmailObservation(BaseModel):
    inbox: List[EmailSnippet]
    unread_count: int
    current_folder: str = "INBOX"
    error_message: Optional[str] = None

# 2. What the AI can do (The Controls)
class EmailAction(BaseModel):
    command: Literal["archive", "delete", "label", "reply"]
    email_id: int
    label_name: Optional[str] = Field(None, description="Used only for 'label' command")
    reply_text: Optional[str] = Field(None, description="Used only for 'reply' command")

# 3. How the AI is scored (The Feedback)
class EmailReward(BaseModel):
    reward: float = Field(..., description="Numerical score for the action")
    comment: str = Field(..., description="Explanation of why this reward was given")
    is_terminal: bool = Field(False, description="True if the task is finished")