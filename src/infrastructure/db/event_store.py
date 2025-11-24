from domain.events import DomainEvent
from infrastructure.db.database import get_db_connection
import json
from typing import List, Optional

class EventStore:
    """Repositório para persistir eventos"""
    
    def save_event(self, event: DomainEvent) -> int:
        """Salva um evento no banco de dados"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO events (event_type, aggregate_id, data, occurred_at)
                VALUES (?, ?, ?, ?)
            ''', (
                event.event_type.value,
                event.aggregate_id,
                json.dumps(event.data),
                event.occurred_at
            ))
            event.event_id = cursor.lastrowid
            return event.event_id
    
    def get_events_by_aggregate(self, aggregate_id: int) -> List[DomainEvent]:
        """Busca todos os eventos de um agregado específico"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, event_type, aggregate_id, data, occurred_at
                FROM events
                WHERE aggregate_id = ?
                ORDER BY id ASC
            ''', (aggregate_id,))
            
            events = []
            for row in cursor.fetchall():
                event = DomainEvent(
                    event_type=row['event_type'],
                    aggregate_id=row['aggregate_id'],
                    data=json.loads(row['data'])
                )
                event.event_id = row['id']
                event.occurred_at = row['occurred_at']
                events.append(event)
            
            return events
    
    def get_events_by_type(self, event_type: str) -> List[DomainEvent]:
        """Busca todos os eventos de um tipo específico"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, event_type, aggregate_id, data, occurred_at
                FROM events
                WHERE event_type = ?
                ORDER BY id ASC
            ''', (event_type,))
            
            events = []
            for row in cursor.fetchall():
                event = DomainEvent(
                    event_type=row['event_type'],
                    aggregate_id=row['aggregate_id'],
                    data=json.loads(row['data'])
                )
                event.event_id = row['id']
                event.occurred_at = row['occurred_at']
                events.append(event)
            
            return events
