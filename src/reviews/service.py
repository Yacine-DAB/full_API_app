import logging

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.service import UserService
from src.books.service import BookService
from src.db.models import Review

from .schema import ReviewCreateModel

book_service = BookService()
user_service = UserService()

class ReviewService:
     async def add_review_to_book(
          self,
          user_email: str,
          book_uid: str,
          review_data: ReviewCreateModel,
          session: AsyncSession,
     ):
          try:
               book = await book_service.get_book(book_uid=book_uid, session=session)
               user = await user_service.get_user_by_email(
                    email=user_email, session=session
               )
               review_data_dict = review_data.model_dump()
               if not book:
                    raise HTTPException(
                         detail='Book not found',
                         status_code=status.HTTP_404_NOT_FOUND
                    )
                    
               if not user:
                    raise HTTPException(
                         detail='User not found', status_code=status.HTTP_404_NOT_FOUND
                    )
                    
               new_review = Review(**review_data_dict, user=user, book=book)
               
               session.add(new_review)
               
               await session.commit()
                    
               return new_review
                    
          except Exception as e:
               logging.exception(e)
               raise HTTPException(
                    detail='Oops... something went wrong! ',
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               )
     async def get_review(self, review_uid: str, session: AsyncSession):
          statment = select(Review).where(Review.uid == review_uid)
          result = await session.exec(statment)
          return result.first()
     
     async def get_all_reviews(self, session: AsyncSession):
          statment = select(Review).order_by(desc(Review.created_at))
          result = await session.exec(statment)
          return result.all()
     
     async def delete_review_to_from_book(
          self, review_uid: str, user_email: str, session: AsyncSession
     ):
          user = await user_service.get_user_by_email(user_email, session)
          review = await self.get_review(review_uid, session)
          
          if not review or (review.user != user):
               raise HTTPException(
                    detail='Cannot selete this review',
                    status_code=status.Http_403_FORBIDDEN,
               )
               
          await session.delete(review)
          
          await session.commit()
          

               
               
          