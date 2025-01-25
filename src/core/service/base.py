from typing import Generic, TypeVar, Type, List, Dict, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.future import select
from abc import ABC, abstractmethod
from uuid import UUID

T = TypeVar("T")


class BaseService(ABC, Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model
        self.instance = None

    async def handle_session_error(self, func, refresh=False, *args, **kwargs) -> T:
        try:
            instance = await func(*args, **kwargs)
            await self.session.commit()
            if refresh:
                await self.session.refresh(instance)
                return instance
            return instance
        except IntegrityError as e:
            raise IntegrityError(f"IntegrityError: {e}")
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"SQLAlchemyError: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

    async def __commit_in_session(self, call_next, refresh=True, *args, **kwargs) -> T:
        return await self.handle_session_error(call_next, refresh, *args, **kwargs)

    async def _exe_in_session(self, call_next, fetch_one=True, **kwargs) -> T:
        result = await self.handle_session_error(call_next, **kwargs)
        if fetch_one:
            return result.scalars().first()
        else:
            return result.scalars().all()

    @abstractmethod
    async def before_add(self, *args, **kwargs):
        pass

    async def add(self, *args, **kwargs) -> T:
        async def _add(**kwargs_inner):
            self.instance = self.model(**kwargs_inner)
            await self.before_add(**kwargs_inner)
            self.session.add(self.instance)
            return self.instance

        instance = await self.__commit_in_session(_add, **kwargs)
        return instance

    async def get_by_id(self, id: UUID) -> T:
        async def _get_by_id(id: UUID):
            query = select(self.model).where(self.model.id == id)
            return await self.session.execute(query)

        instance = await self._exe_in_session(_get_by_id, id=id)
        if not instance:
            return None
        return instance

    async def update(self, id: UUID, **kwargs) -> T:
        async def _update(inner_id: UUID, **inkwargs):
            self.instance = await self.get_by_id(inner_id)
            for k, v in inkwargs.items():
                setattr(self.instance, k, v)
            return self.instance

        instance = await self.__commit_in_session(
            _update, refresh=False, inner_id=id, **kwargs
        )

        return instance

    async def hard_delete(self, id: UUID) -> str:
        async def _delete(id: UUID):
            self.instance = await self.get_by_id(id)
            await self.session.delete(self.instance)
            return self.instance

        return await self.__commit_in_session(_delete, refresh=False, id=id)

    async def filter(self, fields=None, **kwargs) -> Union[List[Dict], List]:
        """
        Filter records with dynamic criteria and select specific columns.

        Args:
            fields (list): List of fields to retrieve. If None, retrieves all columns.
                           Example: fields=["id", "name"]
            kwargs: Key-value pairs for filtering.
                    Example: filter(name="Alice", age=30)

        Returns:
            List of filtered results (as dictionaries if
            fields are specified) or None in case of error.
        """
        query = select(self.model)

        if fields:
            selected_fields = [
                getattr(self.model, field)
                for field in fields
                if hasattr(self.model, field)
            ]
            if not selected_fields:
                raise AttributeError("No valid fields specified for selection.")
            query = select(*selected_fields)

        for field, value in kwargs.items():
            if hasattr(self.model, field):
                query = query.where(getattr(self.model, field) == value)
            else:
                raise AttributeError(
                    f"Field '{field}' does not exist in model '{self.model.__name__}'."
                )

        async def _filter_query():
            return await self.session.execute(query)

        response = await self._exe_in_session(_filter_query, fetch_one=False)

        # if fields and response:
        # return [dict(zip(fields, row)) for row in response]
        return response or []
