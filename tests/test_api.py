import pytest
import asyncio
from httpx import AsyncClient
from bson import ObjectId

from main import api


base_url = "http://localhost:8000/"
test_person = {
    "Survived": False,
    "Pclass": 1,
    "Name": "Mr. Tester",
    "Sex": "male",
    "Age": 26.0,
    "Siblings/Spouses Aboard": 0,
    "Parents/Children Aboard": 0,
    "Fare": 15.25,
}
test_invalid_person = {
    "Survived": "Invalid",
    "Pclass": 1,
    "Name": "Mr. Invalid",
    "Sex": "male",
    "Age": 26.0,
    "Siblings/Spouses Aboard": 0,
    "Parents/Children Aboard": 0,
    "Fare": 15.25,
}


@pytest.mark.asyncio
async def test_root():
    """Test if root view is available"""
    async with AsyncClient(app=api, base_url=base_url) as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    assert "<title>Titanic API</title>" in response.text


@pytest.mark.asyncio
async def test_docs():
    """Test if automatically generated documentation is available"""
    async with AsyncClient(app=api, base_url=base_url) as ac:
        response = await ac.get("/docs")

    assert response.status_code == 200
    assert "Titanic Passengers API" in response.text


@pytest.mark.asyncio
async def test_alt_docs():
    """Test if automatically generated documentation is available"""
    async with AsyncClient(app=api, base_url=base_url) as ac:
        response = await ac.get("/redoc")

    assert response.status_code == 200
    assert "Titanic Passengers API" in response.text


@pytest.mark.asyncio
async def test_add_person():
    """Verify we can create a new person entry"""
    async with AsyncClient(app=api, base_url=base_url) as ac:
        response = await ac.post("/people", json=test_person)

    assert response.status_code == 201
    assert test_person.items() <= response.json().items()


@pytest.mark.asyncio
async def test_add_invalid_person():
    """Verify we can't create an invalid person entry"""
    async with AsyncClient(app=api, base_url=base_url) as ac:
        response = await ac.post("/people", json=test_invalid_person)

    assert response.status_code == 422
    assert "type_error" in response.json()["detail"][0]["type"]


@pytest.mark.asyncio
async def test_get_all_people():
    """Verify we can get all entries"""
    async with AsyncClient(app=api, base_url=base_url) as ac:
        response = await ac.get("/people")

    assert response.status_code == 200
    assert test_person.keys() <= response.json()[0].keys()


@pytest.mark.asyncio
async def test_get_person_by_uuid():
    """Verify we can find an entry by uuid"""
    async with AsyncClient(app=api, base_url=base_url) as ac:
        response = await ac.get("/people")

    uuid = response.json()[0]["_id"]
    uuid = ObjectId(uuid)

    async with AsyncClient(app=api, base_url=base_url) as ac:
        response = await ac.get(f"/people/{uuid}")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_person_by_invalid_uuid():
    """Verify we can't use invalid uuid"""
    async with AsyncClient(app=api, base_url=base_url) as ac:
        response = await ac.get("/people/invalid")

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Invalid uuid; uuid must be a 12-byte input or a 24-char hex string."
    }


@pytest.mark.asyncio
async def test_delete_person_by_uuid():
    """Verify we can delete person entry"""
    async with AsyncClient(app=api, base_url=base_url) as ac:
        response = await ac.get("/people")

    uuid = response.json()[0]["_id"]
    uuid = ObjectId(uuid)

    async with AsyncClient(app=api, base_url=base_url) as ac:
        response = await ac.delete(f"/people/{uuid}")

    assert response.status_code == 200
    assert "Person deleted." in response.json()


@pytest.mark.asyncio
async def test_delete_person_by_invalid_uuid():
    """Verify we can't use invalid uuid to delete person entry"""
    async with AsyncClient(app=api, base_url=base_url) as ac:
        response = await ac.delete(f"/people/invalid")

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Invalid uuid; uuid must be a 12-byte input or a 24-char hex string."
    }
