"""
API endpoints for website registration.
"""

from fastapi import APIRouter, HTTPException
from models.website import Website
from db.mongodb import website_collection

router = APIRouter()

@router.post("/", response_model=Website)
async def register_website(website: Website):
    """
    Register a new website in the CMS.
    
    - **website**: Website object containing the domain and registration timestamp.
    """
    # Check if the website already exists.
    existing = await website_collection.find_one({"domain": website.domain})
    if existing:
        raise HTTPException(status_code=400, detail="Website already exists")
    
    await website_collection.insert_one(website.dict())
    return website


@router.delete("/{domain}")
async def delete_website(domain: str):
    """
    Delete a website (domain) from the CMS.
    
    - **domain**: The domain to delete.
    """
    result = await website_collection.delete_one({"domain": domain})
    if result.deleted_count == 1:
        return {"message": f"Website '{domain}' deleted successfully."}
    raise HTTPException(status_code=404, detail="Website not found")