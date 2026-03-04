import json
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
import aiosqlite
from app.database import get_db
router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")
@router.get("/")
async def home(request: Request, db: aiosqlite.Connection = Depends(get_db)):
    # Fetch all data from DB
    cursor = await db.execute("SELECT * FROM pillars ORDER BY number")
    pillars = [dict(row) for row in await cursor.fetchall()]
    cursor = await db.execute("SELECT * FROM architecture_layers ORDER BY layer_number")
    layers_raw = await cursor.fetchall()
    architecture_layers = []
    for row in layers_raw:
        d = dict(row)
        d["tags"] = json.loads(d["tags"])
        architecture_layers.append(d)
    cursor = await db.execute("SELECT * FROM revenue_streams ORDER BY id")
    revenue_streams = [dict(row) for row in await cursor.fetchall()]
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
            "pillars": pillars,
            "architecture_layers": architecture_layers,
            "revenue_streams": revenue_streams,
            "stats": stats,
        },
    )
