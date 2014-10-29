# coding=utf-8
from Avaliacao import Avaliacao
from gluon import current


class MailAvaliacao(object):
    def __init__(self, avaliacao):
        """

        :type avaliacao: Avaliacao
        :param avaliacao: Uma avaliação referente ao email
        """
        self.avaliacao = avaliacao
        self.reply_to = "naoresponder.avaliacao@unirio.br"
        self.subject = "[DTIC/PROGEP] Avaliação Funcional e Institucional de " + self.avaliacao.servidorAvaliado[
            "NOME_SERVIDOR"].encode('utf-8')

    def sendConfirmationEmail(self):
        if self.avaliacao.tipo == 'autoavaliacao':
            subordinado = self.parametrosParaFinalServidor
            chefia = self.parametrosParaFinalChefia

        elif self.avaliacao.tipo == 'subordinados':
            subordinado = self.parametrosParaEnvioServidor
            chefia = self.parametrosParaEnvioChefia

        current.mail.send(**subordinado)
        current.mail.send(**chefia)

    @property
    def parametrosParaFinalServidor(self):
        """
        Email a ser enviado para o servidor ao término de uma avaliação.

        :rtype : dict
        :return: Dicionário de parâmetros de email
        """
        return {
            "to": [self.avaliacao.servidorAvaliado['EMAIL_SERVIDOR']],
            "subject": self.subject,
            "reply_to": self.reply_to,
            "message": self.avaliacao.servidorAvaliado['NOME_SERVIDOR'].encode('utf-8')
                       + ", sua avaliação foi finalizada com sucesso. Acompanhe o resumo em http://sistemas.unirio.br/avaliacao"
        }

    @property
    def parametrosParaFinalChefia(self):
        """
        Email a ser enviado para a chefia ao término de uma avaliação.

        :rtype : dict
        :return: Dicionário de parâmetros de email
        """
        return {
            "to": [self.avaliacao.servidorAvaliado['EMAIL_CHEFIA_TITULAR']],
            "subject": self.subject,
            "reply_to": self.reply_to,
            "message": self.avaliacao.servidorAvaliado['CHEFIA_TITULAR'].encode('utf-8')
                       + ", o servidor " + self.avaliacao.servidorAvaliado['NOME_SERVIDOR'].encode('utf-8')
                       + " finalizou sua avaliação com sucesso. Acompanhe o resumo em http://sistemas.unirio.br/avaliacao"
        }

    @property
    def parametrosParaEnvioServidor(self):
        """
        Email a ser enviado para um servidor ao final de uma avaliação realizada pela chefia.

        :rtype : dict
        :return: Dicionário de parâmetros de email
        """
        return {
            "to": [self.avaliacao.servidorAvaliado['EMAIL_SERVIDOR']],
            "subject": self.subject,
            "reply_to": self.reply_to,
            "message": self.avaliacao.servidorAvaliado['NOME_SERVIDOR'].encode('utf-8')
                       + ", sua avaliação foi enviada por " + self.avaliacao.servidorAvaliado['CHEFIA_TITULAR'].encode('utf-8')
                       + ". Acesse http://sistemas.unirio.br/avaliacao e finalize sua avaliação."
        }

    @property
    def parametrosParaEnvioChefia(self):
        """
        Email a ser enviado para a chefia ao final de uma avaliação feita pela mesma.

        :rtype : dict
        :return: Dicionário de parâmetros de email
        """
        return {
            "to": [self.avaliacao.servidorAvaliado['EMAIL_SERVIDOR']],
            "subject": self.subject,
            "reply_to": self.reply_to,
            "message": self.avaliacao.servidorAvaliado['CHEFIA_TITULAR'].encode('utf-8')
                       + ", sua avaliação de " + self.avaliacao.servidorAvaliado["NOME_SERVIDOR"].encode('utf-8')
                       + " foi enviada com sucesso. Acompanhe o andamento em http://sistemas.unirio.br/avaliacao"
        }