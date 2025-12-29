from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, model):
        json_schema = super().__get_pydantic_json_schema__(schema, model)
        json_schema = {'type': 'string'}
        return json_schema


# Database Models
class TaxScheme(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    item_name: str
    tax_percentage: float
    last_updated: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True


class PendingUpdate(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    detected_item: str
    current_db_val: float
    new_web_val: float
    evidence_pdf_path: str
    evidence_quote: str
    status: Literal["pending", "accepted", "rejected"] = "pending"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True


class AuditLog(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    action: str
    item_name: str
    old_value: float
    new_value: float
    timestamp: datetime = Field(default_factory=datetime.now)
    manager_id: Optional[str] = None

    class Config:
        populate_by_name = True


# API Request/Response Models
class UpdateAcceptRequest(BaseModel):
    accept: bool


class UpdateResponse(BaseModel):
    id: str
    detected_item: str
    current_db_val: float
    new_web_val: float
    evidence_pdf_path: str
    evidence_quote: str
    status: str
    created_at: datetime


class AnalysisResult(BaseModel):
    change_detected: bool
    item: Optional[str] = None
    new_val: Optional[float] = None
    quote: Optional[str] = None
