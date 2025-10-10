# Built-in imports
import os
import sys
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "./src")))

# Third-party imports
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

# Local imports
from api.routes import user


app = FastAPI(title="IoT API")
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",          
        host=os.getenv("HOST"),        
        port=int(os.getenv("PORT")),
        reload=True             
    )