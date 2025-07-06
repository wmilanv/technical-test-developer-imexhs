from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import logging
import json
from datetime import datetime
from uuid import uuid4

from . import models, schemas, crud, database

# Setup logging
logging.basicConfig(filename='api_requests.log', level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Medical Image Processing API")

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/elements/", response_model=List[schemas.ProcessedData])
def create_elements(payload: Dict[str, Dict[str, Any]], db: Session = Depends(get_db)):
    results = []
    for key in payload:
        entry = payload[key]
        data_str = ' '.join(entry['data']).split()
        try:
            values = [float(num) for num in data_str]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid data format. All values must be numbers.")

        max_val = max(values)
        normalized = [v / max_val for v in values]

        avg_before = sum(values) / len(values)
        avg_after = sum(normalized) / len(normalized)
        size = len(values)

        device_name = entry.get("deviceName", "Unknown")
        device = crud.get_device_by_name(db, device_name)
        if not device:
            device = crud.create_device(db, schemas.DeviceCreate(device_name=device_name))

        data_entry = schemas.ProcessedDataCreate(
            data_id=entry.get("id", f"default_{uuid4()}"),
            average_before_normalization=avg_before,
            average_after_normalization=avg_after,
            data_size=size,
            created_date=datetime.now(),
            updated_date=datetime.now(),
            device_id=device.id
        )
        result = crud.create_processed_data(db, data_entry)
        results.append(result)
    logger.info(f"POST /api/elements/ - Payload: {json.dumps(payload)} - Result: {len(results)} entries created")
    return results

@app.get("/api/elements/", response_model=List[schemas.ProcessedData])
def read_elements(
    db: Session = Depends(get_db),
    data_id: Optional[int] = None,
    data_id__gt: Optional[int] = None,
    data_id__lt: Optional[int] = None,
    data_size: Optional[int] = None,
    data_size__gt: Optional[int] = None,
    data_size__lt: Optional[int] = None,
    average_before_normalization: Optional[float] = None,
    average_before_normalization__gt: Optional[float] = None,
    average_before_normalization__lt: Optional[float] = None,
    average_after_normalization: Optional[float] = None,
    average_after_normalization__gt: Optional[float] = None,
    average_after_normalization__lt: Optional[float] = None,
    created_date: Optional[datetime] = None,
    updated_date: Optional[datetime] = None
):
    filters = {
        k: v for k, v in locals().items() if v is not None and k != "db"
    }
    logger.info(f"GET /api/elements/ - Filters: {filters}")
    return crud.get_all_data(db, filters)

@app.get("/api/elements/{data_id}", response_model=schemas.ProcessedData)
def read_element(data_id: int, db: Session = Depends(get_db)):
    db_data = crud.get_data_by_id(db, data_id)
    if not db_data:
        raise HTTPException(status_code=404, detail="Entry not found")
    logger.info(f"GET /api/elements/{data_id} - Found")
    return db_data

@app.put("/api/elements/{data_id}", response_model=schemas.ProcessedData)
def update_element(data_id: int, payload: dict, db: Session = Depends(get_db)):
    db_data = crud.get_data_by_id(db, data_id)
    if not db_data:
        raise HTTPException(status_code=404, detail="Entry not found")
    updated = crud.update_data(db, data_id, payload)
    logger.info(f"PUT /api/elements/{data_id} - Updated with {payload}")
    return updated

@app.delete("/api/elements/{data_id}")
def delete_element(data_id: int, db: Session = Depends(get_db)):
    result = crud.delete_data(db, data_id)
    logger.info(f"DELETE /api/elements/{data_id} - Deleted")
    return result