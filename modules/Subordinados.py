# coding=utf-8
from gluon import current, redirect
from gluon.html import URL
from MailAvaliacao import MailSubordinados


class Subordinados(object):
    def __init__(self):
        self.subordinados = current.session.subordinados

    def removerSubordinados(self, siapes, observacao=None):
        """

        :type subordinados: list
        :param subordinados: Lista de subordinados a serem removidos
        """
        # TODO Procurar forma mais eficiente de realizar essa busca
        for siape in siapes:
            for subordinado in self.subordinados:
                if siape == str(subordinado["SIAPE_SERVIDOR"]):
                    params = {
                        "SIAPE_SERVIDOR": subordinado["SIAPE_SERVIDOR"],
                        "SIAPE_CHEFIA_TITULAR": subordinado["SIAPE_CHEFIA_TITULAR"],
                        "UNIDADE_EXERCICIO_SERVIDOR": subordinado["SIAPE_CHEFIA_TITULAR"],
                        "OBSERVACAO": observacao
                    }
                    current.db.SUBORDINADOS_EXCLUIR.insert(**params)
                    current.db.commit()
                    self.subordinados.remove(subordinado)
                    try:
                        email = MailSubordinados(subordinado, observacao)
                        email.sendSubordinadoRemocaoMail()
                    except Exception:
                        current.session.flash = "Um erro ocorreu durante o envio de e-mail de confirmação de remoção de subordinado."
                        redirect(URL('subordinados', 'index'))




