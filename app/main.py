from fastapi import FastAPI
from .database import engine, Base
from .routes import router

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
