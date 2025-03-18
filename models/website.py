"""
Pydantic model for Website registration.
"""

from pydantic import BaseModel, Field
from datetime import datetime

class Website(BaseModel):
    domain: str = Field(..., description="The domain name of the website")
    created_at: datetime = Field(default_factory=datetime.utcnow)
