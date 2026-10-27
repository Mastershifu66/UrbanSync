from fastapi import FastAPI, Depends, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from .database import Base, engine, get_db
from .models import Complaint
from .schemas import ComplaintCreate, ComplaintUpdate, ComplaintOut, STATUSES
app=FastAPI(title="UrbanSync API",version="1.0.0",description="Smart City Integrated Management Platform — demo API")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
Base.metadata.create_all(bind=engine)
SEED=[("Streetlight not working","Electricity","MI Road, Jaipur","Streetlight near the crossing has been off for two nights.","In Progress","Electrical","High"),("Garbage collection missed","Waste Management","Mansarovar, Jaipur","Collection was missed on the scheduled day.","Submitted","Sanitation","Medium"),("Water leakage on road","Water Supply","Vaishali Nagar, Jaipur","Water is pooling near the footpath.","Assigned","Water Works","Urgent"),("Pothole repair request","Roads","Malviya Nagar, Jaipur","Large pothole needs attention.","Resolved","Roads & Transport","Medium"),("Traffic signal timing","Traffic","Tonk Road, Jaipur","Signal cycle is causing a long queue.","Under Review","Traffic Management","Low")]
def seed(db):
    if not (db.scalar(select(func.count(Complaint.id))) or 0):
        for title,category,location,description,status,department,priority in SEED: db.add(Complaint(title=title,category=category,location=location,description=description,status=status,department=department,priority=priority))
        db.commit()
@app.on_event("startup")
def startup():
    db=next(get_db())
    try: seed(db)
    finally: db.close()
@app.get("/")
def root(): return {"name":"UrbanSync","tagline":"One City. Everything Connected.","status":"running","docs":"/docs"}
@app.get("/api/health")
def health(): return {"status":"healthy","service":"UrbanSync API"}
@app.get("/api/complaints",response_model=list[ComplaintOut])
def list_complaints(status:str|None=Query(default=None),category:str|None=Query(default=None),search:str|None=Query(default=None,max_length=120),db:Session=Depends(get_db)):
    q=select(Complaint).order_by(Complaint.id.desc())
    if status: q=q.where(Complaint.status==status)
    if category: q=q.where(Complaint.category==category)
    if search:
        term=f"%{search.strip()}%"; q=q.where((Complaint.title.ilike(term))|(Complaint.location.ilike(term))|(Complaint.description.ilike(term)))
    return list(db.scalars(q).all())
@app.post("/api/complaints",response_model=ComplaintOut,status_code=201)
def create_complaint(payload:ComplaintCreate,db:Session=Depends(get_db)):
    item=Complaint(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
@app.patch("/api/complaints/{item_id}",response_model=ComplaintOut)
def update_complaint(item_id:int,payload:ComplaintUpdate,db:Session=Depends(get_db),x_role:str=Header(default="Citizen")):
    if x_role not in {"Municipal Administrator","Municipal Staff"}: raise HTTPException(status_code=403,detail="Only municipal staff or administrators can update complaints.")
    item=db.get(Complaint,item_id)
    if not item: raise HTTPException(status_code=404,detail="Complaint not found")
    changes=payload.model_dump(exclude_unset=True)
    if changes.get("status") and changes["status"] not in STATUSES: raise HTTPException(status_code=422,detail="Invalid complaint status")
    for key,value in changes.items(): setattr(item,key,value)
    db.commit(); db.refresh(item); return item
@app.get("/api/analytics")
def analytics(db:Session=Depends(get_db)):
    total=db.scalar(select(func.count(Complaint.id))) or 0
    rows=db.execute(select(Complaint.status,func.count(Complaint.id)).group_by(Complaint.status)).all()
    cats=db.execute(select(Complaint.category,func.count(Complaint.id)).group_by(Complaint.category)).all()
    resolved=sum(n for s,n in rows if s=="Resolved")
    return {"total_complaints":total,"resolved":resolved,"open":total-resolved,"resolution_rate":round(resolved/total*100) if total else 0,"by_status":[{"status":s,"count":n} for s,n in rows],"by_category":[{"category":c,"count":n} for c,n in cats]}
@app.get("/api/modules")
def modules():
    return [{"name":n,"status":s} for n,s in [("Citizen Services","Operational"),("Complaint Management","Operational"),("Municipal Operations","Operational"),("Smart Infrastructure","Simulated data"),("Emergency Response","Demo only"),("Healthcare Integration","Directory demo"),("Analytics & Reporting","Operational"),("Administration","Demo controls")]]
