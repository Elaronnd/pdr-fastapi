import uvicorn
import asyncio
from app.web.__init__ import app

async def main():
    uvicorn.run("main:app", reload=True)

if __name__ == "__main__":
    asyncio.run(main())
