"""Patient schemas for request/response validation."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator


class PatientBase(BaseModel):
    """Base patient schema with common fields."""

    patient_id: str = Field(..., min_length=10, max_length=10, description="10-digit patient ID")
    patient_name: str = Field(..., min_length=1, max_length=200, description="Patient's full name")
    patient_email: str = Field(..., min_length=1, max_length=200, description="Patient's email")
    emergency_name: str = Field(..., min_length=1, max_length=200, description="Emergency contact name")
    emergency_contact: str = Field(..., min_length=10, max_length=10, description="10-digit emergency contact number")
    patient_discharge_summary: Dict[str, Any] = Field(default_factory=dict, description="Patient discharge summary object")
    bill_details: List[Dict[str, Any]] = Field(default_factory=list, description="Array of billing details")
    medication_details: List[Dict[str, Any]] = Field(default_factory=list, description="Array of medication details")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="Array of previous conversation messages")
    conversation_summary: str = Field(default="", description="Summary of conversations")
    appointment_followup: List[Dict[str, Any]] = Field(default_factory=list, description="Array of appointment follow-up details")

    @field_validator("patient_id", "emergency_contact")
    @classmethod
    def validate_numeric_string(cls, v: str, info) -> str:
        """Validate that the string contains only digits."""
        if not v.isdigit():
            raise ValueError(f"{info.field_name} must contain only digits")
        return v


class PatientCreate(PatientBase):
    """Schema for creating a new patient."""

    pass


class PatientUpdate(BaseModel):
    """Schema for updating a patient."""

    patient_name: Optional[str] = Field(None, min_length=1, max_length=200)
    patient_email: Optional[str] = Field(None, min_length=1, max_length=200)
    emergency_name: Optional[str] = Field(None, min_length=1, max_length=200)
    emergency_contact: Optional[str] = Field(None, min_length=10, max_length=10)
    patient_discharge_summary: Optional[Dict[str, Any]] = None
    bill_details: Optional[List[Dict[str, Any]]] = None
    medication_details: Optional[List[Dict[str, Any]]] = None
    messages: Optional[List[Dict[str, Any]]] = None
    conversation_summary: Optional[str] = None
    appointment_followup: Optional[List[Dict[str, Any]]] = None

    @field_validator("emergency_contact")
    @classmethod
    def validate_emergency_contact(cls, v: Optional[str]) -> Optional[str]:
        """Validate emergency contact if provided."""
        if v is not None and not v.isdigit():
            raise ValueError("emergency_contact must contain only digits")
        return v


class PatientResponse(PatientBase):
    """Schema for patient response."""

    id: str = Field(..., alias="_id", description="MongoDB ObjectId")

    class Config:
        """Pydantic config."""
        populate_by_name = True
        json_encoders = {
            str: str
        }
