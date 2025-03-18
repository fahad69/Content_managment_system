"""
Main FastAPI application for the CMS.
This application only integrates API endpoints for website registration and blog fetching.
"""

from fastapi import FastAPI
from api import websites, blogs,stats  

app = FastAPI(
    title="Custom CMS for Blogs",
    description="A CMS that registers websites and fetches blogs (AI agent is separate).",
    version="1.0.0"
)

# Include API routers for websites and blogs.
app.include_router(websites.router, prefix="/websites", tags=["Websites"])
app.include_router(blogs.router, prefix="/blogs", tags=["Blogs"])
app.include_router(stats.router, prefix="/stats", tags=["Statistics"])
@app.get("/")
async def root():
    return {"message": "Welcome to the CMS API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
