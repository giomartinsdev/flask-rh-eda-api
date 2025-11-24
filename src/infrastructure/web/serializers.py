def user_to_dict(user):
    """Converte um objeto User para dicionário com todos os atributos"""
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "is_active": user.is_active,
        "phone": user.phone,
        "salary": user.salary,
        "position": user.position,
        "department": user.department,
        "employment_type": user.employment_type,
        "manager_id": user.manager_id,
        "hire_date": user.hire_date,
        "birth_date": user.birth_date,
        "address": user.address,
    }
