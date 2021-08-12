from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Person(BaseModel):
    """Person Model"""

    uuid: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    survived: bool = Field(..., alias="Survived")
    passengerClass: int = Field(..., alias="Pclass")
    name: str = Field(..., alias="Name")
    sex: str = Field(..., alias="Sex")
    age: float = Field(..., alias="Age")
    siblingsOrSpousesAboard: int = Field(..., alias="Siblings/Spouses Aboard")
    parentsOrChildrenAboard: int = Field(..., alias="Parents/Children Aboard")
    fare: float = Field(..., alias="Fare")

    class Config:
        allow_population_by_field_name = False
        allow_population_by_alias = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "610b70c82a2fb60768158340",
                "Survived": False,
                "Pclass": 3,
                "Name": "Mr. Owen Harris Braund",
                "Sex": "male",
                "Age": "22",
                "Siblings/Spouses Aboard": "1",
                "Parents/Children Aboard": "0",
                "Fare": "7.25",
            }
        }


class PersonData(BaseModel):
    """PersonData Model"""

    survived: bool = Field(..., alias="Survived")
    passengerClass: int = Field(..., alias="Pclass")
    name: str = Field(..., alias="Name")
    sex: str = Field(..., alias="Sex")
    age: float = Field(..., alias="Age")
    siblingsOrSpousesAboard: int = Field(..., alias="Siblings/Spouses Aboard")
    parentsOrChildrenAboard: int = Field(..., alias="Parents/Children Aboard")
    fare: float = Field(..., alias="Fare")

    class Config:
        allow_population_by_field_name = False
        allow_population_by_alias = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "Survived": False,
                "Pclass": 3,
                "Name": "Mr. Owen Harris Braund",
                "Sex": "male",
                "Age": 22.0,
                "Siblings/Spouses Aboard": 1,
                "Parents/Children Aboard": 0,
                "Fare": 7.25,
            }
        }
