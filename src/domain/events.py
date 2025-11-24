from enum import Enum
from datetime import datetime
from typing import Any, Dict

class EventType(str, Enum):
    """Tipos de eventos do sistema"""
    # user lifecycle events
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    USER_DELETED = "user.deleted"
    USER_ACTIVATED = "user.activated"
    USER_DEACTIVATED = "user.deactivated"
    
    # user attribute change events
    USER_NAME_CHANGED = "user.name.changed"
    USER_EMAIL_CHANGED = "user.email.changed"
    USER_PHONE_CHANGED = "user.phone.changed"
    USER_ADDRESS_CHANGED = "user.address.changed"
    USER_BIRTH_DATE_CHANGED = "user.birth_date.changed"
    
    # career events
    POSITION_CHANGED = "user.position.changed"
    SALARY_CHANGED = "user.salary.changed"
    DEPARTMENT_CHANGED = "user.department.changed"
    MANAGER_CHANGED = "user.manager.changed"
    EMPLOYMENT_TYPE_CHANGED = "user.employment_type.changed"
    USER_HIRED = "user.hired"
    USER_PROMOTED = "user.promoted"
    USER_DEMOTED = "user.demoted"
    
    # query events
    USER_QUERIED = "user.queried"
    USER_LIST_QUERIED = "user.list.queried"
    USER_EVENTS_QUERIED = "user.events.queried"

class DomainEvent:
    """Evento de domínio base"""
    def __init__(self, event_type: EventType, aggregate_id: int, data: Dict[str, Any]):
        self.event_type = event_type
        self.aggregate_id = aggregate_id
        self.data = data
        self.occurred_at = datetime.now().isoformat()
        self.event_id = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "aggregate_id": self.aggregate_id,
            "data": self.data,
            "occurred_at": self.occurred_at
        }

class UserCreatedEvent(DomainEvent):
    """Evento disparado quando um usuário é criado"""
    def __init__(self, user_id: int, user_data: Dict[str, Any]):
        super().__init__(EventType.USER_CREATED, user_id, user_data)

class UserUpdatedEvent(DomainEvent):
    """Evento disparado quando um usuário é atualizado"""
    def __init__(self, user_id: int, changes: Dict[str, Any]):
        super().__init__(EventType.USER_UPDATED, user_id, changes)

class UserDeletedEvent(DomainEvent):
    """Evento disparado quando um usuário é deletado"""
    def __init__(self, user_id: int):
        super().__init__(EventType.USER_DELETED, user_id, {})

class PositionChangedEvent(DomainEvent):
    """Evento disparado quando a posição de um usuário muda"""
    def __init__(self, user_id: int, old_position: str, new_position: str, changed_by: int = None):
        super().__init__(EventType.POSITION_CHANGED, user_id, {
            "old_position": old_position,
            "new_position": new_position,
            "changed_by": changed_by
        })

class SalaryChangedEvent(DomainEvent):
    """Evento disparado quando o salário de um usuário muda"""
    def __init__(self, user_id: int, old_salary: float, new_salary: float, changed_by: int = None):
        super().__init__(EventType.SALARY_CHANGED, user_id, {
            "old_salary": old_salary,
            "new_salary": new_salary,
            "changed_by": changed_by
        })

class DepartmentChangedEvent(DomainEvent):
    """Evento disparado quando o departamento de um usuário muda"""
    def __init__(self, user_id: int, old_department: str, new_department: str, changed_by: int = None):
        super().__init__(EventType.DEPARTMENT_CHANGED, user_id, {
            "old_department": old_department,
            "new_department": new_department,
            "changed_by": changed_by
        })

class ManagerChangedEvent(DomainEvent):
    """Evento disparado quando o gerente de um usuário muda"""
    def __init__(self, user_id: int, old_manager_id: int, new_manager_id: int, changed_by: int = None):
        super().__init__(EventType.MANAGER_CHANGED, user_id, {
            "old_manager_id": old_manager_id,
            "new_manager_id": new_manager_id,
            "changed_by": changed_by
        })

