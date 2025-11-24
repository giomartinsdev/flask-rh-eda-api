from typing import List, Callable
from domain.events import DomainEvent, EventType


class EventBus:
    """Event Bus para publicar e assinar eventos"""

    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type: EventType, handler: Callable[[DomainEvent], None]):
        """Registra um handler para um tipo de evento"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def publish(self, event: DomainEvent):
        """Publica um evento para todos os handlers registrados"""
        if event.event_type in self._subscribers:
            for handler in self._subscribers[event.event_type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error handling event {event.event_type}: {str(e)}")


_event_bus = EventBus()


def get_event_bus() -> EventBus:
    """Retorna a instância global do EventBus"""
    return _event_bus
