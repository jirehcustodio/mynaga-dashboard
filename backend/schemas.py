"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class TagCreate(BaseModel):
    """Schema for creating tags."""
    tag_name: str


class TagResponse(BaseModel):
    """Schema for tag responses."""
    id: int
    tag_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class CaseUpdateCreate(BaseModel):
    """Schema for creating case updates."""
    update_text: str
    updated_by: str
    status_after_update: Optional[str] = None


class CaseUpdateResponse(BaseModel):
    """Schema for case update responses."""
    id: int
    update_text: str
    updated_by: str
    update_timestamp: datetime
    status_after_update: Optional[str]

    class Config:
        from_attributes = True


class CaseCreate(BaseModel):
    """Schema for creating cases."""
    control_no: str
    category: str
    sender_location: Optional[str] = None
    cluster: Optional[str] = None  # Column D
    barangay: Optional[str] = None
    description: Optional[str] = None
    attached_media: Optional[str] = None
    reported_by: Optional[str] = None
    contact_number: Optional[str] = None
    office: Optional[str] = None  # Column I
    link_to_report: Optional[str] = None
    mynaga_app_status: Optional[str] = None  # Column M
    updates_sent_to_user_new: Optional[str] = None  # Column N
    refined_category: Optional[str] = None
    status: str = "OPEN"


class CaseUpdate(BaseModel):
    """Schema for updating cases."""
    category: Optional[str] = None
    cluster: Optional[str] = None  # Column D
    barangay: Optional[str] = None
    description: Optional[str] = None
    office: Optional[str] = None  # Column I
    mynaga_app_status: Optional[str] = None  # Column M
    updates_sent_to_user_new: Optional[str] = None  # Column N
    status: Optional[str] = None
    refined_category: Optional[str] = None
    office_progress_updates: Optional[str] = None


class CaseResponse(BaseModel):
    """Schema for case responses."""
    id: int
    control_no: str
    date_created: datetime
    category: str
    sender_location: Optional[str]
    cluster: Optional[str]  # Column D
    barangay: Optional[str]
    description: Optional[str]
    attached_media: Optional[str]  # Media URLs from MyNaga App
    office: Optional[str]  # Column I
    link_to_report: Optional[str]
    mynaga_app_status: Optional[str]  # Column M
    updates_sent_to_user_new: Optional[str]  # Column N (TEXT field)
    status: str
    reported_by: Optional[str]
    contact_number: Optional[str]
    tags: List[TagResponse] = []
    updates: List[CaseUpdateResponse] = []

    class Config:
        from_attributes = True


class OfficeCreate(BaseModel):
    """Schema for creating offices."""
    name: str
    code: Optional[str] = None
    location: Optional[str] = None
    contact_person: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None


class OfficeResponse(BaseModel):
    """Schema for office responses."""
    id: int
    name: str
    code: Optional[str]
    location: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


class ClusterCreate(BaseModel):
    """Schema for creating clusters."""
    name: str
    description: Optional[str] = None
    barangay: Optional[str] = None
    color: str = "#3B82F6"
    created_by: str


class ClusterUpdate(BaseModel):
    """Schema for updating clusters."""
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None


class ClusterResponse(BaseModel):
    """Schema for cluster responses."""
    id: int
    name: str
    description: Optional[str]
    barangay: Optional[str]
    color: str
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    """Schema for statistics."""
    total_cases: int
    open_cases: int
    resolved_cases: int
    rerouting_cases: int
    total_offices: int
    total_clusters: int
    average_case_aging: float
