import json
from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
from app.database import get_db
from app.models.schemas import (
    PillarResponse,
    PillarCreate,
    ArchitectureLayerResponse,
    ArchitectureLayerCreate,
    RevenueStreamResponse,
    RevenueStreamCreate,
    ProjectResponse,
    ContactSubmission,
    ContactResponse,
    NewsletterSubscription,
    NewsletterResponse,
    StatsResponse,
    MessageResponse,
)

router = APIRouter(prefix="/api", tags=["api"])

# --- Pillars ---
@router.get("/pillars", response_model=list[PillarResponse])
async def get_pillars(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM pillars ORDER BY number")
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]

# --- Architecture Layers ---
@router.get("/architecture", response_model=list[ArchitectureLayerResponse])
async def get_architecture_layers(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM architecture_layers ORDER BY layer_number")
    rows = await cursor.fetchall()
    result = []
    for row in rows:
        d = dict(row)
        d["tags"] = json.loads(d["tags"])
        result.append(d)
    return result

# --- Revenue Streams ---
@router.get("/revenue-streams", response_model=list[RevenueStreamResponse])
async def get_revenue_streams(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM revenue_streams ORDER BY id")
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]

# --- Projects ---
@router.get("/projects", response_model=list[ProjectResponse])
async def get_projects(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM projects ORDER BY id")
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]

# --- Contact Form ---
@router.post("/contact", response_model=MessageResponse, status_code=201)
async def submit_contact(submission: ContactSubmission, db: aiosqlite.Connection = Depends(get_db)):
    await db.execute(
        "INSERT INTO contact_submissions (name, email, role, message) VALUES (?, ?, ?, ?)",
        (submission.name, submission.email, submission.role, submission.message),
    )
    await db.commit()
    return {"message": "Thank you for reaching out! We will get back to you soon.", "success": True}

# --- Newsletter ---
@router.post("/newsletter", response_model=MessageResponse, status_code=201)
async def subscribe_newsletter(subscription: NewsletterSubscription, db: aiosqlite.Connection = Depends(get_db)):
    try:
        await db.execute(
            "INSERT INTO newsletter_subscribers (email) VALUES (?)",
            (subscription.email,),
        )
        await db.commit()
        return {"message": "Successfully subscribed to the newsletter!", "success": True}
    except Exception:
        return {"message": "This email is already subscribed.", "success": False}

# --- Stats ---
@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT COUNT(*) FROM pillars")
    pillars_count = (await cursor.fetchone())[0]
    cursor = await db.execute("SELECT COUNT(*) FROM architecture_layers")
    layers_count = (await cursor.fetchone())[0]
    return {
        "pillars_count": pillars_count,
        "architecture_layers_count": layers_count,
        "xr_label": "XR",
        "ai_label": "AI",
    }
