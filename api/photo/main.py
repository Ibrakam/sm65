from fastapi import APIRouter, UploadFile, File
import random

photo_router = APIRouter(prefix="/photo", tags=["PhotoApi"])


@photo_router.post('/add_photo')
async def add_photo_api(pid: int, photo_file: UploadFile = File(...)):
    file_id = random.randint(1, 1_000_000)
    if photo_file:
        try:
            with open(f"database/images/photo_{file_id}_{pid}.jpg", "wb") as photo:
                photo_to_save = await photo_file.read()
                photo.write(photo_to_save)
                return {"status": 1, "message": "Фото успешно загружено"}
        except Exception as e:
            return {"status": 0, "message": e}
