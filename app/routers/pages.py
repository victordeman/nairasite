import os
import json
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
import libsql_client
from app.database import get_db, to_dict_list

router = APIRouter(tags=["pages"])

# Define the base directory for templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/")
async def home(request: Request, db: libsql_client.Client = Depends(get_db)):
    pillars_res = await db.execute("SELECT * FROM pillars ORDER BY number")
    pillars = to_dict_list(pillars_res)
    
    layers_res = await db.execute("SELECT * FROM architecture_layers ORDER BY layer_number")
    architecture_layers = to_dict_list(layers_res)
    for d in architecture_layers:
        d["tags"] = json.loads(d["tags"])
    
    pillars_count_res = await db.execute("SELECT COUNT(*) FROM pillars")
    pillars_count = pillars_count_res.rows[0][0]
    
    layers_count_res = await db.execute("SELECT COUNT(*) FROM architecture_layers")
    layers_count = layers_count_res.rows[0][0]
    
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
            "pillars": pillars,
            "architecture_layers": architecture_layers,
            "stats": stats,
        },
    )

@router.get("/vision")
async def vision(request: Request):
    return templates.TemplateResponse("vision.html", {"request": request})

@router.get("/pillars")
async def pillars(request: Request, db: libsql_client.Client = Depends(get_db)):
    pillars_res = await db.execute("SELECT * FROM pillars ORDER BY number")
    pillars = to_dict_list(pillars_res)
    return templates.TemplateResponse("pillars.html", {"request": request, "pillars": pillars})

@router.get("/architecture")
async def architecture(request: Request, db: libsql_client.Client = Depends(get_db)):
    layers_res = await db.execute("SELECT * FROM architecture_layers ORDER BY layer_number")
    architecture_layers = to_dict_list(layers_res)
    for d in architecture_layers:
        d["tags"] = json.loads(d["tags"])
    return templates.TemplateResponse("architecture.html", {"request": request, "architecture_layers": architecture_layers})

@router.get("/revenue")
async def revenue(request: Request, db: libsql_client.Client = Depends(get_db)):
    revenue_res = await db.execute("SELECT * FROM revenue_streams ORDER BY id")
    revenue_streams = to_dict_list(revenue_res)
    return templates.TemplateResponse("revenue.html", {"request": request, "revenue_streams": revenue_streams})

@router.get("/content")
async def content(request: Request):
    return templates.TemplateResponse("content.html", {"request": request})

@router.get("/projects")
async def projects(request: Request, db: libsql_client.Client = Depends(get_db)):
    projects_res = await db.execute("SELECT * FROM projects ORDER BY id")
    projects = to_dict_list(projects_res)
    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})

@router.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@router.get("/agent")
async def agent(request: Request):
    return templates.TemplateResponse("agent.html", {"request": request})
