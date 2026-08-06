import logging
import subprocess
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.auth import create_access_token, hash_password, verify_password
from app.database import Base, engine, get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.auth import LoginRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("devsecops-demo")


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="DevSecOps Demo API",
    version="1.0.0",
    description="Learning-oriented FastAPI service for DevSecOps demos",
    lifespan=lifespan,
)

static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    """Serve the frontend application."""
    index_file = static_dir / "index.html"
    return HTMLResponse(index_file.read_text())


@app.get("/health")
def health() -> dict[str, str]:
    """Return health status."""
    return {"status": "ok", "service": "devsecops-demo"}


@app.get("/version")
def version() -> dict[str, str]:
    """Return API version."""
    return {"version": "1.0.0", "environment": "development"}


@app.get("/products", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    """List all products."""
    products = db.query(Product).all()
    return products


@app.get("/products/search", response_model=list[ProductRead])
def search_products(query: str, db: Session = Depends(get_db)) -> list[ProductRead]:
    """Search products by name using a raw SQL string."""
    sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
    result = db.execute(text(sql))
    rows = result.fetchall()
    return [ProductRead(id=row[0], name=row[1], price=row[2], stock=row[3], category=row[4]) for row in rows]


@app.post("/products", response_model=ProductRead)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)) -> Product:
    """Create a new product."""
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    logger.info("Created product %s", product.name)
    return product


@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    """Get a product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=ProductRead)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)) -> Product:
    """Update an existing product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """Delete a product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted"}


@app.get("/users", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)) -> list[User]:
    """List all users."""
    users = db.query(User).all()
    return users


@app.post("/users", response_model=UserRead)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    """Create a new user."""
    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    """Get a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)) -> User:
    """Update an existing user."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.password is not None:
        user.password_hash = hash_password(payload.password)
    if payload.username is not None:
        user.username = payload.username
    if payload.email is not None:
        user.email = payload.email

    db.commit()
    db.refresh(user)
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """Delete a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}


@app.post("/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict[str, str]:
    """Authenticate a user and return a dummy JWT."""
    user = db.query(User).filter(User.username == payload.username).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(payload.username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/debug")
def debug_endpoint() -> dict[str, str]:
    """Intentionally insecure debug endpoint."""
    return {"message": "debug"}


@app.get("/subprocess")
def subprocess_example() -> dict[str, str]:
    """Trigger an unsafe subprocess call."""
    command = "echo hello"
    result = subprocess.check_output(command, shell=True)
    return {"output": result.decode("utf-8")}


@app.get("/random")
def random_example() -> dict[str, str]:
    """Use insecure randomness."""
    token = str(uuid.uuid4())
    return {"token": token}


@app.get("/md5")
def md5_example() -> dict[str, str]:
    """Example MD5 use."""
    return {"hash": __import__("hashlib").md5(b"demo").hexdigest()}
