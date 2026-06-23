from fastapi import Depends, HTTPException
from database import get_db
import models
from schemas import CreateIssue
from auth import get_current_user
from sqlalchemy.orm import Session

def create_issue(issue: CreateIssue, current_user_id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(issue.assigned_to == models.User.name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_issue = models.Issue(
        title = issue.title,
        description = issue.description,
        priority = issue.priority,
        status = issue.status,
        assigned_to = user.id,
        created_by = current_user_id
    )
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return new_issue