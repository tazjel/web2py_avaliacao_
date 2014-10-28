# coding=utf-8
from gluon import current
from unirio.api import UNIRIOAPIRequest


class SIEChefiasImediatas(object):
    def __init__(self):
        self.apiRequest = UNIRIOAPIRequest(current.kAPIKey)
        self.path = "V_CHEFIAS_IMEDIATAS"

    def getChefiaForCPF(self, CPF):
        """
        Dado o CPF de um servidor, a consulta trará os seus dados e de suas chefias
        mais informações em http://sistemas.unirio.br/api/default/index#table_V_CHEFIAS_IMEDIATAS

        :param CPF: O CPF do servidor a ser buscado, sem máscara
        :type CPF: str
        :rtype : dict
        """
        params = {"CPF_SERVIDOR": CPF}

        servidor = self.apiRequest.performGETRequest(self.path, params)
        return servidor.content[0]

class SIESubordinados(object):
    def __init__(self):
        self.apiRequest = UNIRIOAPIRequest(current.kAPIKey)
        self.path = "V_SUBORDINADOS"
        self.lmin = 0
        self.lmax = 1000

    def getSubordinados(self, CPF):
        """
        Dado o CPF de um servidor com chefia, a consulta trará todos os servidores subordinados a ele.
        Mais informações em http://sistemas.unirio.br/api/default/index#table_V_SUBORDINADOS

        :param CPF: O CPF do servidor com chefia a ser buscado, sem máscara
        :type CPF: str
        :return: Uma lista de dicionários de subordinados
        :rtype : list
        """
        params = {"CPF_CHEFIA": CPF,
                  "LMIN": self.lmin,
                  "LMAX": self.lmax}

        try:
            subordinados = self.apiRequest.performGETRequest(self.path, params)
            return subordinados.content
        except Exception:
            pass

