# coding=utf-8
from gluon import current
from SIEServidores import SIEServidorNome
from gluon.html import *

__all__ = [
    "TableAvaliacoes",
    "TableAvaliacoesRealizadas"
]



class TableAvaliacoes(object):
    def __init__(self, avaliacoes):
        """

        :type avaliacoes: list
        """
        self.avaliacoes = avaliacoes


    def servidor(self, avaliacao):

        try:
            servidor = SIEServidorNome().getServidorBySiape(avaliacao['SIAPE_SERVIDOR'])
            return servidor
        except (TypeError, ValueError, AttributeError):
            return "Servidor não encontrado"

    def chefia(self, avaliacao):

        try:
            chefia = SIEServidorNome().getServidorBySiape(avaliacao['SIAPE_CHEFIA'])
            return chefia
        except (TypeError, ValueError, AttributeError):
            return "Servidor não encontrado"



class TableAvaliacoesRealizadas(TableAvaliacoes):
    def __init__(self, avaliacoes):
        self.headers = (
            "Ano Exercício",
            "Nome Servidor",
            "SIAPE Servidor",
            "Lotação Exercício",
            "Nome Chefia",
            "SIAPE Chefia",
            "Ciente Chefia",
            "Ciente Servidor",
            "Info Complementar Servidor",
            "Sugestões Servidor",
            "Info Complementar Chefia",
            "Sugestões Chefia"
        )
        super(TableAvaliacoesRealizadas, self).__init__(avaliacoes)

    def printTable(self):
        def row(a):
            servidor = self.servidor(a)
            chefia = self.chefia(a)
            return TR( a['ANO_EXERCICIO'], servidor['NOME_FUNCIONARIO'], a['SIAPE_SERVIDOR'],
                      chefia['DESC_LOT_EXERCICIO'], chefia['NOME_FUNCIONARIO'], a['SIAPE_CHEFIA'] , a['CIENTE_CHEFIA'],
                      a['CIENTE_SERVIDOR'],a['INFO_COMPLEMENTAR_SERVIDOR'],
            a['SUGESTOES_SERVIDOR'],a['SUGESTOES_CHEFIA'], a['INFO_COMPLEMENTAR_CHEFIA'])

        return TABLE(
            THEAD(TR([TH(h) for h in self.headers])),
            TBODY([row(a) for a in self.avaliacoes if a])
        )