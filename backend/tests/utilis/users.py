from sqlalchemy.orm import Session
import random
import string

from db.schemas.user import UserCreate
from db.repository.user import create_user



from db.repository.login import get_user
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase,k=32))


def create_random_owner(db:Session):
    email = f"{random_lower_string()}@{random_lower_string()}.com"
    password = random_lower_string()
    full_name = random_lower_string()
    location = random_lower_string()
    created_by = random_lower_string()
    updated_by = random_lower_string()
    contact_number = "3215698198453168"
    user_schema = UserCreate(username = email,email=email,password=password, full_name=full_name, location=location,
                                created_by=created_by, updated_by=updated_by, contact_number=contact_number)
    user = create_user(user= user_schema,db = db)
    return user

def user_authentication_headers(client: TestClient, email: str, password: str):      #new
    data = {"username": email, "password": password}
    r = client.post("/login/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):        #new
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = "random-passW0rd"
    full_name = random_lower_string()
    location = random_lower_string()
    created_by = random_lower_string()
    updated_by = random_lower_string()
    contact_number = "3215698198453168"
    user = get_user(username=email, db=db)
    if not user:
        user_in_create = UserCreate(username=email, email=email, password=password, full_name=full_name, location=location,
                                created_by=created_by, updated_by=updated_by, contact_number=contact_number)
        user = create_user(user=user_in_create, db=db)
    return user_authentication_headers(client=client, email=email, password=password)
