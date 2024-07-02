from enum import Enum


class StorageType(Enum):
    REFRIGERADOS = 'Refrigerados'
    CONGELADOS = 'Congelados'
    GENERAL = 'General'


class OrderStatus(Enum):
    EN_PROCESO = 'En proceso'
    FINALIZADO = 'Finalizado'


class UserRole(Enum):
    ADMIN = 'Admin'
    CHEF = 'Chef'
    WAITER = 'Waiter'
    CUSTOMER = 'Customer'
