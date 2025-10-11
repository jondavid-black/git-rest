
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
	user_id: str

class Repository(BaseModel):
	repo_id: str
	name: str
	owner_user_id: str

class Branch(BaseModel):
	branch_id: str
	name: str
	repository_id: str

class File(BaseModel):
	file_id: str
	path: str
	repository_id: str
	branch_id: str
	owner_user_id: str

class AuditLog(BaseModel):
	log_id: str
	user_id: str
	action_type: str
	target_resource: str
	timestamp: datetime
	outcome: str
	retention: int = 365  # days
