from typing import Optional, List
from domain.enums import Department, Position, EmploymentType
from domain.events import DomainEvent


class User:
    def __init__(
        self,
        name: str,
        email: str,
        id: int = None,
        is_active: bool = True,
        phone: str = None,
        salary: float = 0.0,
        position: str = None,
        department: str = None,
        employment_type: str = None,
        manager_id: int = None,
        hire_date: str = None,
        birth_date: str = None,
        address: str = None,
    ):
        if "@" not in email:
            raise ValueError("Email inválido")

        if position and position not in [p.value for p in Position]:
            raise ValueError(f"Cargo inválido: {position}")
        if department and department not in [d.value for d in Department]:
            raise ValueError(f"Departamento inválido: {department}")
        if employment_type and employment_type not in [e.value for e in EmploymentType]:
            raise ValueError(f"Tipo de contratação inválido: {employment_type}")

        self.id = id
        self.name = name
        self.email = email
        self.is_active = is_active
        self.phone = phone
        self.salary = salary
        self.position = position
        self.department = department
        self.employment_type = employment_type
        self.manager_id = manager_id
        self.hire_date = hire_date
        self.birth_date = birth_date
        self.address = address

        self._uncommitted_events: List[DomainEvent] = []

    def get_uncommitted_events(self) -> List[DomainEvent]:
        """Retorna eventos pendentes de commit"""
        return self._uncommitted_events.copy()

    def clear_uncommitted_events(self):
        """Limpa eventos após serem persistidos"""
        self._uncommitted_events.clear()

    def _add_event(self, event: DomainEvent):
        """Adiciona um evento à lista de eventos não commitados"""
        self._uncommitted_events.append(event)
