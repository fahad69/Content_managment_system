"""
Pydantic model for a Blog Summary.
This model only includes the minimal fields needed for the landing page.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

class BlogSummary(BaseModel):
    id: str = Field(None, alias="_id")
    title: str = Field(..., description="The title of the blog post")
    snippet: str = Field(..., description="A short snippet from the blog post")
    image_url: str = Field(None, description="URL for the blog post's image")
    created_at: datetime = Field(..., description="Creation date of the blog post")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
