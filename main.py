import uvicorn

from server import app
import os
PORT = os.getenv("PORT")
if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=int(PORT) if PORT else 8000,
        reload=False,
        workers=1,
    )