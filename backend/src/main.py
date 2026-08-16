from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.database import init_db, close_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="Property Management System API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting application...")
    await init_db()
    logger.info("Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")
    await close_db()
    logger.info("Application shut down")


@app.get("/")
async def root():
    return {"message": "Welcome to Property Management System API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Import routers here to avoid circular imports
from src.routers import auth, users, properties, bills, payments, repairs, visitors, complaints, notifications, work_orders, admins, uploads, import_router

# Static files
from fastapi.staticfiles import StaticFiles
import os
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(properties.router, prefix="/api/v1/properties", tags=["Properties"])
app.include_router(bills.router, prefix="/api/v1/bills", tags=["Bills"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])
app.include_router(repairs.router, prefix="/api/v1/repairs", tags=["Repairs"])
app.include_router(visitors.router, prefix="/api/v1/visitors", tags=["Visitors"])
app.include_router(complaints.router, prefix="/api/v1/complaints", tags=["Complaints"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(work_orders.router, prefix="/api/v1/work-orders", tags=["Work Orders"])
app.include_router(admins.router, prefix="/api/v1/admins", tags=["Admin"])
app.include_router(uploads.router, tags=["Uploads"])
app.include_router(import_router.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
