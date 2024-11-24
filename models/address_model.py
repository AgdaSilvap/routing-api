from sqlalchemy import Column, Double, String, Integer


from core.configs import settings

Base = settings.DBBase

class AddressModel(Base):
     __tablename__ = 'address'

     id = Column(Integer, primary_key=True, autoincrement=True)
     description = Column(String(400), nullable=False, unique=True)
     lat = Column(Double, nullable=False)
     long = Column(Double, nullable=False)

    

