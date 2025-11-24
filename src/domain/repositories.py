from abc import ABC, abstractmethod
from domain.user import User
from typing import Optional, List

class UserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass
    
    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass
    
    @abstractmethod
    def update_user(self, user_id: int, user: User) -> Optional[User]:
        pass
    
    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass
