from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
class PillarBase(BaseModel):
    number: str
    title: str
    summary: str = ""
    description: str
    icon: str
    color: str
class PillarResponse(PillarBase):
    id: int
class PillarCreate(PillarBase):
    pass

class VisionMissionBase(BaseModel):
    slug: str
    title: str
    summary: str
    description: str
    icon: str
    color: str

class VisionMissionResponse(VisionMissionBase):
    id: int

class VisionMissionCreate(VisionMissionBase):
    pass

class ArchitectureLayerBase(BaseModel):
    layer_number: int
    title: str
    description: str
    icon: str
    color: str
    tags: list[str]
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

class ProjectResponse(BaseModel):
    id: int
    slug: str
    title: str
    summary: str
    full_description: str
    icon: str
    category: str
    status: str
    project_group: str

class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = "local"

class ChatResponse(BaseModel):
    response: str
