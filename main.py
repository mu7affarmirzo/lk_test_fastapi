from database import SessionLocal
from schemas import *
from services import *
from models import *

import schemas as sch


app = FastAPI()

SECRET_KEY = "98d8dd3f7f9132a8e68e4f0ee4a0d6ec46cb874f3d9962858c46ae234c1a1d9e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone_number: str = payload.get("sub")
        if phone_number is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = get_user_by_phone_number(db, phone_number)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return user


# Register a new user
@app.post("/register/", response_model=sch.User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_phone_number(db, user.phone_number)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return create_user(db, user)


# Token endpoint for user login
@app.post("/token/", response_model=sch.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: LoginForm = Depends()):
    user = authenticate_user(db, form_data.msisdn, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect phone number or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = get_access_token(db, user)
    print(access_token, '\n-------------\n')
    if access_token is None:
        access_token = 'NONE'

    return {"access_token": access_token, "token_type": "bearer"}


# Function to authenticate a user
def authenticate_user(db: Session, phone_number: str, password: str):
    user = get_user_by_phone_number(db, phone_number)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


# Endpoint for user profile
# @app.get("/profile/", response_model=User)
# async def get_user_profile(current_user: User = Depends(get_current_user)):
#     return current_user


# Function to get the current use

# Update user details
# @app.put("/profile/update/")
# async def update_user_profile(user_data: UserUpdate, db: Session = Depends(get_db, current_user: User = Depends(get_current_user))):
#     user = db.query(User).filter(User.id == current_user.id).first()
#     if user:
#         for key, value in user_data.dict().items():
#             setattr(user, key, value)
#         db.commit()
#         db.refresh(user)
#         return {"message": "Profile updated successfully"}
#     raise HTTPException(status_code=400, detail="User not found")


# Logout endpoint (if needed)
@app.post("/logout/", response_model=dict)
async def logout(current_user: User = Depends(get_current_user)):
    # Here you can implement any specific logic for logging out if needed
    return {"message": "Logged out successfully"}
