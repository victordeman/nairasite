import json
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
import libsql_client
from app.database import get_db, to_dict_list

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def home(request: Request, db: libsql_client.Client = Depends(get_db)):
    # Fetch all data from DB
    pillars_res = await db.execute("SELECT * FROM pillars ORDER BY number")
    pillars = to_dict_list(pillars_res)

    layers_res = await db.execute("SELECT * FROM architecture_layers ORDER BY layer_number")
    architecture_layers = to_dict_list(layers_res)
    for d in architecture_layers:
        d["tags"] = json.loads(d["tags"])

    revenue_res = await db.execute("SELECT * FROM revenue_streams ORDER BY id")
    revenue_streams = to_dict_list(revenue_res)

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
            "revenue_streams": revenue_streams,
            "stats": stats,
        },
    )
