import inspect
from flask_restx import fields
from typing import get_type_hints, Any
from domain.enums import Department, Position, EmploymentType

def map_python_type_to_swagger(python_type: Any) -> fields.Raw:
    """Mapeia tipos Python para tipos Swagger"""
    type_mapping = {
        str: fields.String,
        int: fields.Integer,
        float: fields.Float,
        bool: fields.Boolean,
    }
    return type_mapping.get(python_type, fields.String)

def get_enum_values(field_name: str):
    """Retorna valores de enum baseado no nome do campo"""
    enum_mapping = {
        'department': [d.value for d in Department],
        'position': [p.value for p in Position],
        'employment_type': [e.value for e in EmploymentType]
    }
    return enum_mapping.get(field_name, None)

def generate_swagger_model_from_class(cls, exclude_fields=None):
    """Gera dinamicamente um modelo Swagger a partir de uma classe Python"""
    if exclude_fields is None:
        exclude_fields = []
    
    swagger_fields = {}
    sig = inspect.signature(cls.__init__)
    
    try:
        type_hints = get_type_hints(cls.__init__)
    except:
        type_hints = {}
    
    for param_name, param in sig.parameters.items():
        if param_name == 'self' or param_name in exclude_fields:
            continue
        
        is_required = param.default == inspect.Parameter.empty
        param_type = type_hints.get(param_name, str)
        
        enum_values = get_enum_values(param_name)
        if enum_values:
            swagger_fields[param_name] = fields.String(
                required=is_required,
                description=f'{param_name.capitalize()}',
                enum=enum_values
            )
        else:
            swagger_field_type = map_python_type_to_swagger(param_type)
            swagger_fields[param_name] = swagger_field_type(
                required=is_required,
                description=f'{param_name.capitalize()}'
            )
    
    return swagger_fields

def generate_response_model_from_class(cls):
    """Gera modelo de resposta incluindo todos os atributos"""
    swagger_fields = generate_swagger_model_from_class(cls, exclude_fields=[])
    
    if 'id' not in swagger_fields:
        swagger_fields['id'] = fields.Integer(description='ID', required=False)
    
    return swagger_fields
