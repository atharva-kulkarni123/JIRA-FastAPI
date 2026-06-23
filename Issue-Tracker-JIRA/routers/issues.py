from fastapi import Depends, HTTPException, APIRouter
from database import get_db
from schemas import CreateIssue, IssueResponse
from sqlalchemy.orm import Session
import models
from auth import get_current_user
from services import issue_service

router = APIRouter(prefix="/issues", tags=["issues"])

@router.get("/issues", response_model=list[IssueResponse])
def get_all_issues(current_user = Depends(get_current_user), db: Session=Depends(get_db)):
    return db.query(models.Issue).all()  

@router.post("/create")
def create_issue(issue: CreateIssue, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return issue_service.create_issue(issue, current_user.id, db)


