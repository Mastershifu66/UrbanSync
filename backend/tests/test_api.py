import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():
    r=client.get("/api/health"); assert r.status_code==200 and r.json()["status"]=="healthy"
def test_create_complaint():
    r=client.post("/api/complaints",json={"title":"Test broken streetlight","category":"Electricity","location":"Test Road","description":"API test","priority":"Medium"})
    assert r.status_code==201 and r.json()["title"]=="Test broken streetlight"
def test_role_protection():
    r=client.patch("/api/complaints/1",json={"status":"Resolved"},headers={"X-Role":"Citizen"}); assert r.status_code==403
