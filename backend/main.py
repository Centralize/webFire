from datetime import timedelta
from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel, Field, ConfigDict

from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    Token,
    TokenData,
    create_access_token,
    get_password_hash,
    verify_password,
)
from ufw_service import (
    get_ufw_status,
    get_ufw_rules,
    add_ufw_rule,
    delete_ufw_rule,
    enable_ufw,
    disable_ufw,
    Rule,
)

tags_metadata = [
    {"name": "Health", "description": "Service health and readiness checks."},
    {"name": "Auth", "description": "Authentication and access token issuance."},
    {"name": "UFW", "description": "Firewall status and rule management endpoints."},
]

app = FastAPI(
    title="webFire API",
    description="API for managing UFW (Uncomplicated Firewall).",
    version="0.1.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# --- Schemas for OpenAPI/Swagger ---
class HealthResponse(BaseModel):
    service: str = Field(example="webFire API")
    status: str = Field(example="ok")


class StatusResponse(BaseModel):
    status: str = Field(description="UFW status: active | inactive | unknown | error")
    message: Optional[str] = Field(default=None, description="Optional error or info message")


class RuleOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: int
    to: str
    action: str
    direction: str = ""
    from_: str = Field(default="", alias="from")


class RulesResponse(BaseModel):
    status: str
    rules: List[RuleOut] = []


class OperationResult(BaseModel):
    status: str
    message: Optional[str] = None


# --- Health Check ---
@app.get(
    "/",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Service health check",
    description="Returns a simple payload indicating the API is running.",
)
def health_check():
    return {"service": "webFire API", "status": "ok"}

# CORS Middleware — allow dev (Vite) and Nginx hosts
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:4280",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

 

# --- Minimal Dev Authentication ---
# In-memory user store for development. Replace with DB-backed users for production.
fake_users_db = {
    "admin": {
        "username": "admin",
        # default password: "secret" (change in production)
        "hashed_password": get_password_hash("secret"),
    }
}


def get_user(db, username: str) -> Optional[dict]:
    return db.get(username)


def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = get_user(fake_users_db, username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


# Use /api/token to align with Nginx proxy prefix
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)  # type: ignore[arg-type]
    if user is None:
        raise credentials_exception
    return user


@app.post("/api/token", response_model=Token, tags=["Auth"], summary="Issue access token")
@app.post("/token", response_model=Token, include_in_schema=False)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- Endpoints ---
@app.get(
    "/api/status",
    response_model=StatusResponse,
    dependencies=[Depends(get_current_user)],
    tags=["UFW"],
    summary="Get UFW status",
)
def get_status():
    return get_ufw_status()


@app.get(
    "/api/rules",
    response_model=RulesResponse,
    dependencies=[Depends(get_current_user)],
    tags=["UFW"],
    summary="List UFW rules",
    description="Returns UFW rules with numbered IDs for stable delete operations.",
)
def get_rules():
    return get_ufw_rules()


@app.post(
    "/api/rules",
    response_model=OperationResult,
    dependencies=[Depends(get_current_user)],
    tags=["UFW"],
    summary="Add a UFW rule",
)
def add_rule(rule: Rule):
    return add_ufw_rule(rule)


@app.delete(
    "/api/rules/{rule_id}",
    response_model=OperationResult,
    dependencies=[Depends(get_current_user)],
    tags=["UFW"],
    summary="Delete a UFW rule by ID",
)
def delete_rule(rule_id: int):
    return delete_ufw_rule(rule_id)


@app.post(
    "/api/enable",
    response_model=OperationResult,
    dependencies=[Depends(get_current_user)],
    tags=["UFW"],
    summary="Enable UFW",
)
def enable():
    return enable_ufw()


@app.post(
    "/api/disable",
    response_model=OperationResult,
    dependencies=[Depends(get_current_user)],
    tags=["UFW"],
    summary="Disable UFW",
)
def disable():
    return disable_ufw()
