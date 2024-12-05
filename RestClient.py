# main.py
from Server.init import app
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5501",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:5502",
    ],  # Adjust this as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def runServer():
    try:
        uvicorn.run(app, port=8081)
    except Exception as ex:
        print(f"Error: {ex}")
