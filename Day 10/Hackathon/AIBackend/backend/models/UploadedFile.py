from beanie import Document, Indexed, PydanticObjectId
from datetime import datetime, timezone
from pydantic import Field
from bson import ObjectId
from typing import Optional

class UploadedFile(Document):
    user_id: Optional[PydanticObjectId] = None
    filename: str
    file_type: str
    file_size: int
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    file_path: str
    processed: bool = False
    
    class Settings:
        name = "uploaded_files"
    
    # class Config:
    #     validate_by_name = True
    #     allow_population_by_field_name = True
    #     arbitrary_types_allowed = True
    #     json_encoders = {ObjectId: str}