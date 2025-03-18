"""
API endpoints for fetching CMS statistics.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from db.mongodb import website_collection, blog_collection

router = APIRouter()

@router.get("/", response_model=dict)
async def get_cms_stats():
    """
    Fetch CMS statistics including:
      - Total registered domains.
      - For each domain: the count of blogs generated today and status (completed/pending).
      - Count of domains that have completed or are pending today's blog quota.
    
    Assumes that each domain should have at least 2 blogs generated per day.
    """
    # Count total registered domains.
    total_domains = await website_collection.count_documents({})

    # Fetch the list of registered domains.
    domains_cursor = website_collection.find({}, {"domain": 1, "_id": 0})
    domains_list = await domains_cursor.to_list(length=None)
    domain_names = [doc["domain"] for doc in domains_list]

    # Determine today's starting time (UTC).
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    domain_stats = []
    completed_domains = []
    pending_domains = []

    for domain in domain_names:
        # Count how many blogs for this domain were generated today.
        count = await blog_collection.count_documents({
            "domain": domain,
            "created_at": {"$gte": today_start}
        })
        status = "completed" if count >= 2 else "pending"
        domain_stats.append({
            "domain": domain,
            "blogs_generated_today": count,
            "status": status
        })
        if status == "completed":
            completed_domains.append(domain)
        else:
            pending_domains.append(domain)

    stats = {
        "total_domains": total_domains,
        "domain_stats": domain_stats,
        "completed_domains_count": len(completed_domains),
        "pending_domains_count": len(pending_domains)
    }
    return stats
