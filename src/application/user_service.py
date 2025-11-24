from domain.user import User
from domain.repositories import UserRepository
from domain.events import (
    UserCreatedEvent,
    UserUpdatedEvent,
    UserDeletedEvent,
    PositionChangedEvent,
    SalaryChangedEvent,
    DepartmentChangedEvent,
    ManagerChangedEvent,
    EmploymentTypeChangedEvent,
    UserActivatedEvent,
    UserDeactivatedEvent,
    UserNameChangedEvent,
    UserEmailChangedEvent,
    UserPhoneChangedEvent,
    UserAddressChangedEvent,
    UserHiredEvent,
    UserPromotedEvent,
    UserDemotedEvent,
    UserQueriedEvent,
    UserListQueriedEvent,
    UserEventsQueriedEvent,
)
from infrastructure.event_bus import get_event_bus
from infrastructure.db.event_store import EventStore
from typing import Optional, List


class UserService:
    def __init__(self, user_repository: UserRepository, event_store: EventStore = None):
        self.user_repository = user_repository
        self.event_bus = get_event_bus()
        self.event_store = event_store or EventStore()

    def get_user(self, user_id: int, queried_by: int = None) -> Optional[User]:
        """Fetch a user and publish query event"""
        user = self.user_repository.get_user_by_id(user_id)

        if user:
            event = UserQueriedEvent(user_id, queried_by)
            self.event_store.save_event(event)
            self.event_bus.publish(event)

        return user

    def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        created_user = self.user_repository.create_user(user)

        event = UserCreatedEvent(created_user.id, user_data)
        self.event_store.save_event(event)
        self.event_bus.publish(event)

        return created_user

    def get_all_users(self, filters: dict = None, queried_by: int = None) -> List[User]:
        """Fetch all users and publish query event"""
        users = self.user_repository.get_all_users()

        event = UserListQueriedEvent(filters, queried_by)
        self.event_store.save_event(event)
        self.event_bus.publish(event)

        return users

    def update_user(
        self, user_id: int, user_data: dict, changed_by: int = None
    ) -> Optional[User]:
        """Update user and publish events for each detected change"""
        current_user = self.user_repository.get_user_by_id(user_id)
        if not current_user:
            return None

        field_event_map = {
            "name": lambda old, new: UserNameChangedEvent(user_id, old, new),
            "email": lambda old, new: UserEmailChangedEvent(user_id, old, new),
            "phone": lambda old, new: UserPhoneChangedEvent(user_id, old, new),
            "address": lambda old, new: UserAddressChangedEvent(user_id, old, new),
            "position": lambda old, new: PositionChangedEvent(
                user_id, old, new, changed_by
            ),
            "salary": lambda old, new: SalaryChangedEvent(
                user_id, old, new, changed_by
            ),
            "department": lambda old, new: DepartmentChangedEvent(
                user_id, old, new, changed_by
            ),
            "manager_id": lambda old, new: ManagerChangedEvent(
                user_id, old, new, changed_by
            ),
            "employment_type": lambda old, new: EmploymentTypeChangedEvent(
                user_id, old, new, changed_by
            ),
        }

        for field, event_factory in field_event_map.items():
            if field in user_data:
                old_value = getattr(current_user, field)
                new_value = user_data[field]
                if old_value != new_value:
                    event = event_factory(old_value, new_value)
                    self.event_store.save_event(event)
                    self.event_bus.publish(event)

        if (
            "is_active" in user_data
            and user_data["is_active"] != current_user.is_active
        ):
            if user_data["is_active"]:
                event = UserActivatedEvent(user_id, changed_by)
            else:
                event = UserDeactivatedEvent(user_id, changed_by)
            self.event_store.save_event(event)
            self.event_bus.publish(event)

        user = User(**user_data)
        updated_user = self.user_repository.update_user(user_id, user)

        if updated_user:
            event = UserUpdatedEvent(user_id, user_data)
            self.event_store.save_event(event)
            self.event_bus.publish(event)

        return updated_user

    def delete_user(self, user_id: int) -> bool:
        deleted = self.user_repository.delete_user(user_id)

        if deleted:
            event = UserDeletedEvent(user_id)
            self.event_store.save_event(event)
            self.event_bus.publish(event)

        return deleted

    def get_user_events(self, user_id: int, queried_by: int = None):
        """Return event history for a user"""
        event = UserEventsQueriedEvent(user_id, queried_by)
        self.event_store.save_event(event)
        self.event_bus.publish(event)

        return self.event_store.get_events_by_aggregate(user_id)

    def change_position(
        self, user_id: int, new_position: str, new_salary: float, changed_by: int = None
    ) -> Optional[User]:
        """Change a user's position (can be promotion, demotion, or lateral move)"""
        current_user = self.user_repository.get_user_by_id(user_id)
        if not current_user:
            return None

        if new_salary > current_user.salary:
            event = UserPromotedEvent(
                user_id,
                current_user.position,
                new_position,
                current_user.salary,
                new_salary,
            )
        elif new_salary < current_user.salary:
            event = UserDemotedEvent(
                user_id,
                current_user.position,
                new_position,
                current_user.salary,
                new_salary,
            )
        else:
            event = PositionChangedEvent(user_id, current_user.position, new_position)

        self.event_store.save_event(event)
        self.event_bus.publish(event)

        return self.update_user(
            user_id,
            {
                "name": current_user.name,
                "email": current_user.email,
                "is_active": current_user.is_active,
                "phone": current_user.phone,
                "salary": new_salary,
                "position": new_position,
                "department": current_user.department,
                "employment_type": current_user.employment_type,
                "manager_id": current_user.manager_id,
                "hire_date": current_user.hire_date,
                "birth_date": current_user.birth_date,
                "address": current_user.address,
            },
            changed_by,
        )
