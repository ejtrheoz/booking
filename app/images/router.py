from fastapi import APIRouter, UploadFile
import shutil

from app.tasks.tasks import resize_image


router = APIRouter(
    prefix="/images",
    tags=["images"],
)


@router.post("/hotels/")
async def upload_hotel_image(name: int, file: UploadFile):
    im_path = f"app/static/images/{name}.webp"

    with open(im_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    resize_image.delay(im_path)
    
