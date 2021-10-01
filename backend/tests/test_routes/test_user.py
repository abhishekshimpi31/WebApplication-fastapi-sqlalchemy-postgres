import json


def test_create_user(client):
    data = {"full_name": "user1",
            "email": "user1@example.com",
            "contact_number": "538579817597",
            "password": "password",
            "location": "pune",
            "created_by": "user1",
            "created_on": "2021-09-18",
            "updated_by": "user1",
            "updated_on": "2021-09-18"}
    response = client.post("/user/user", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "user1@example.com"
    assert response.json()["is_active"] == True
