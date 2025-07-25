from fastapi import APIRouter, UploadFile, File, Request
import numpy as np
import cv2
import queue


from shared.image_data import ImageWithMeta

upload_router  = APIRouter()

@upload_router .post("/image")
async def upload_image(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    
    # Đọc ảnh từ binary và chuyển sang định dạng OpenCV
    np_img = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    img = ImageWithMeta(img)

    # Đẩy ảnh vào queue
    try:
        request.app.state.image_queue.put_nowait(img)
        return {"status": "Image added to queue"}
    except queue.Full:
        return {"status": "Queue is full. Try again later."}

