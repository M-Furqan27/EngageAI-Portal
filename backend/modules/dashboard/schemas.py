from pydantic import BaseModel
from typing import List



class DashboardSummary(BaseModel):
    total_leads: int
    new_leads: int
    contacted_leads: int
    qualified_leads: int
    lost_leads: int
    total_knowledge_sources: int
    active_employees: int
    inactive_employees: int


class LeadsOverTimePoint(BaseModel):
    date: str          # "2026-07-25"
    count: int


class LeadsOverTimeResponse(BaseModel):
    points: List[LeadsOverTimePoint]
    