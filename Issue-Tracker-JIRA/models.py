from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey

# In the DB task-jira this will be a table with name users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    username = Column(String, unique=True)
    name = Column(String)
    password_hash = Column(String)

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    priority = Column(String, nullable=False)
    status = Column (String)
    assigned_to = Column(Integer, ForeignKey("users.id"))  # Store ID
    