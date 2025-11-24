from flask_restx import Resource, Namespace, fields
from flask import request
from application.user_service import UserService
from infrastructure.db.sqlite_user_repository import SqliteUserRepository
from infrastructure.db.database import init_db
from infrastructure.db.event_store import EventStore
from domain.user import User
from infrastructure.web.swagger_mapper import (
    generate_swagger_model_from_class,
    generate_response_model_from_class,
)
from infrastructure.web.serializers import user_to_dict
from infrastructure.event_bus import get_event_bus
from application.event_handlers import (
    LogEventHandler,
    PositionChangeNotificationHandler,
    SalaryChangeAuditHandler,
    DepartmentChangeHandler,
    UserActivationHandler,
    PositionChangeHandler,
    QueryAuditHandler,
)
from domain.enums import Position
from domain.events import EventType

ns_user = Namespace("user", description="User related operations")

init_db()

event_bus = get_event_bus()
log_handler = LogEventHandler()
position_handler = PositionChangeNotificationHandler()
salary_handler = SalaryChangeAuditHandler()
department_handler = DepartmentChangeHandler()
activation_handler = UserActivationHandler()
position_change_handler = PositionChangeHandler()
query_audit_handler = QueryAuditHandler()

for event_type in EventType:
    event_bus.subscribe(event_type, log_handler.handle)

event_bus.subscribe(EventType.POSITION_CHANGED, position_handler.handle)
event_bus.subscribe(EventType.SALARY_CHANGED, salary_handler.handle)
event_bus.subscribe(EventType.DEPARTMENT_CHANGED, department_handler.handle)
event_bus.subscribe(EventType.USER_ACTIVATED, activation_handler.handle)
event_bus.subscribe(EventType.USER_DEACTIVATED, activation_handler.handle)
event_bus.subscribe(EventType.USER_PROMOTED, position_change_handler.handle)
event_bus.subscribe(EventType.USER_DEMOTED, position_change_handler.handle)
event_bus.subscribe(EventType.USER_QUERIED, query_audit_handler.handle)
event_bus.subscribe(EventType.USER_LIST_QUERIED, query_audit_handler.handle)
event_bus.subscribe(EventType.USER_EVENTS_QUERIED, query_audit_handler.handle)

user_repository = SqliteUserRepository()
event_store = EventStore()
user_service = UserService(user_repository, event_store)

user_input_model = ns_user.model(
    "UserInput", generate_swagger_model_from_class(User, exclude_fields=["id"])
)
user_response_model = ns_user.model(
    "UserResponse", generate_response_model_from_class(User)
)


@ns_user.route("/")
class UsersResource(Resource):
    @ns_user.doc("get_all_users")
    @ns_user.response(200, "Success", [user_response_model])
    @ns_user.response(500, "Internal error")
    def get(self):
        """Get the list of users"""
        try:
            users = user_service.get_all_users()
            return [user_to_dict(u) for u in users], 200
        except Exception as e:
            ns_user.abort(500, "Error listing users")

    @ns_user.doc("create_user")
    @ns_user.expect(user_input_model)
    @ns_user.response(201, "User created successfully", user_response_model)
    @ns_user.response(400, "Invalid data")
    @ns_user.response(500, "Internal error")
    def post(self):
        """Create a new user"""
        try:
            user_data = request.json
            user = user_service.create_user(user_data)
            return user_to_dict(user), 201
        except ValueError as e:
            ns_user.abort(400, str(e))
        except Exception as e:
            ns_user.abort(500, "Error creating user")


@ns_user.route("/<int:user_id>")
class UserResource(Resource):
    @ns_user.doc("get_user")
    @ns_user.response(200, "Success", user_response_model)
    @ns_user.response(404, "User not found")
    @ns_user.response(500, "Internal error")
    def get(self, user_id):
        """Get a specific user by ID"""
        try:
            user = user_service.get_user(user_id)
            if user:
                return user_to_dict(user), 200
            ns_user.abort(404, "User not found")
        except Exception as e:
            ns_user.abort(500, "Error fetching user")

    @ns_user.doc("update_user")
    @ns_user.expect(user_input_model)
    @ns_user.response(200, "User updated successfully", user_response_model)
    @ns_user.response(400, "Invalid data")
    @ns_user.response(404, "User not found")
    @ns_user.response(500, "Internal error")
    def put(self, user_id):
        """Update an existing user"""
        try:
            user_data = request.json
            user = user_service.update_user(user_id, user_data)
            if user:
                return user_to_dict(user), 200
            ns_user.abort(404, "User not found")
        except ValueError as e:
            ns_user.abort(400, str(e))
        except Exception as e:
            ns_user.abort(500, "Error updating user")

    @ns_user.doc("delete_user")
    @ns_user.response(200, "User deleted successfully")
    @ns_user.response(404, "User not found")
    @ns_user.response(500, "Internal error")
    def delete(self, user_id):
        """Delete a user"""
        try:
            deleted = user_service.delete_user(user_id)
            if deleted:
                return {"msg": "User deleted successfully"}, 200
            ns_user.abort(404, "User not found")
        except Exception as e:
            ns_user.abort(500, "Error deleting user")


@ns_user.route("/<int:user_id>/events")
class UserEventsResource(Resource):
    @ns_user.doc("get_user_events")
    @ns_user.response(200, "User event history")
    def get(self, user_id):
        """Get a user's event history"""
        try:
            events = user_service.get_user_events(user_id)
            return [e.to_dict() for e in events], 200
        except Exception as e:
            ns_user.abort(500, "Error fetching events")


@ns_user.route("/<int:user_id>/change-position")
class UserPositionChangeResource(Resource):
    @ns_user.doc("change_position")
    @ns_user.expect(
        ns_user.model(
            "PositionChange",
            {
                "new_position": fields.String(
                    required=True,
                    description="New position",
                    enum=[pos.value for pos in Position],
                ),
                "new_salary": fields.Float(required=True, description="New salary"),
                "changed_by": fields.Integer(
                    description="ID of the user making the position change"
                ),
            },
        )
    )
    @ns_user.response(200, "Position changed successfully", user_response_model)
    @ns_user.response(404, "User not found")
    @ns_user.response(400, "Invalid data")
    def post(self, user_id):
        """Change an employee's position (promotion, demotion, or lateral move)"""
        try:
            data = request.json
            new_position = data.get("new_position")
            new_salary = data.get("new_salary")
            changed_by = data.get("changed_by")

            user = user_service.change_position(
                user_id, new_position, new_salary, changed_by
            )
            if user:
                return user_to_dict(user), 200
            ns_user.abort(404, "User not found")
        except ValueError as e:
            ns_user.abort(400, str(e))
        except Exception as e:
            ns_user.abort(500, "Error changing user position")
