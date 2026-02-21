from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from get_recipes import router as get_recipes_router
from post_recipes import router as post_recipes_router

app.include_router(get_recipes_router)
app.include_router(post_recipes_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("frontend_hoster:app", host="0.0.0.0", port=8000, reload=True)
