""" Titanic API """

from typing import List
from bson import ObjectId
from bson.errors import InvalidId

from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from core.config import title, version
from db.db import collection
from models.models import Person, PersonData


templates = Jinja2Templates(directory="./templates")

api = FastAPI(title=title, version=version)


@api.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    """Root path"""
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": title, "version": version}
    )


@api.get(
    "/people",
    response_description="Get a list of all people",
    response_model=List[Person],
)
async def get_all_people():
    """Get all people from the database."""
    persons = await collection.find().to_list(1000)
    return persons


@api.get(
    "/people/{uuid}",
    response_description="Get information about one person",
    response_model=Person,
)
async def get_person_by_uuid(uuid: str):
    """Get information about one person from the database by uuid."""
    try:
        if (person := await collection.find_one({"_id": ObjectId(uuid)})) is not None:
            return person
    except InvalidId:
        raise HTTPException(
            status_code=422,
            detail=(
                "Invalid uuid; uuid must be a 12-byte input or a 24-char hex string.")
            ,
        )
    raise HTTPException(status_code=404, detail=f'Person with uuid "{uuid}" not found.')


@api.post(
    "/people",
    response_description="Add a person to the database",
    response_model=Person,
    status_code=201,
)
async def add_person(
    person: PersonData = Body(...),
):
    """Add one person to the database."""

    person = jsonable_encoder(person)
    new_person = await collection.insert_one(person)
    if (
        created_person := await collection.find_one(
            {"_id": ObjectId(new_person.inserted_id)}
        )
    ) is not None:
        return created_person


@api.put(
    "/people/{uuid}",
    response_description="Update information about one person",
    response_model=Person,
    status_code=201,
)
async def update_person_by_uuid(
    uuid: str,
    person: PersonData = Body(...),
):
    """Update one person record in the database by _id."""
    person = jsonable_encoder(person)

    if len(person) >= 1:
        update_result = await collection.update_one(
            {"_id": ObjectId(uuid)}, {"$set": person}
        )

        if update_result.modified_count == 1:
            if (
                updated_result := await collection.find_one({"_id": ObjectId(uuid)})
            ) is not None:
                return updated_result

    if (
        existing_person := await collection.find_one({"_id": ObjectId(uuid)})
    ) is not None:
        return existing_person

    raise HTTPException(status_code=404, detail=f"Person with uuid {uuid} not found.")


@api.delete(
    "/people/{uuid}",
    response_description="Delete this person",
)
async def delete_person_by_uuid(uuid: str):
    """Delete one person from the database by uuid."""
    try:
        delete_person = await collection.delete_one({"_id": ObjectId(uuid)})
        if delete_person.deleted_count == 1:
            return JSONResponse(status_code=200, content="Person deleted.")
    except InvalidId:
        raise HTTPException(
            status_code=422,
            detail="Invalid uuid; uuid must be a 12-byte input or a 24-char hex string.",
        )
    raise HTTPException(status_code=404, detail=f"Person with uuid {uuid} not found.")
