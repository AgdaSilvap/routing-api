
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas.user_schema import UserSchemaBase, UserSchemaCreate
from models.user_model import UserModel
from core.deps import get_session, get_current_user
from core.security import generate_password
from core.auth import authenticate, create_access_token


router = APIRouter()

#GET User logged
@router.get('/logado', response_model=UserSchemaBase)
def get_user_logon(user_logon: UserModel = Depends(get_current_user)):
    return user_logon


#POST Users
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user : UserModel = UserModel( username= user.username, password= generate_password(user.password), company= user.company)
    async with db as session:
        session.add(new_user)
        await session.commit()

        return new_user

        

#DELETE USER
@router.delete('/{user_id}',  status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_deleted: UserSchemaBase = result.sacalars().unique().one_or_none()

        if user_deleted:
            await session.delete(user_deleted)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
         raise HTTPException(detail='Usuário não encontrado!',
                             status_code=status.HTTP_404_NOT_FOUND)   
    
#POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm  = Depends(), db: AsyncSession = Depends(get_session)):
   user = await authenticate(username=form_data.username, password = form_data.password, db = db)

   if not user:
      raise HTTPException(detail='Usuário não encontrado!',
                             status_code=status.HTTP_400_BAD_REQUEST) 
   return JSONResponse(content={'access_token': create_access_token(sub= user.id), 'toke_type': 'bearer'}, status_code=status.HTTP_200_OK) 