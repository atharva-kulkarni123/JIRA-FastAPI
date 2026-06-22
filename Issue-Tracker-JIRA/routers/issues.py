from fastapi import Depends, HTTPException, APIRouter
from database import get_db
from schemas import CreateIssue, IssueResponse
from sqlalchemy.orm import Session
import models
from auth import get_current_user

router = APIRouter(prefix="/issues", tags=["issues"])

@router.get("/issues", response_model=list[IssueResponse])
def get_all_issues(current_user = Depends(get_current_user), db: Session=Depends(get_db)):
    return db.query(models.Issue).all()  

@router.post("/create")
def  create_issue(issue: CreateIssue, current_user = Depends(get_current_user) , db: Session=Depends(get_db)):
    user = db.query(models.User).filter(issue.assigned_to == models.User.name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_issue = models.Issue(
        title = issue.title,
        description = issue.description,
        priority = issue.priority,
        status = issue.status,
        assigned_to = user.id,
        created_by = current_user.id
    )
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return new_issue