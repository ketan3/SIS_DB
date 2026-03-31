from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# Creates the engine for asynchronous PostgreSQL (asyncpg)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True, # This will show you the SQL it generates in your terminal
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
