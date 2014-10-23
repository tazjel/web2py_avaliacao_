from gluon import current
from unirio.api import UNIRIOAPIRequest


class SIEChefiasImediatas(object):
    def __init__(self):
        self.apiRequest = UNIRIOAPIRequest(current.kAPIKey)
        self.path = "V_CHEFIAS_IMEDIATAS"

class SIESubordinados(object):
    def __init__(self):
        self.apiRequest = UNIRIOAPIRequest(current.kAPIKey)
        self.path = "V_SUBORDINADOS"
