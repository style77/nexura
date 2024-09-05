from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import dotenv

dotenv.load_dotenv("../.env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.add_api_route("{provider}/{endpoint}")
