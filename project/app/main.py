from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import predict, viz, dbroutes

from db_files import models, schemas
from db_files.database import SessionLocal, engine

app = FastAPI(
    title='Labs25-B2P-TeamC-DS',
    description='B2P DS API',
    version='0.1',
    docs_url='/',
)

app.include_router(predict.router)
app.include_router(viz.router)
app.include_router(dbroutes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
