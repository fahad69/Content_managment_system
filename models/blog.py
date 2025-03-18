"""
Pydantic model for a Blog post.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

class Blog(BaseModel):
    id: str = Field(None, alias="_id")
    domain: str = Field(..., description="The domain associated with this blog")
    title: str = Field(..., description="The title of the blog post")
    content: str = Field(..., description="The content of the blog post")
    snippet: str = Field(None, description="A short snippet of the blog post's content")
    image_url: str = Field(None, description="URL for the blog post's image")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
