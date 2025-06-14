from io import BytesIO
from typing import Union, Type
from PIL import Image
from fastapi import UploadFile
from app.exceptions import AnswerImageError, QuestionImageError


async def image_validator(
    image: UploadFile,
    image_bytes: bytes,
    image_size: tuple[int, int],
    exception_image_error: Union[Type[QuestionImageError], Type[AnswerImageError]]
):
    filename = image.filename
    if not filename.lower().endswith((".jpg",".jpeg",".png",".webp")):
        raise exception_image_error(status_code=406, message="Your file is not image", filename=filename)
    elif image.size > 5000000:
        raise exception_image_error(status_code=413, message=f"Your image is too large", filename=filename)
    width, height = Image.open(BytesIO(image_bytes)).size
    if width < image_size[0] or height < image_size[1]:
        raise exception_image_error(status_code=413,
                               message=f"Image \"{filename}\" resolution does not correspond to {image_size[0]}x{image_size[1]}",
                               filename=filename)
