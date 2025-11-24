from domain.user import User
from domain.repositories import UserRepository
from infrastructure.db.database import get_db_connection
from typing import Optional, List


class SqliteUserRepository(UserRepository):
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Busca um usuário pelo ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, name, email, is_active, phone, salary, position, 
                       department, employment_type, manager_id, hire_date, birth_date, address
                FROM users WHERE id = ?
            """,
                (user_id,),
            )
            row = cursor.fetchone()

            if row and row["is_active"]:
                return User(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    is_active=row["is_active"],
                    phone=row["phone"],
                    salary=row["salary"],
                    position=row["position"],
                    department=row["department"],
                    employment_type=row["employment_type"],
                    manager_id=row["manager_id"],
                    hire_date=row["hire_date"],
                    birth_date=row["birth_date"],
                    address=row["address"],
                )
            return None

    def create_user(self, user: User) -> User:
        """Cria um novo usuário no banco de dados"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (name, email, is_active, phone, salary, position, 
                                 department, employment_type, manager_id, hire_date, birth_date, address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    user.name,
                    user.email,
                    user.is_active,
                    user.phone,
                    user.salary,
                    user.position,
                    user.department,
                    user.employment_type,
                    user.manager_id,
                    user.hire_date,
                    user.birth_date,
                    user.address,
                ),
            )
            user.id = cursor.lastrowid
            return user

    def get_all_users(self) -> List[User]:
        """Retorna todos os usuários"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, name, email, is_active, phone, salary, position,
                       department, employment_type, manager_id, hire_date, birth_date, address
                FROM users WHERE is_active = 1
            """
            )
            rows = cursor.fetchall()

            users = []
            for row in rows:
                user = User(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    is_active=row["is_active"],
                    phone=row["phone"],
                    salary=row["salary"],
                    position=row["position"],
                    department=row["department"],
                    employment_type=row["employment_type"],
                    manager_id=row["manager_id"],
                    hire_date=row["hire_date"],
                    birth_date=row["birth_date"],
                    address=row["address"],
                )
                users.append(user)
            return users

    def update_user(self, user_id: int, user: User) -> Optional[User]:
        """Atualiza um usuário existente"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE users 
                SET name = ?, email = ?, is_active = ?, phone = ?, salary = ?,
                    position = ?, department = ?, employment_type = ?, manager_id = ?,
                    hire_date = ?, birth_date = ?, address = ?
                WHERE id = ?
            """,
                (
                    user.name,
                    user.email,
                    user.is_active,
                    user.phone,
                    user.salary,
                    user.position,
                    user.department,
                    user.employment_type,
                    user.manager_id,
                    user.hire_date,
                    user.birth_date,
                    user.address,
                    user_id,
                ),
            )
            if cursor.rowcount > 0:
                user.id = user_id
                return user
            return None

    def delete_user(self, user_id: int) -> bool:
        """Deleta um usuário pelo ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET is_active = ? WHERE id = ?", (False, user_id)
            )
            if cursor.rowcount > 0:
                return True
            return False
