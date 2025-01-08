from typing import Generic, TypeVar, Type, List, Dict;
from sqlalchemy.ext.asyncio import AsyncSession;
from sqlalchemy.exc import SQLAlchemyError, IntegrityError;
from sqlalchemy.future import select
from abc import ABC, abstractmethod;
from uuid import UUID;
T = TypeVar("T");

class BaseService(ABC, Generic[T]):
    def __init__(self, session: AsyncSession, model:Type[T]):
        self.session = session;
        self.model = model;
        self.instance = None

    async def handle_session_error(self, func, *args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            raise IntegrityError(f"IntegrityError: {e}")
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"SQLAlchemyError: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

    async def __commit_in_session(self, callable, refresh=True, *args, **kwargs):
        return await self.handle_session_error(callable, *args, **kwargs)

    async def __exe_in_session(self, query, fetch_one = True):
        result = await self.handle_session_error(self.session.execute, query)
        if fetch_one:
            return result.scalars().first()
        else:
            return result.scalars().all()

    @abstractmethod
    def before_add(self,*args, **kwargs):
        pass
    async def add(self, *args, **kwargs) -> T:
        async def _add(**kwargs):
            self.instance = self.model(**kwargs)
            self.before_add(**kwargs)
            self.session.add(self.instance)
            return self.instance
        instance = await self.__commit_in_session(_add, **kwargs)
        return instance

    async def get_by_id(self, id: UUID) -> T:
        query = select(self.model).where(self.model.id == id)
        instance = self.__exe_in_session(query)
        if not instance:
            return None
        return instance

    async def update(self, id: UUID, **kwargs) -> T:
        async def _update(id:UUID):
            self.instance = await self.get_by_id(id);
            for k,v in kwargs.items():
                setattr(self.instance,k,v)
            return self.instance
        instance = await self.__commit_in_session(_update, refresh = False, id = id, **kwargs)

        return instance

    async def hard_delete(self, id: UUID) -> str:
        async def _delete(id: UUID):
            self.instance = await self.get_by_id(id);
            await self.session.delete(self.instance);
            return self.instance

        return await self.__commit_in_session(_delete, refresh = False, id = id)


    async def filter(self, fields=None, **kwargs) -> List[Dict]:
        """
        Filter records with dynamic criteria and select specific columns.

        Args:
            fields (list): List of fields to retrieve. If None, retrieves all columns.
                           Example: fields=["id", "name"]
            kwargs: Key-value pairs for filtering.
                    Example: filter(name="Alice", age=30)

        Returns:
            List of filtered results (as dictionaries if fields are specified) or None in case of error.
        """
        query = select(self.model)

        if fields:
            selected_fields = [getattr(self.model, field) for field in fields if hasattr(self.model, field)]
            if not selected_fields:
                raise AttributeError("No valid fields specified for selection.")
            query = select(*selected_fields)

        for field, value in kwargs.items():
            if hasattr(self.model, field):
                query = query.where(getattr(self.model, field) == value)
            else:
                raise AttributeError(f"Field '{field}' does not exist in model '{self.model.__name__}'.")

        response = await self.__exe_in_session(query, fetch_one=False)

        if fields and response:
            return [dict(zip(fields, row)) for row in response]
        return response or []