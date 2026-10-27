from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
STATUSES={"Submitted","Under Review","Assigned","In Progress","Resolved","Rejected","Reopened"}
class ComplaintCreate(BaseModel):
    title:str=Field(min_length=3,max_length=160)
    category:str=Field(default="General",max_length=60)
    location:str=Field(default="Jaipur",max_length=160)
    description:str=Field(default="",max_length=3000)
    priority:str=Field(default="Medium",pattern="^(Low|Medium|High|Urgent)$")
class ComplaintUpdate(BaseModel):
    status:str|None=None
    department:str|None=Field(default=None,max_length=80)
    priority:str|None=Field(default=None,pattern="^(Low|Medium|High|Urgent)$")
class ComplaintOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; title:str; category:str; location:str; description:str; status:str; department:str; priority:str; created_at:datetime
