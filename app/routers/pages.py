import os
import json
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
import aiosqlite
from app.database import get_db

router = APIRouter(tags=["pages"])

# Use absolute path for templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/")
async def home(request: Request, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT COUNT(*) FROM pillars")
    pillars_count = (await cursor.fetchone())[0]

    cursor = await db.execute("SELECT COUNT(*) FROM architecture_layers")
    layers_count = (await cursor.fetchone())[0]

    stats = {
        "pillars_count": pillars_count,
        "architecture_layers_count": layers_count,
        "xr_label": "XR",
        "ai_label": "AI",
    }

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "stats": stats,
        },
    )

@router.get("/vision")
async def vision(request: Request):
    return templates.TemplateResponse("vision.html", {"request": request})

@router.get("/pillars")
async def pillars(request: Request, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM pillars ORDER BY number")
    pillars = [dict(row) for row in await cursor.fetchall()]
    return templates.TemplateResponse("pillars.html", {"request": request, "pillars": pillars})

@router.get("/architecture")
async def architecture(request: Request, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM architecture_layers ORDER BY layer_number")
    layers_raw = await cursor.fetchall()
    architecture_layers = []
    for row in layers_raw:
        d = dict(row)
        d["tags"] = json.loads(d["tags"])
        architecture_layers.append(d)
    return templates.TemplateResponse("architecture.html", {"request": request, "architecture_layers": architecture_layers})

@router.get("/revenue")
async def revenue(request: Request, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM revenue_streams ORDER BY id")
    revenue_streams = [dict(row) for row in await cursor.fetchall()]
    return templates.TemplateResponse("revenue.html", {"request": request, "revenue_streams": revenue_streams})

@router.get("/content")
async def content(request: Request):
    return templates.TemplateResponse("content.html", {"request": request})

@router.get("/projects")
async def projects(request: Request, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM projects ORDER BY id")
    projects = [dict(row) for row in await cursor.fetchall()]
    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})

@router.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})
