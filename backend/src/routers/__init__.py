from src.routers import auth
from src.routers import users
from src.routers import properties
from src.routers import bills
from src.routers import payments
from src.routers import repairs
from src.routers import visitors
from src.routers import complaints
from src.routers import notifications
from src.routers import work_orders
from src.routers import admins

__all__ = [
    "auth", "users", "properties", "bills", "payments",
    "repairs", "visitors", "complaints", "notifications",
    "work_orders", "admins"
]
