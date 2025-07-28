#!/home/vision/projects/defect_detection/venv/bin/python
import os
from fastapi import FastAPI, Request
from web_interface.routes.upload import upload_router
from web_interface.routes.camera import camera_router
from web_interface.routes.websocket import websocket_router

from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


# sys.path.append(os.path.abspath("./services"))

from core.lifespan import lifespan


app = FastAPI(lifespan=lifespan)

# Mount static files (for serving images, JS, CSS, etc.)
app.mount("/static", StaticFiles(directory=os.path.join("web_interface", "static")), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory=os.path.join("web_interface", "templates"))

@app.get("/")
@app.get("/panel", response_class=HTMLResponse)
async def control_panel(request: Request):
    # Trả về giao diện điều khiển AI Vision
    return templates.TemplateResponse("index3.html", {"request": request})

app.include_router(websocket_router)
app.include_router(upload_router, prefix="/upload")
app.include_router(camera_router, prefix="/camera")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

   
