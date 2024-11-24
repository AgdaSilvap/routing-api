from typing import List

from fastapi import APIRouter, Depends, status 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas.address_schema import AddressSchemaBase
from models.address_model import AddressModel
from core.deps import get_session

router = APIRouter()

#POST Address
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AddressSchemaBase)
async def post_address(addr: AddressSchemaBase, db: AsyncSession = Depends(get_session)):
    new_route: AddressModel = AddressModel(description = addr.description, lat = addr.lat, long = addr.long)

    db.add(new_route)
    await db.commit()

    return new_route

#GET Addresses
@router.get('/', response_model=List[AddressSchemaBase])
async def get_address(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AddressModel)
        result = await session.execute(query)
        routes: List[AddressModel] = result.scalars().unique().all()

        return routes
    
