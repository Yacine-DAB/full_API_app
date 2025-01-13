from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

<<<<<<< Tabnine <<<<<<<
from src.config import Config#-
from config import Config#+
>>>>>>> Tabnine >>>>>>># {"conversationId":"7f5fe95f-03ea-46cd-a73f-dca9a34c6290","source":"instruct"}

async_engine = AsyncEngine(create_engine(url=Config.DATABASE_URL))

async def init_db() -> None:
     async with async_engine.begin() as conn:
          await conn.run_sync(SQLModel.metadata.create_all)
          
async def get_session() -> AsyncSession:
     Session = sessionmaker(
          bind=async_engine, class_=AsyncSession, expire_on_commit=False
     )
     
     async with Session() as session:
          yield session
          
          