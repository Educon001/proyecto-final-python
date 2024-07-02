from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, TypeVar, Generic, Optional

T = TypeVar('T')


class IRepository(ABC, Generic[T]):

        @abstractmethod
        def get_all(self) -> Optional[List[T]]:
            pass

        @abstractmethod
        def add(self, entity: T) -> T:
            pass

        @abstractmethod
        def get_by_id(self, entity_id: UUID) -> Optional[T]:
            pass

        @abstractmethod
        def delete(self, entity_id: UUID) -> Optional[UUID]:
            pass

