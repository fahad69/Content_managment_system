"""
API endpoints for fetching blog summaries.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from models.blog_summary import BlogSummary
from db.mongodb import blog_collection
from bson import ObjectId
from models.blog import Blog

router = APIRouter()

@router.get("/{domain}", response_model=List[BlogSummary])
async def get_blog_summaries(domain: str):
    """
    Fetch blog summaries (title, snippet, image_url, created_at) for a given website domain.
    
    - **domain**: Domain name used as an identifier.
    """
    # Use a projection to only fetch the required fields.
    projection = {
        "title": 1,
        "snippet": 1,
        "image_url": 1,
        "created_at": 1
    }
    cursor = blog_collection.find({"domain": domain}, projection)
    summaries = await cursor.to_list(length=1000)
    
    # Convert ObjectId to string for each summary.
    for summary in summaries:
        summary["_id"] = str(summary["_id"])
    
    return summaries

@router.get("/{domain}/{blog_id}", response_model=Blog)
async def get_blog(domain: str, blog_id: str):
    """
    Fetch a specific blog post (detailed view) by its ID and domain.
    
    - **domain**: Domain name to which the blog belongs.
    - **blog_id**: The unique identifier of the blog post.
    
    Returns the full blog post including its content.
    """
    blog = await blog_collection.find_one({"_id": ObjectId(blog_id), "domain": domain})
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog["_id"] = str(blog["_id"])
    return blog
