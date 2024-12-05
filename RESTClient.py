# main.py
from server.Init import app
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os


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
        port = int(os.getenv("PORT", 8081))  # Use the PORT environment variable
        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as ex:
        print(f"Error: {ex}")