class EmploymentTypeChangedEvent(DomainEvent):
    """Evento disparado quando o tipo de contratação muda"""
    def __init__(self, user_id: int, old_type: str, new_type: str, changed_by: int = None):
        super().__init__(EventType.EMPLOYMENT_TYPE_CHANGED, user_id, {
            "old_employment_type": old_type,
            "new_employment_type": new_type,
            "changed_by": changed_by
        })

class UserActivatedEvent(DomainEvent):
    """Evento disparado quando um usuário é ativado"""
    def __init__(self, user_id: int, activated_by: int = None):
        super().__init__(EventType.USER_ACTIVATED, user_id, {
            "activated_by": activated_by
        })

class UserDeactivatedEvent(DomainEvent):
    """Evento disparado quando um usuário é desativado"""
    def __init__(self, user_id: int, deactivated_by: int = None):
        super().__init__(EventType.USER_DEACTIVATED, user_id, {
            "deactivated_by": deactivated_by
        })

class UserNameChangedEvent(DomainEvent):
    """Evento disparado quando o nome muda"""
    def __init__(self, user_id: int, old_name: str, new_name: str):
        super().__init__(EventType.USER_NAME_CHANGED, user_id, {
            "old_name": old_name,
            "new_name": new_name
        })

class UserEmailChangedEvent(DomainEvent):
    """Evento disparado quando o email muda"""
    def __init__(self, user_id: int, old_email: str, new_email: str):
        super().__init__(EventType.USER_EMAIL_CHANGED, user_id, {
            "old_email": old_email,
            "new_email": new_email
        })

class UserPhoneChangedEvent(DomainEvent):
    """Evento disparado quando o telefone muda"""
    def __init__(self, user_id: int, old_phone: str, new_phone: str):
        super().__init__(EventType.USER_PHONE_CHANGED, user_id, {
            "old_phone": old_phone,
            "new_phone": new_phone
        })

class UserAddressChangedEvent(DomainEvent):
    """Evento disparado quando o endereço muda"""
    def __init__(self, user_id: int, old_address: str, new_address: str):
        super().__init__(EventType.USER_ADDRESS_CHANGED, user_id, {
            "old_address": old_address,
            "new_address": new_address
        })

class UserHiredEvent(DomainEvent):
    """Evento disparado quando um usuário é contratado"""
    def __init__(self, user_id: int, hire_date: str, position: str, department: str, salary: float):
        super().__init__(EventType.USER_HIRED, user_id, {
            "hire_date": hire_date,
            "position": position,
            "department": department,
            "salary": salary
        })

class UserPromotedEvent(DomainEvent):
    """Evento disparado quando um usuário é promovido"""
    def __init__(self, user_id: int, old_position: str, new_position: str, old_salary: float, new_salary: float):
        super().__init__(EventType.USER_PROMOTED, user_id, {
            "old_position": old_position,
            "new_position": new_position,
            "old_salary": old_salary,
            "new_salary": new_salary
        })

class UserDemotedEvent(DomainEvent):
    """Evento disparado quando um usuário é rebaixado"""
    def __init__(self, user_id: int, old_position: str, new_position: str, old_salary: float, new_salary: float):
        super().__init__(EventType.USER_DEMOTED, user_id, {
            "old_position": old_position,
            "new_position": new_position,
            "old_salary": old_salary,
            "new_salary": new_salary
        })

class UserQueriedEvent(DomainEvent):
    """Evento disparado quando um usuário é consultado"""
    def __init__(self, user_id: int, queried_by: int = None):
        super().__init__(EventType.USER_QUERIED, user_id, {
            "queried_by": queried_by
        })

class UserListQueriedEvent(DomainEvent):
    """Evento disparado quando a lista de usuários é consultada"""
    def __init__(self, filters: Dict[str, Any] = None, queried_by: int = None):
        super().__init__(EventType.USER_LIST_QUERIED, 0, {
            "filters": filters or {},
            "queried_by": queried_by
        })

class UserEventsQueriedEvent(DomainEvent):
    """Evento disparado quando os eventos de um usuário são consultados"""
    def __init__(self, user_id: int, queried_by: int = None):
        super().__init__(EventType.USER_EVENTS_QUERIED, user_id, {
            "queried_by": queried_by
        })
