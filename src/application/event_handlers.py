from domain.events import DomainEvent, EventType
from abc import ABC, abstractmethod

class EventHandler(ABC):
    """Handler base para eventos"""
    @abstractmethod
    def handle(self, event: DomainEvent):
        pass

class LogEventHandler(EventHandler):
    """Handler que loga todos os eventos"""
    def handle(self, event: DomainEvent):
        print(f"[EVENT LOG] {event.event_type.value} - User ID: {event.aggregate_id}")
        print(f"            Data: {event.data}")
        print(f"            Time: {event.occurred_at}")

class PositionChangeNotificationHandler(EventHandler):
    """Handler que notifica quando há mudança de posição"""
    def handle(self, event: DomainEvent):
        old_pos = event.data.get('old_position')
        new_pos = event.data.get('new_position')
        print(f"[NOTIFICATION] User {event.aggregate_id} changed position from {old_pos} to {new_pos}")

class SalaryChangeAuditHandler(EventHandler):
    """Handler que audita mudanças de salário"""
    def handle(self, event: DomainEvent):
        old_salary = event.data.get('old_salary')
        new_salary = event.data.get('new_salary')
        changed_by = event.data.get('changed_by', 'system')
        print(f"[AUDIT] Salary changed for user {event.aggregate_id}")
        print(f"        From: ${old_salary} to ${new_salary}")
        print(f"        Changed by: {changed_by}")

class DepartmentChangeHandler(EventHandler):
    """Handler que processa mudanças de departamento"""
    def handle(self, event: DomainEvent):
        old_dept = event.data.get('old_department')
        new_dept = event.data.get('new_department')
        print(f"[DEPARTMENT] User {event.aggregate_id} moved from {old_dept} to {new_dept}")
        
class UserActivationHandler(EventHandler):
    """Handler que processa ativações e desativações de usuários"""
    def handle(self, event: DomainEvent):
        action = "activated" if event.event_type == EventType.USER_ACTIVATED else "deactivated"
        print(f"[USER STATUS] User {event.aggregate_id} has been {action}")
        
class PositionChangeHandler(EventHandler):
    """Handler que processa mudanças de posição de usuários (promoções, demoções, mudanças laterais)"""
    def handle(self, event: DomainEvent):
        old_pos = event.data.get('old_position')
        new_pos = event.data.get('new_position')
        old_salary = event.data.get('old_salary')
        new_salary = event.data.get('new_salary')
        
        change_type = "lateral"
        if new_salary and old_salary:
            if new_salary > old_salary:
                change_type = "promoção"
            elif new_salary < old_salary:
                change_type = "demoção"
        
        print(f"[POSITION CHANGE] User {event.aggregate_id} - {change_type}")
        print(f"                  Position: {old_pos} → {new_pos}")
        if new_salary and old_salary:
            print(f"                  Salary: ${old_salary} → ${new_salary}")

class QueryAuditHandler(EventHandler):
    """Handler que audita consultas de usuários"""
    def handle(self, event: DomainEvent):
        queried_by = event.data.get('queried_by', 'unknown')
        print(f"[QUERY AUDIT] Events for user {event.aggregate_id} were queried by {queried_by}")