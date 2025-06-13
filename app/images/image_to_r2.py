import asyncio
import threading
from uuid import uuid4
from PIL import Image, ImageOps
from io import BytesIO
from app.db.queries.answers import edit_answer
from app.cloud.r2_cloudflare import r2_client

def run_async_task_in_new_loop(coro):
    def runner():
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(coro)
        new_loop.close()

    thread = threading.Thread(target=runner)
    thread.start()

def save_image(
    image_bytes: bytes,
    answer_id: int = None,
    question_id: int = None
) -> None:
    if answer_id is None and question_id is None:
        raise ValueError("answer_id and question_id can't be both None")
    with Image.open(BytesIO(image_bytes)) as image:
        img = ImageOps.exif_transpose(image).convert("RGB")
        resized = ImageOps.fit(img, (512, 512))
        filename = uuid4().hex
        while True:
            try:
                run_async_task_in_new_loop(r2_client.upload_file(resized, f"{filename}.webp"))
                break
            except FileExistsError:
                pass
        run_async_task_in_new_loop(edit_answer(answer_id=answer_id, filename=filename))

