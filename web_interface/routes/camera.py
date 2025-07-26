from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


camera_router  = APIRouter()

@camera_router.post("/capture")
async def capture_image(request: Request):
    # Lấy biến camera_controller từ app.state
    camera_controller = request.app.state.camera_controller

    # Chụp ảnh
    success  = camera_controller.capture()
    
    if not success:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Could not send trigger to camera"
            }
        )

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "Image captured successfully"
        }
    )

