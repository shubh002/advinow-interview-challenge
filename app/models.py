from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint, and_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime
from dotenv import load_dotenv
import os, sys, os.path
sys.path.append('/root/job_assesments/advinow-interview-challenge')
#change the system path accordingly (to root folder)
import settings

Base = declarative_base()

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/postgres"

SQLALCHEMY_DATABASE_URL = settings.DB_URL

#SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class to handle database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Business(Base):
    __tablename__ = "business"

    business_id = Column(Integer)
    business_name = Column(String(100))
    symptom_code = Column(String(100), ForeignKey('symptom.symptom_code'))
    
    __table_args__ = (
        PrimaryKeyConstraint('business_id', 'symptom_code'),
    )

class Symptom(Base): 
    __tablename__ = "symptom"

    symptom_code = Column(String(100), primary_key=True)
    symptom_name = Column(String(100))
    symptom_diagnostic = Column(Boolean, unique=False, default=True)


class BusinessDataLoader():
    def __init__(self):
        self.db = SessionLocal()
        self.session = SessionLocal()
        self.column_positions = {
            'Business ID' : 0,
            'Business Name' : 1,
            'Symptom Code' : 2,
            'Symptom Name' : 3 , 
            'Symptom Diagnostic' : 4
        }
        self.true_variants = ["yes", "true"]

    def update(self, csv_data):
        sucessfully_update = self.update_col_positions(csv_data[0])
        business_data, symptom_data = self.build_data_objs(csv_data)
        for business_row, symptom_row in zip(business_data, symptom_data):
            # print(business_row.business_id, symptom_row.symptom_code)
            if not self.session.query(Symptom).filter(Symptom.symptom_code == symptom_row.symptom_code).first():
                self.db.add(symptom_row)
                self.db.commit()
            if not self.session.query(Business).filter(and_(Business.business_id == business_row.business_id, Business.symptom_code == business_row.symptom_code)).all():
                self.db.add(business_row)
                self.db.commit()
            
            
        print("database updated successfully")
        
    
    def build_data_objs(self, csv_data):
        business_data = []
        symptom_data = []
        if len(csv_data) > 1:
            for row in csv_data[1:]:
                business_data.append(Business(
                    business_id = int(row[self.column_positions["Business ID"]]),
                    business_name = row[self.column_positions["Business Name"]],
                    symptom_code = row[self.column_positions["Symptom Code"]],
                ))
                
                symptom_data.append(Symptom(
                    symptom_code = row[self.column_positions["Symptom Code"]],
                    symptom_name = row[self.column_positions["Symptom Name"]],
                    symptom_diagnostic = row[self.column_positions["Symptom Diagnostic"]].lower() in self.true_variants,
                ))

        return business_data, symptom_data 

        

    def update_col_positions(self, cols):
        for i, col in enumerate(cols):
            if col in self.column_positions:
                self.column_positions[col] = i
            else:
                raise Exception("Have unexpected columns in the data")