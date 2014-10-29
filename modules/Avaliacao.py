# coding=utf-8
from gluon import current


class Avaliacao(object):
    def __init__(self, ano, siapeServidor):
        self.ano = ano
        self.tipo = current.session.avalicaoTipo
        self.siapeServidor = self._validateAccessForCurrentSession(siapeServidor)


    def _validateAccessForCurrentSession(self, siapeServidor):
        """
        Dada a sessão corrente de usuário e tipo de avaliaçao, verifica se o mesmo tem autorização
        para acessar a manipular uma avaliação.

        * Em uma autoavaliação, o siapeServidor deve ser igual ao do servidor da sessão.
        * Em uma avaliação de subordinado, o siapeServidor deve estar contido em algum dos dicionários
        da lista de subordinados

        :type siapeServidor: str
        :rtype : str
        :param siapeServidor: O SIAPE de um servidor a ser verificado como válido para uma avaliaçao
        """
        if current.session.avaliacaoTipo == "subordinados":
            if current.session.avaliacaoTipo in self.tiposDeAvaliacaoesForCurrentSession().keys():
                for subordinado in current.session.subordinados:
                    if str(siapeServidor) == str(subordinado['SIAPE_SUBORDINADO']):
                        return siapeServidor

        elif str(siapeServidor) == str(current.session.dadosServidor['SIAPE_SERVIDOR']):
                return siapeServidor

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

    def isChefiaCiente(self):
        """
        Dada uma autoavaliação de um servidor, verifica se a chefia imediata já terminou sua avaliação

        :rtype : bool
        """
        if current.session.avaliacaoTipo == 'autoavaliacao':
            if current.session.avaliacao['CIENTE_CHEFIA'] == 'T':
                return True

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
            return (int(current.session.avaliacao['NOTA_' + topico]) + int(
                current.session.avaliacao['NOTA_' + topico + '_CHEFIA']) ) / 2

    @property
    def dados(self):
        avaliacao = current.db((current.db.AVAL_ANEXO_1.ANO_EXERCICIO == self.ano)
                               & (current.db.AVAL_ANEXO_1.SIAPE_SERVIDOR == self.siapeServidor)).select().first()
        if avaliacao:
            return avaliacao
        else:
            return {
                'SIAPE_SERVIDOR': self.siapeServidor,
                'ANO_EXERCICIO': self.ano,
                'SIAPE_CHEFIA': self.siapeServidor if self.tipo == "autoavaliacao" else current.session.dadosServidor['SIAPE_SERVIDOR']
            }


