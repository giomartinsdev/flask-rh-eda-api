from enum import Enum


class Department(str, Enum):
    """Departamentos disponíveis na empresa"""

    ENGINEERING = "engineering"
    SALES = "sales"
    MARKETING = "marketing"
    HR = "hr"
    FINANCE = "finance"
    OPERATIONS = "operations"
    IT = "it"
    CUSTOMER_SUPPORT = "customer_support"


class Position(str, Enum):
    """Cargos disponíveis na empresa"""

    INTERN = "intern"
    JUNIOR = "junior"
    PLENO = "pleno"
    SENIOR = "senior"
    TECH_LEAD = "tech_lead"
    MANAGER = "manager"
    DIRECTOR = "director"
    VP = "vp"
    CTO = "cto"
    CEO = "ceo"


class EmploymentType(str, Enum):
    """Tipos de contratação"""

    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERN = "intern"
    FREELANCE = "freelance"
