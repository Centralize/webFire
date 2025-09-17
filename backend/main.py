from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

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

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],  # Allows only the frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Authentication ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# TODO: Integrate a proper user management system (e.g., database) instead of hardcoded users.
# For now, authentication will fail as there are no users defined.


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication is temporarily disabled. Please implement a proper user management system.",
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
    # TODO: Replace with actual user retrieval from a database
    # For now, we'll just check if a username is present in the token
    if token_data.username is None:
        raise credentials_exception
    return {"username": token_data.username}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # TODO: Replace with actual user authentication from a database
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication is temporarily disabled. Please implement a proper user management system.",
        headers={"WWW-Authenticate": "Bearer"},
    )


# --- Endpoints ---

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/status", dependencies=[Depends(get_current_user)])
def get_status():
    return get_ufw_status()


@app.get("/api/rules", dependencies=[Depends(get_current_user)])
def get_rules():
    return get_ufw_rules()


@app.post("/api/rules", dependencies=[Depends(get_current_user)])
def add_rule(rule: Rule):
    return add_ufw_rule(rule)


@app.delete("/api/rules/{rule_id}", dependencies=[Depends(get_current_user)])
def delete_rule(rule_id: int):
    return delete_ufw_rule(rule_id)


@app.post("/api/enable", dependencies=[Depends(get_current_user)])
def enable():
    return enable_ufw()


@app.post("/api/disable", dependencies=[Depends(get_current_user)])
def disable():
    return disable_ufw()