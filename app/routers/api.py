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
        "INSERT INTO pillars (number, title, summary, description, icon, color) VALUES (?, ?, ?, ?, ?, ?)",
        (pillar.number, pillar.title, pillar.summary, pillar.description, pillar.icon, pillar.color),
    )
    new_id = result.last_insert_rowid
    return {**pillar.model_dump(), "id": new_id}

@router.put("/pillars/{pillar_id}", response_model=PillarResponse)
async def update_pillar(pillar_id: int, pillar: PillarCreate, db: libsql_client.Client = Depends(get_db)):
    result = await db.execute("SELECT id FROM pillars WHERE id = ?", (pillar_id,))
    if not result.rows:
        raise HTTPException(status_code=404, detail="Pillar not found")
    
    await db.execute(
        "UPDATE pillars SET number=?, title=?, summary=?, description=?, icon=?, color=? WHERE id=?",
        (pillar.number, pillar.title, pillar.summary, pillar.description, pillar.icon, pillar.color, pillar_id),
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
async def get_naira_context(db: libsql_client.Client):
    """Retrieves all core info to serve as LLM context."""
    pillars = await db.execute("SELECT title, description FROM pillars")
    vision = await db.execute("SELECT title, description FROM vision_missions")
    architecture = await db.execute("SELECT title, description, tags FROM architecture_layers")
    revenue = await db.execute("SELECT title, description FROM revenue_streams")
    projects = await db.execute("SELECT title, summary, full_description, category, status, project_group FROM projects")
    
    context = "NAIRA (NBU AI Research & Advancement Institute) Context:\n\n"

    context += "VISION & MISSION:\n"
    for v in vision.rows:
        context += f"- {v[0]}: {v[1]}\n"
    
    context += "\nSTRATEGIC PILLARS:\n"
    for p in pillars.rows:
        context += f"- {p[0]}: {p[1]}\n"
        
    context += "\nARCHITECTURE LAYERS:\n"
    for a in architecture.rows:
        context += f"- {a[0]}: {a[1]} (Tags: {a[2]})\n"
        
    context += "\nREVENUE STREAMS:\n"
    for r in revenue.rows:
        context += f"- {r[0]}: {r[1]}\n"
        
    context += "\nKEY PROJECTS & USE-CASES:\n"
    for pr in projects.rows:
        context += f"- {pr[0]} ({pr[3]}): {pr[1]} (Group: {pr[5]}) [Status: {pr[4]}]\n"
        
    return context

@router.post("/chat", response_model=ChatResponse)
async def chat_ai(request: ChatRequest, db: libsql_client.Client = Depends(get_db)):
    user_msg = request.message
    selected_model = request.model
    naira_context = await get_naira_context(db)
    
    system_prompt = f"""You are the NAIRA AI Assistant, an expert on the NBU AI Research & Advancement Institute.
Your goal is to provide helpful, accurate, and culturally relevant information about NAIRA's work in AI and XR.

{naira_context}

Guidelines:
1. Use the provided context to answer questions about NAIRA.
2. If the user asks something outside this context, answer generally but try to relate it back to NAIRA's mission (African-centered AI/XR).
3. Be professional, visionary, and encouraging.
4. Keep responses concise but informative.
"""

    # For now, we use a mock LLM response that incorporates the context 
    # unless an API key is detected (Integration Placeholder)
    import os
    gemini_key = os.getenv("GOOGLE_API_KEY")
    hf_token = os.getenv("HF_TOKEN")

    if selected_model == "gemini" and gemini_key:
        # Placeholder for real Gemini call
        # response = call_gemini(system_prompt, user_msg)
        return {"response": f"[Gemini Mode] I've processed your request about '{user_msg}' using NAIRA's context."}
    elif selected_model == "hf" and hf_token:
        # Placeholder for real HF call
        return {"response": f"[Hugging Face Mode] Analyzing '{user_msg}' through the lens of African AI excellence."}
    elif selected_model in ["gemini", "hf"]:
        # User selected a premium model but keys are missing
        return {"response": f"I see you selected {selected_model.upper()}, but I'm currently running in Local RAG mode because no API keys were found. To use {selected_model.upper()}, please configure the environment variables."}
    else:
        # Enhanced RAG-lite fallback: if user message matches keywords, use specific context
        full_message = user_msg.lower()
        if any(k in full_message for k in ["pillar", "strategy", "focus"]):
            return {"response": "NAIRA operates on six strategic pillars, including African-Centered AI Research and Educational Transformation. Which pillar would you like to dive deeper into?"}
        if any(k in full_message for k in ["project", "doing", "working"]):
            return {"response": "We are currently working on several high-impact projects like the African Language LLM and XR Medical Simulations. These aim to solve local challenges using global tech."}
        if any(k in full_message for k in ["architecture", "layer", "system"]):
            return {"response": "Our architecture is built on three layers: Experience (XR), Intelligence (Generative AI), and Data/Integration. This ensures both immersion and intelligence."}
            
        return {"response": f"I'm the NAIRA Assistant. I can tell you all about our vision for African AI. You asked: '{user_msg}'. How can I relate this to our strategic pillars or current projects?"}
