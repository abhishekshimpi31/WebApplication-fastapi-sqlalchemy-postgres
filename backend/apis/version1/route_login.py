from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import JWTError, jwt


from db.session import get_db
from core.security import create_access_token
from core.hashing import Hasher
from db.repository.login import get_user
from core.config import settings

router = APIRouter()

def authenticate_user(username:str, password:str , db):
    user = get_user(username, db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_passwd(password, user.hashed_password):
        return False
    return user


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    access_token= create_access_token(data={"sub":user.email}, expires_delta=timedelta(settings.TIME_TO_EXPIRE))
    return {"access_token":access_token, 'token_type':'bearer'}


oauth_schema = OAuth2PasswordBearer(tokenUrl="/login/token")


def get_current_user_from_token(token:str = Depends(oauth_schema), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You are not authorise to create this Job")
    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            return credentials_exception
    except JWTError:
        return credentials_exception
    user = get_user(username=username, db =db)
    if user is None:
        return credentials_exception
    return user
    
