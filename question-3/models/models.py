from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String, unique=True, index=True)
    data_entries = relationship("ProcessedData", back_populates="device")


class ProcessedData(Base):
    __tablename__ = "processed_data"
    id = Column(Integer, primary_key=True)
    data_id = Column(String, index=True)
    average_before_normalization = Column(Float)
    average_after_normalization = Column(Float)
    data_size = Column(Integer)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device", back_populates="data_entries")
