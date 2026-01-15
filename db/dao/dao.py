from db.dao import BaseDAO
from db.models import Service, Master


class ServiceDAO(BaseDAO):
    model = Service


class MasterDAO(BaseDAO):
    model = Master
