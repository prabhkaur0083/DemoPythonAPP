import os
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI()

# Root route
@app.get("/")
def read_root():
    return {"message new": "Welcome to your FastAPI app on Render! this is my first deployment testing with azure....."}

# Route with query parameters
@app.get("/greet/")
def greet_user(name: str = "Guest"):
    if os.getenv("VALUE"):
         return {"message": f"Hello, {name}!"}
    else:
        return {"message": f"No env find, {name}!"}


# Route with path parameters
@app.get("/items/{item_id}")
def read_item(item_id: int, details: bool = False):
    if details:
        return {"item_id": item_id, "description": f"Details for item {item_id}"}
    return {"item_id": item_id}

@app.get("/newitems/{item_id}")
def new_item(item_id: int, details: bool = False):
    if details:
        return {"new_item_id": item_id, "newdescription": f"Details for item {item_id}"}
    return {"item_id": item_id}

# Route for POST request
@app.post("/create/")
def create_item(name: str, description: str):
    return {"name": name, "description": description, "status": "created"}

# Run the app with Render's PORT environment variable
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to port 8000 if PORT is not set
    uvicorn.run(app)
