# coding=utf-8
from gluon import current
from datetime import date
import math


class Avaliacao(object):
    def __init__(self, ano, siapeServidor):
        self.ano = ano
        self.tipo = current.session.avaliacaoTipo
        self.servidorAvaliado = self._validateAccessForCurrentSession(siapeServidor)
        current.session.servidorAvaliado = self.servidorAvaliado


    def _validateAccessForCurrentSession(self, siapeServidor):
        """
        Dada a sessão corrente de usuário e tipo de avaliaçao, verifica se o mesmo tem autorização
        para acessar a manipular uma avaliação.

        * Em uma autoavaliação, o dicionário devem ser igual ao do servidor da sessão.
        * Em uma avaliação de subordinado, o dicionário deve estar contido na lista de subordinados

        :type dadosServidor: dict
        :rtype: dict
        :param dadosServidor: O dicionário correspondente a um servidor válido para uma avaliaçao
        """
        if current.session.avaliacaoTipo == "subordinados":
            if current.session.avaliacaoTipo in self.tiposDeAvaliacaoesForCurrentSession().keys():
                for subordinado in current.session.subordinados:
                    if str(subordinado['SIAPE_SERVIDOR']) == str(siapeServidor):
                        return subordinado

        elif str(siapeServidor) == str(current.session.dadosServidor["SIAPE_SERVIDOR"]):
            return current.session.dadosServidor

        raise Exception("Você não tem permissão de acesso para a avaliaçao de " + str(siapeServidor))

    @staticmethod
    def tiposDeAvaliacaoesForCurrentSession():
        """
        Dada uma determinada sessão de usuário, o método retonará um dicionário com os tipos de avaliação possíveis.

        :rtype : dict
        :return: Retorna um dicionário em que k = str de um tipo de avaliação e v = label do tipo
        """
        tipos = {"autoavaliacao": "Autoavaliação"}
        if current.session.subordinados:
            tipos.update({"subordinados": "Avaliar subordinados"})

        return tipos

    @staticmethod
    def isCiente():
        """
        Dada uma determinada sessão de usuário, o método retorna o booleano equivalente a se terminou
        uma avaliação ou não.

        :rtype : bool
        :return: True caso tenha marcado ciente ao final de uma avaliação e False caso contrário
        """
        if current.session.avaliacao:
            if current.session.avaliacaoTipo == 'autoavaliacao':
                if 'CIENTE_SERVIDOR' in current.session.avaliacao and current.session.avaliacao[
                    'CIENTE_SERVIDOR'] == 'T':
                    return True
            elif current.session.avaliacaoTipo == 'subordinados':
                if 'CIENTE_CHEFIA' in current.session.avaliacao and current.session.avaliacao['CIENTE_CHEFIA'] == 'T':
                    return True

    @staticmethod
    def isChefiaCiente():
        """
        Dada uma autoavaliação de um servidor, verifica se a chefia imediata já terminou sua avaliação

        :rtype : bool
        """
        if current.session.avaliacaoTipo == 'autoavaliacao':
            if 'CIENTE_CHEFIA' in current.session.avaliacao and current.session.avaliacao['CIENTE_CHEFIA'] == 'T':
                return True

    @staticmethod
    def isFinalizada():
        """
        TODO documentar esta caceta
        :return:
        """
        if 'CIENTE_CHEFIA' in current.session.avaliacao and current.session.avaliacao['CIENTE_CHEFIA'] == 'T':
            if 'CIENTE_SERVIDOR' in current.session.avaliacao and current.session.avaliacao['CIENTE_SERVIDOR'] == 'T':
                return True
        else:
            raise Exception(current.session)

    @staticmethod
    def anosDeExercicio():
        return current.db().select(current.db.PERIODOS_ABERTOS_AVAL.ANO_EXERCICIO)

    # TODO documentar pontosPorFator
    @staticmethod
    def pontosPorFator(topico):
        """

        :param topico: string correspondente a um Fator
        :return: int correspondente aos pontos por fator
        """
        if current.session.avaliacao:
            if 'NOTA_' + topico in current.session.avaliacao:
                return round(float(current.session.avaliacao['NOTA_' + topico] +
                        current.session.avaliacao['NOTA_' + topico + '_CHEFIA']) / 2, 1)

    @staticmethod
    def notaFinal():
        somatorioNotas = 0
        for k, v in current.session.avaliacao.iteritems():
            if Avaliacao.columnIsNota(k) and v:
                somatorioNotas += v
        return round(float(somatorioNotas) / 18, 1)

    @property
    def dados(self):
        avaliacao = current.db((current.db.AVAL_ANEXO_1.ANO_EXERCICIO == self.ano)
                               & (
            current.db.AVAL_ANEXO_1.SIAPE_SERVIDOR == self.servidorAvaliado['SIAPE_SERVIDOR'])).select().first()
        if avaliacao:
            return avaliacao
        else:
            return {
                "ANO_EXERCICIO": self.ano,
                "SIAPE_SERVIDOR": self.servidorAvaliado['SIAPE_SERVIDOR'],
                "SIAPE_CHEFIA": self.servidorAvaliado['SIAPE_CHEFIA_TITULAR']
            }

    @staticmethod
    def columnNeedChefia(column):
        """
        Verifica se a coluna fornecidade deve ser preenchiada pela chefia

        :param column: uma coluna do banco AVAL_ANEXO_1
        :type column: str
        :rtype : bool
        """
        return column.endswith("_CHEFIA")

    @staticmethod
    def columnIsNota(column):
        """

        :param column: uma coluna do banco AVAL_ANEXO_1
        :type column: str
        :rtype : bool
        """
        return column.startswith("NOTA_")

    def _validFieldsForChefia(self, fields):
        """
        Dada uma lista de campos, o método retorna somente os campos em que a chefia pode manipular

        :type fields: list
        :rtype : list
        :param fields: Uma lista de campos a ser validada
        :return: Campos que podem ser manipulados em uma sessão de chefia
        """
        return [field for field in fields if self.columnNeedChefia(field)]


    def _filterFields(self, vars):
        """


        :type vars: dict
        :param vars:
        """
        if self.tipo == 'subordinados':
            validFields = self._validFieldsForChefia(vars.keys())
        elif self.tipo == 'autoavaliacao':
            validFields = [field for field in vars.keys() if field not in self._validFieldsForChefia(vars.keys())]

        filteredDict = {}
        filteredDict.update(self.dados)
        filteredDict.update({"ANO_EXERCICIO": self.ano, "DATA_DOCUMENTO": date.today()})

        for field in validFields:
            if field in current.db.AVAL_ANEXO_1.fields:
                filteredDict.update({field: vars[field]})

        return filteredDict


    def salvarModificacoes(self, vars):
        if not self.isFinalizada():
            filteredDict = self._filterFields(vars)

            current.db.AVAL_ANEXO_1.update_or_insert((current.db.AVAL_ANEXO_1.ANO_EXERCICIO == self.ano)
                                                     & (
                current.db.AVAL_ANEXO_1.SIAPE_SERVIDOR == self.servidorAvaliado['SIAPE_SERVIDOR']), **filteredDict)
            # atualiza session
            current.session.avaliacao.update(filteredDict)

            current.session.flash = "Modificações salvas com sucesso."







