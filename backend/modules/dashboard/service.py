from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from modules.leads.models import Lead
from modules.knowledge.models import KnowledgeBase
from modules.profile.user_model import User, UserRole, UserStatus



def get_summary(db: Session, organization_id):
    leads_query = db.query(Lead).filter(Lead.organization_id == organization_id)

    total_leads = leads_query.count()
    new_leads = leads_query.filter(Lead.status == "New").count()
    contacted_leads = leads_query.filter(Lead.status == "Contacted").count()
    qualified_leads = leads_query.filter(Lead.status == "Qualified").count()
    lost_leads = leads_query.filter(Lead.status == "Lost").count()


    total_knowledge_sources = (
        db.query(KnowledgeBase).filter(KnowledgeBase.organization_id == organization_id).count()
    )

    active_employees = (
        db.query(User)
        .filter(User.organization_id == organization_id, User.role != UserRole.Owner, User.status == UserStatus.Active)
        .count()
    )
    inactive_employees = (
        db.query(User)
        .filter(User.organization_id == organization_id, User.role != UserRole.Owner, User.status == UserStatus.Inactive)
        .count()
    )

    return {
        "total_leads": total_leads,
        "new_leads": new_leads,
        "contacted_leads": contacted_leads,
        "qualified_leads": qualified_leads,
        "lost_leads": lost_leads,
        "total_knowledge_sources": total_knowledge_sources,
        "active_employees": active_employees,
        "inactive_employees": inactive_employees,
    }


def get_leads_over_time(db: Session, organization_id, days: int = 30):
    """Pichle N dinon mein roz kitni leads aayi — chart ke liye."""
    since = datetime.utcnow() - timedelta(days=days)

    rows = (
        db.query(func.date(Lead.created_at).label("day"), func.count(Lead.id).label("count"))
        .filter(Lead.organization_id == organization_id, Lead.created_at >= since)
        .group_by(func.date(Lead.created_at))
        .order_by(func.date(Lead.created_at))
        .all()
    )

    data_by_day = {str(row.day): row.count for row in rows}

    # missing dinon ko 0 se fill karo taake chart mein gap na aaye
    points = []
    for i in range(days, -1, -1):
        day = (datetime.utcnow() - timedelta(days=i)).date()
        points.append({"date": str(day), "count": data_by_day.get(str(day), 0)})

    return points


