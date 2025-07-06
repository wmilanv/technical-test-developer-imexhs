from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from uuid import uuid4

def get_device_by_name(db: Session, name: str):
    return db.query(models.Device).filter(models.Device.device_name == name).first()

def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def create_processed_data(db: Session, data: schemas.ProcessedDataCreate):
    db_data = models.ProcessedData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_all_data(db: Session, filters: dict):
    query = db.query(models.ProcessedData)
    for key, value in filters.items():
        if "__gt" in key:
            field = key.replace("__gt", "")
            query = query.filter(getattr(models.ProcessedData, field) > value)
        elif "__lt" in key:
            field = key.replace("__lt", "")
            query = query.filter(getattr(models.ProcessedData, field) < value)
        else:
            query = query.filter(getattr(models.ProcessedData, key) == value)
    return query.all()

def get_data_by_id(db: Session, data_id: int):
    return db.query(models.ProcessedData).filter(models.ProcessedData.id == data_id).first()

def update_data(db: Session, data_id: int, update_data: dict):
    db_data = db.query(models.ProcessedData).filter(models.ProcessedData.id == data_id).first()
    if not db_data:
        return None
    for key, value in update_data.items():
        setattr(db_data, key, value)
    db_data.updated_date = datetime.now()
    db.commit()
    db.refresh(db_data)
    return db_data

def delete_data(db: Session, data_id: int):
    db_data = db.query(models.ProcessedData).filter(models.ProcessedData.id == data_id).first()
    if not db_data:
        return None
    db.delete(db_data)
    db.commit()
    return {"message": "Data deleted"}
