# coding=utf-8
from gluon import current
from unirio.api.apirequest import UNIRIOAPIRequest


class SIEChefiasImediatas(object):
    chefiaNotFoundErrorMessage = "Chefia não encontrada"

    def __init__(self):
        self.apiRequest = UNIRIOAPIRequest(current.kAPIKey)
        self.path = "V_CHEFIAS_IMEDIATAS"
        self.lmin = 0
        self.lmax = 1

    def getChefiaForCPF(self, CPF):
        """
        Dado o CPF de um servidor, a consulta trará os seus dados e de suas chefias
        mais informações em http://sistemas.unirio.br/api/default/index#table_V_CHEFIAS_IMEDIATAS

        Solução de CÉLIO PONTES:

        O método procura primeiramente por uma entrada normal na view de chefias, caso a mesma não seja encontrada,
        será executada uma nova consulta, que buscará por alguma entrada deste servidor como uma chefia. Isso resultará
        em dados incompletos e mensagens de erro, mas não impossibilitará o mesmo de utilizar o sistema e avaliar seus
        subordinados.

        :param CPF: O CPF do servidor a ser buscado, sem máscara
        :type CPF: str
        :rtype : dict
        """
        try:
            params = {
                "CPF_SERVIDOR": CPF,
                "LMIN": self.lmin,
                "LMAX": self.lmax
            }
            servidor = self.apiRequest.performGETRequest(self.path, params)

            return servidor.content[0]
        except ValueError:
            try:
                params = {
                    "CPF_CHEFIA": CPF,
                    "LMIN": self.lmin,
                    "LMAX": self.lmax
                }
                servidor = self.apiRequest.performGETRequest(self.path, params).content[0]
                dadosServidorGambiarra = {
                    "CPF_SERVIDOR": servidor["CPF_CHEFIA"],
                    "SIAPE_SERVIDOR": servidor["SIAPE_CHEFIA_TITULAR"],
                    "EMAIL_SERVIDOR": servidor["EMAIL_CHEFIA_TITULAR"],
                    "CARGO_SERVIDOR": "Indefinido",
                    "UNIDADE_EXERCICIO_SERVIDOR": servidor["UNIDADE_EXERCICIO_CHEFIA"],

                    "CHEFIA_TITULAR": self.chefiaNotFoundErrorMessage,
                    "SIAPE_CHEFIA": self.chefiaNotFoundErrorMessage,
                    "UNIDADE_EXERCICIO_CHEFIA": self.chefiaNotFoundErrorMessage,
                    "EMAIL_CHEFIA_TITULAR": self.chefiaNotFoundErrorMessage
                }
                return dadosServidorGambiarra
            except ValueError:
                current.session.flash = "Não foi possível achar os seus dados. Entre em contato com a PROGEPE"



class SIESubordinados(SIEChefiasImediatas):
    def __init__(self):
        super(SIESubordinados, self).__init__()
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
        params = {
            "CPF_CHEFIA": CPF,
            "LMIN": self.lmin,
            "LMAX": self.lmax
        }

        try:
            subordinados = self.apiRequest.performGETRequest(self.path, params)
            return subordinados.content
        except Exception:
            pass

