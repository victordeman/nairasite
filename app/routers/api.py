import json
from fastapi import APIRouter, Depends, HTTPException
import libsql_client
from app.database import get_db, to_dict_list
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
    ChatRequest,
    ChatResponse,
)

router = APIRouter(prefix="/api", tags=["api"])

# --- Pillars ---
@router.get("/pillars", response_model=list[PillarResponse])
async def get_pillars(db: libsql_client.Client = Depends(get_db)):
    result = await db.execute("SELECT * FROM pillars ORDER BY number")
    return to_dict_list(result)

@router.post("/pillars", response_model=PillarResponse, status_code=201)
async def create_pillar(pillar: PillarCreate, db: libsql_client.Client = Depends(get_db)):
    result = await db.execute(
        "INSERT INTO pillars (number, title, description, icon, color) VALUES (?, ?, ?, ?, ?)",
        (pillar.number, pillar.title, pillar.description, pillar.icon, pillar.color),
    )
    new_id = result.last_insert_rowid
    return {**pillar.model_dump(), "id": new_id}

@router.put("/pillars/{pillar_id}", response_model=PillarResponse)
async def update_pillar(pillar_id: int, pillar: PillarCreate, db: libsql_client.Client = Depends(get_db)):
    result = await db.execute("SELECT id FROM pillars WHERE id = ?", (pillar_id,))
    if not result.rows:
        raise HTTPException(status_code=404, detail="Pillar not found")
    
    await db.execute(
        "UPDATE pillars SET number=?, title=?, description=?, icon=?, color=? WHERE id=?",
        (pillar.number, pillar.title, pillar.description, pillar.icon, pillar.color, pillar_id),
    )
    return {**pillar.model_dump(), "id": pillar_id}

@router.delete("/pillars/{pillar_id}", response_model=MessageResponse)
async def delete_pillar(pillar_id: int, db: libsql_client.Client = Depends(get_db)):
    result = await db.execute("SELECT id FROM pillars WHERE id = ?", (pillar_id,))
    if not result.rows:
        raise HTTPException(status_code=404, detail="Pillar not found")
    
    await db.execute("DELETE FROM pillars WHERE id = ?", (pillar_id,))
    return {"message": "Pillar deleted", "success": True}

# --- Architecture Layers ---
@router.get("/architecture", response_model=list[ArchitectureLayerResponse])
async def get_architecture_layers(db: libsql_client.Client = Depends(get_db)):
    result = await db.execute("SELECT * FROM architecture_layers ORDER BY layer_number")
    res_list = to_dict_list(result)
    for d in res_list:
        d["tags"] = json.loads(d["tags"])
    return res_list

@router.post("/architecture", response_model=ArchitectureLayerResponse, status_code=201)
async def create_architecture_layer(layer: ArchitectureLayerCreate, db: libsql_client.Client = Depends(get_db)):
    result = await db.execute(
        "INSERT INTO architecture_layers (layer_number, title, description, icon, color, tags) VALUES (?, ?, ?, ?, ?, ?)",
        (layer.layer_number, layer.title, layer.description, layer.icon, layer.color, json.dumps(layer.tags)),
    )
    new_id = result.last_insert_rowid
    return {**layer.model_dump(), "id": new_id}

@router.put("/architecture/{layer_id}", response_model=ArchitectureLayerResponse)
async def update_architecture_layer(layer_id: int, layer: ArchitectureLayerCreate, db: libsql_client.Client = Depends(get_db)):
    result = await db.execute("SELECT id FROM architecture_layers WHERE id = ?", (layer_id,))
    if not result.rows:
        raise HTTPException(status_code=404, detail="Architecture layer not found")
    
    await db.execute(
        "UPDATE architecture_layers SET layer_number=?, title=?, description=?, icon=?, color=?, tags=? WHERE id=?",
        (layer.layer_number, layer.title, layer.description, layer.icon, layer.color, json.dumps(layer.tags), layer_id),
    )
    return {**layer.model_dump(), "id": layer_id}

@router.delete("/architecture/{layer_id}", response_model=MessageResponse)
async def delete_architecture_layer(layer_id: int, db: libsql_client.Client = Depends(get_db)):
    result = await db.execute("SELECT id FROM architecture_layers WHERE id = ?", (layer_id,))
    if not result.rows:
        raise HTTPException(status_code=404, detail="Architecture layer not found")
    
    await db.execute("DELETE FROM architecture_layers WHERE id = ?", (layer_id,))
    return {"message": "Architecture layer deleted", "success": True}

# --- Revenue Streams ---
@router.get("/revenue-streams", response_model=list[RevenueStreamResponse])
async def get_revenue_streams(db: libsql_client.Client = Depends(get_db)):
    result = await db.execute("SELECT * FROM revenue_streams ORDER BY id")
    return to_dict_list(result)

@router.post("/revenue-streams", response_model=RevenueStreamResponse, status_code=201)
async def create_revenue_stream(stream: RevenueStreamCreate, db: libsql_client.Client = Depends(get_db)):
    result = await db.execute(
        "INSERT INTO revenue_streams (title, description, icon, color) VALUES (?, ?, ?, ?)",
        (stream.title, stream.description, stream.icon, stream.color),
    )
    new_id = result.last_insert_rowid
    return {**stream.model_dump(), "id": new_id}

