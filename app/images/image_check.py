from io import BytesIO

from PIL import Image
from fastapi import UploadFile

from app.exceptions import AnswerImageError


async def image_validator(
    image: UploadFile,
    image_bytes: bytes
):
    filename = image.filename
    if not filename.lower().endswith((".jpg",".jpeg",".png",".webp")):
        raise AnswerImageError(status_code=406, message="Your file is not image", filename=filename)
    elif image.size > 5000000:
        raise AnswerImageError(status_code=413, message=f"Your image is too large", filename=filename)
    width, height = Image.open(BytesIO(image_bytes)).size
    if width < 512 or height < 512:
        raise AnswerImageError(status_code=413,
                               message=f"Image \"{filename}\" resolution does not correspond to 512x512",
                               filename=filename)
