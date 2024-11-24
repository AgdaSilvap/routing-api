from pytz import timezone

from typing import Optional, List
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer 

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.user_model import UserModel 
from core.configs import settings
from core.security import verifiy_password

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/user/login"
)

async def authenticate(userName: str, password: str, db: AsyncSession) -> Optional[UserModel]:
    async with db as session:
        query = select(UserModel).filter(UserModel.userName == userName)
        result = await session.execute(query)
        user : UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None
        
        if not verifiy_password(password, user.password):
            return None
        
        return user
    
def _create_token(type_token: str, deadline: timedelta, sub: str ) -> str:
    payload = {}
    
    sp = timezone('America/Sao_Paulo')
    expire = datetime.now(tz=sp) + deadline

    payload['type'] = type_token
    payload['exp' ] = expire
    payload['iat' ] = datetime.now(tz=sp)
    payload['sub' ] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm= settings.JWT_ALGORITHM)

def create_access_token(sub: str) -> str:
    
    return _create_token(
        type_token= 'access_token', 
        deadline= timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES), 
        sub=sub
    )