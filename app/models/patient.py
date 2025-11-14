"""Patient model for MongoDB."""

from typing import Optional
from pydantic import Field

from app.models.base import BaseModel


class Patient(BaseModel):
    """Patient model for storing patient information.

    Attributes:
        id: MongoDB ObjectId as string
        patient_id: 10-digit patient ID
        patient_name: Patient's full name
        emergency_name: Emergency contact name
        emergency_contact: 10-digit emergency contact number
        patient_discharge_summary: Patient discharge summary
        created_at: When the patient record was created
    """

    id: Optional[str] = Field(default=None, alias="_id")
    patient_id: str = Field(..., min_length=10, max_length=10)
    patient_name: str
    emergency_name: str
    emergency_contact: str = Field(..., min_length=10, max_length=10)
    patient_discharge_summary: str
