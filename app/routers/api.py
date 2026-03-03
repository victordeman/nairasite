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
@router.post("/pillars", response_model=PillarResponse, status_code=201)
async def create_pillar(pillar: PillarCreate, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "INSERT INTO pillars (number, title, description, icon, color) VALUES (?, ?, ?, ?, ?)",
        (pillar.number, pillar.title, pillar.description, pillar.icon, pillar.color),
    )
    await db.commit()
    new_id = cursor.lastrowid
    return {**pillar.model_dump(), "id": new_id}
@router.put("/pillars/{pillar_id}", response_model=PillarResponse)
async def update_pillar(pillar_id: int, pillar: PillarCreate, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT id FROM pillars WHERE id = ?", (pillar_id,))
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="Pillar not found")
    await db.execute(
        "UPDATE pillars SET number=?, title=?, description=?, icon=?, color=? WHERE id=?",
        (pillar.number, pillar.title, pillar.description, pillar.icon, pillar.color, pillar_id),
    )
    await db.commit()
    return {**pillar.model_dump(), "id": pillar_id}
@router.delete("/pillars/{pillar_id}", response_model=MessageResponse)
async def delete_pillar(pillar_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT id FROM pillars WHERE id = ?", (pillar_id,))
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="Pillar not found")
    await db.execute("DELETE FROM pillars WHERE id = ?", (pillar_id,))
    await db.commit()
    return {"message": "Pillar deleted", "success": True}
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
@router.post("/architecture", response_model=ArchitectureLayerResponse, status_code=201)
async def create_architecture_layer(layer: ArchitectureLayerCreate, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "INSERT INTO architecture_layers (layer_number, title, description, icon, color, tags) VALUES (?, ?, ?, ?, ?, ?)",
        (layer.layer_number, layer.title, layer.description, layer.icon, layer.color, json.dumps(layer.tags)),
    )
    await db.commit()
    new_id = cursor.lastrowid
    return {**layer.model_dump(), "id": new_id}
@router.put("/architecture/{layer_id}", response_model=ArchitectureLayerResponse)
async def update_architecture_layer(layer_id: int, layer: ArchitectureLayerCreate, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT id FROM architecture_layers WHERE id = ?", (layer_id,))
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="Architecture layer not found")
    await db.execute(
        "UPDATE architecture_layers SET layer_number=?, title=?, description=?, icon=?, color=?, tags=? WHERE id=?",
        (layer.layer_number, layer.title, layer.description, layer.icon, layer.color, json.dumps(layer.tags), layer_id),
    )
    await db.commit()
    return {**layer.model_dump(), "id": layer_id}
@router.delete("/architecture/{layer_id}", response_model=MessageResponse)
async def delete_architecture_layer(layer_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT id FROM architecture_layers WHERE id = ?", (layer_id,))
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="Architecture layer not found")
    await db.execute("DELETE FROM architecture_layers WHERE id = ?", (layer_id,))
    await db.commit()
    return {"message": "Architecture layer deleted", "success": True}
# --- Revenue Streams ---
@router.get("/revenue-streams", response_model=list[RevenueStreamResponse])
async def get_revenue_streams(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM revenue_streams ORDER BY id")
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]
@router.post("/revenue-streams", response_model=RevenueStreamResponse, status_code=201)
async def create_revenue_stream(stream: RevenueStreamCreate, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "INSERT INTO revenue_streams (title, description, icon, color) VALUES (?, ?, ?, ?)",
        (stream.title, stream.description, stream.icon, stream.color),
    )
    await db.commit()
    new_id = cursor.lastrowid
    return {**stream.model_dump(), "id": new_id}
@router.delete("/revenue-streams/{stream_id}", response_model=MessageResponse)
async def delete_revenue_stream(stream_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT id FROM revenue_streams WHERE id = ?", (stream_id,))
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="Revenue stream not found")
    await db.execute("DELETE FROM revenue_streams WHERE id = ?", (stream_id,))
    await db.commit()
    return {"message": "Revenue stream deleted", "success": True}
# --- Contact Form ---
@router.post("/contact", response_model=MessageResponse, status_code=201)
async def submit_contact(submission: ContactSubmission, db: aiosqlite.Connection = Depends(get_db)):
    await db.execute(
        "INSERT INTO contact_submissions (name, email, role, message) VALUES (?, ?, ?, ?)",
        (submission.name, submission.email, submission.role, submission.message),
    )
    await db.commit()
    return {"message": "Thank you for reaching out! We will get back to you soon.", "success": True}
@router.get("/contact", response_model=list[ContactResponse])
async def get_contacts(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM contact_submissions ORDER BY created_at DESC")
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]
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
@router.get("/newsletter", response_model=list[NewsletterResponse])
async def get_subscribers(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM newsletter_subscribers ORDER BY created_at DESC")
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]
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
