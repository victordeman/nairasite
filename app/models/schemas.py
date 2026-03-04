from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class PillarBase(BaseModel):
    number: str
    title: str
    description: str
    icon: str
    color: str

class PillarResponse(PillarBase):
    id: int

class PillarCreate(PillarBase):
    pass

class ArchitectureLayerBase(BaseModel):
    layer_number: int
    title: str
    description: str
    icon: str
    color: str
    tags: List[str]

class ArchitectureLayerResponse(ArchitectureLayerBase):
    id: int

class ArchitectureLayerCreate(ArchitectureLayerBase):
    pass

class RevenueStreamBase(BaseModel):
    title: str
    description: str
    icon: str
    color: str

class RevenueStreamResponse(RevenueStreamBase):
    id: int

class RevenueStreamCreate(RevenueStreamBase):
    pass

class ProjectBase(BaseModel):
    title: str
    description: str
    icon: str
    category: str
    status: str

class ProjectResponse(ProjectBase):
    id: int

class ContactSubmission(BaseModel):
    name: str
    email: str
    role: str = ""
    message: str

class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    message: str
    created_at: str

class NewsletterSubscription(BaseModel):
    email: str

class NewsletterResponse(BaseModel):
    id: int
    email: str
    created_at: str

class StatsResponse(BaseModel):
    pillars_count: int
    architecture_layers_count: int
    xr_label: str
    ai_label: str

class MessageResponse(BaseModel):
    message: str
    success: bool = True