@router.delete("/revenue-streams/{stream_id}", response_model=MessageResponse)
async def delete_revenue_stream(stream_id: int, db: libsql_client.Client = Depends(get_db)):
    result = await db.execute("SELECT id FROM revenue_streams WHERE id = ?", (stream_id,))
    if not result.rows:
        raise HTTPException(status_code=404, detail="Revenue stream not found")
    
    await db.execute("DELETE FROM revenue_streams WHERE id = ?", (stream_id,))
    return {"message": "Revenue stream deleted", "success": True}

# --- Contact Form ---
@router.post("/contact", response_model=MessageResponse, status_code=201)
async def submit_contact(submission: ContactSubmission, db: libsql_client.Client = Depends(get_db)):
    await db.execute(
        "INSERT INTO contact_submissions (name, email, role, message) VALUES (?, ?, ?, ?)",
        (submission.name, submission.email, submission.role, submission.message),
    )
    return {"message": "Thank you for reaching out! We will get back to you soon.", "success": True}

@router.get("/contact", response_model=list[ContactResponse])
async def get_contacts(db: libsql_client.Client = Depends(get_db)):
    result = await db.execute("SELECT * FROM contact_submissions ORDER BY created_at DESC")
    return to_dict_list(result)

# --- Newsletter ---
@router.post("/newsletter", response_model=MessageResponse, status_code=201)
async def subscribe_newsletter(subscription: NewsletterSubscription, db: libsql_client.Client = Depends(get_db)):
    try:
        await db.execute(
            "INSERT INTO newsletter_subscribers (email) VALUES (?)",
            (subscription.email,),
        )
        return {"message": "Successfully subscribed to the newsletter!", "success": True}
    except Exception:
        return {"message": "This email is already subscribed.", "success": False}

@router.get("/newsletter", response_model=list[NewsletterResponse])
async def get_subscribers(db: libsql_client.Client = Depends(get_db)):
    result = await db.execute("SELECT * FROM newsletter_subscribers ORDER BY created_at DESC")
    return to_dict_list(result)

# --- Stats ---
@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: libsql_client.Client = Depends(get_db)):
    pillars_res = await db.execute("SELECT COUNT(*) FROM pillars")
    pillars_count = pillars_res.rows[0][0]
    
    layers_res = await db.execute("SELECT COUNT(*) FROM architecture_layers")
    layers_count = layers_res.rows[0][0]
    
    return {
        "pillars_count": pillars_count,
        "architecture_layers_count": layers_count,
        "xr_label": "XR",
        "ai_label": "AI",
    }

# --- AI Chat ---
@router.post("/chat", response_model=ChatResponse)
async def chat_ai(request: ChatRequest, db: libsql_client.Client = Depends(get_db)):
    full_message = request.message.lower()
    keywords = full_message.split()
    
    # Tables and their searchable columns
    search_targets = [
        ("pillars", ["title", "description"]),
        ("projects", ["title", "description", "category"]),
        ("architecture_layers", ["title", "description", "tags"]),
        ("revenue_streams", ["title", "description"])
    ]
    
    results = {
        "pillars": [],
        "projects": [],
        "architecture": [],
        "revenue": []
    }
    
    for table, columns in search_targets:
        where_clauses = []
        params = []
        # First try full message if it's not too long
        if len(full_message) > 3:
            for col in columns:
                where_clauses.append(f"LOWER({col}) LIKE ?")
                params.append(f"%{full_message}%")

        # Then try individual keywords
        for kw in keywords:
            if len(kw) < 4: continue # Skip short words
            for col in columns:
                where_clauses.append(f"LOWER({col}) LIKE ?")
                params.append(f"%{kw}%")
        
        if not where_clauses:
            continue
            
        sql = f"SELECT * FROM {table} WHERE " + " OR ".join(where_clauses)
        res = await db.execute(sql, params)
        key = "architecture" if table == "architecture_layers" else table.replace("_streams", "").replace("pillars", "pillars").replace("projects", "projects")
        # Deduplicate results based on title
        existing_titles = [r['title'] for r in results[key]]
        for row in to_dict_list(res):
            if row['title'] not in existing_titles:
                results[key].append(row)

    pillars = results["pillars"]
    projects = results["projects"]
    architecture = results["architecture"]
    revenue = results["revenue"]

    # Construct Response
    if not (pillars or projects or architecture or revenue):
        return {"response": "I couldn't find specific information about that in the NAIRA database. Could you ask about our pillars, projects, architecture, or revenue streams?"}
    
    response_parts = []
    
    if pillars:
        part = "Strategic Pillars: " + "; ".join([f"{p['title']} ({p['description']})" for p in pillars])
        response_parts.append(part)
        
    if projects:
        part = "Projects: " + "; ".join([f"{p['title']} - Status: {p['status']} ({p['description']})" for p in projects])
        response_parts.append(part)
        
    if architecture:
        part = "Architecture: " + "; ".join([f"{a['title']} ({a['description']})" for a in architecture])
        response_parts.append(part)
        
    if revenue:
        part = "Revenue Streams: " + "; ".join([f"{r['title']} ({r['description']})" for r in revenue])
        response_parts.append(part)
        
    final_response = "Here is what I found:\n\n" + "\n\n".join(response_parts)
    return {"response": final_response}
