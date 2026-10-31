from routers.freshness_detector import router as freshness_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.hygiene_monitor import router as hygiene_router
from routers.meal_planner import router as meal_planner_router
from routers.kitchen_assistant import router as kitchen_router
from routers.food_recognition import router as food_router


app = FastAPI(
    title="Food Verse AI",
    description="Multimodal AI-powered Food Intelligence Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(food_router)
app.include_router(freshness_router)
app.include_router(hygiene_router)
app.include_router(meal_planner_router)
app.include_router(kitchen_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Food Verse AI",
        "status": "Running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
