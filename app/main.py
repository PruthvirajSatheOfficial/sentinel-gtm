from fastapi import FastAPI
from app.routers import accounts, buying_intents, outreach_briefs
from app.db.database import Base, engine

# Create tables if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SentinelGTM API", version="1.0")

app.include_router(accounts.router)
app.include_router(buying_intents.router)
app.include_router(outreach_briefs.router)

@app.get("/")
def root():
    return {"status": "SentinelGTM Engine Online"}