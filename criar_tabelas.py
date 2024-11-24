from core.configs import settings
from core.database import engine

async def create_tables() -> None:
    from models import __all_models
    print('Criando tabelas no Banco de Dados')

    async with engine.begin() as connection:
        await connection.run_sync(settings.DBBase.metadata.drop_all)
        await connection.run_sync(settings.DBBase.metadata.create_all)
    
    print('Tabelas criadas com sucesso!')


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())