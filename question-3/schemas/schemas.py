from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DeviceBase(BaseModel):
    device_name: str

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    class Config:
        from_attributes = True


class ProcessedDataBase(BaseModel):
    data_id: str
    average_before_normalization: float
    average_after_normalization: float
    data_size: int
    created_date: datetime
    updated_date: datetime
    device_id: int

class ProcessedDataCreate(ProcessedDataBase):
    pass

class ProcessedData(ProcessedDataBase):
    id: int
    device: Device
    class Config:
        from_attributes = True
