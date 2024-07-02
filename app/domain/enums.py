from enum import Enum


class StorageType(Enum):
    Refrigerados = 'Refrigerados'
    Congelados = 'Congelados'
    General = 'General'


class OrderStatus(Enum):
    En_proceso = 'En_proceso'
    Finalizado = 'Finalizado'


class UserRole(Enum):
    Admin = 'Admin'
    Chef = 'Chef'
    Waiter = 'Waiter'
    Customer = 'Customer'
