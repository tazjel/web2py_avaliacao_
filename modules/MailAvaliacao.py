# coding=utf-8
from Avaliacao import Avaliacao
from gluon import current


class MailAvaliacao(object):
    def __init__(self, avaliacao):
        """
        A classe ``MailAvaliacao``trata estritamente de envio de emails relacionados aos estágios de uma avaliação.
        Utilizada a classe nativa de email de gluon.tools.

        :type avaliacao: Avaliacao
        :param avaliacao: Uma avaliação referente ao email
        """
        self.avaliacao = avaliacao
        self.reply_to = "naoresponder.avaliacao@unirio.br"
        self.subject = "[DTIC/PROGEP] Avaliação Funcional e Institucional de " + self.avaliacao.servidorAvaliado["NOME_SERVIDOR"].encode('utf-8')
        self.footer = "**** E-MAIL AUTOMÁTICO - NÃO RESPONDA ****"

    #TODO Verificar se não é possivel pegar algum erro caso o email não seja enviado
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
            "to": [self.avaliacao.servidorAvaliado['EMAIL_CHEFIA_TITULAR']],
            "subject": self.subject,
            "reply_to": self.reply_to,
            "message": self.avaliacao.servidorAvaliado['CHEFIA_TITULAR'].encode('utf-8')
                       + ", sua avaliação de " + self.avaliacao.servidorAvaliado["NOME_SERVIDOR"].encode('utf-8')
                       + " foi enviada com sucesso. Acompanhe o andamento em http://sistemas.unirio.br/avaliacao"
        }

class MailSubordinados(object):
    def __init__(self, subordinado, observacao=""):
        """


        :type observacao: str
        :type subordinado: dict
        """
        self.reply_to = "naoresponder.avaliacao@unirio.br"
        self.subject = "[DTIC/PROGEP] Avaliação Funcional e Institucional"
        self.subordinado = subordinado
        self.observacao = observacao
        self.setorCompetenteMail = "progepe.spmf@unirio.br"
        self.footer = "\r\n\r\n **** E-MAIL AUTOMÁTICO - NÃO RESPONDA ****"

    def sendSubordinadoRemocaoMail(self):
        chefia = self.parametrosParaChefia()
        setorCompetente = self._parametrosParaSetorCompetente()

        current.mail.send(**chefia)
        current.mail.send(**setorCompetente)


    def _formatedObservacao(self):
        if self.observacao:
            return '"' + self.observacao + '"'
        else:
            return '"Nenhuma observação fornecida."'

    def parametrosParaChefia(self):
        return {
            "to": [self.subordinado['EMAIL_CHEFIA_TITULAR']],
            "subject": self.subject,
            "reply_to": self.reply_to,
            "message": self.subordinado['CHEFIA_TITULAR'].encode('utf-8')
                       + ", o servidor " + self.subordinado["NOME_SERVIDOR"].encode('utf-8')
                       + ' foi removido da sua lista de subordinados pelo motivo: ' + self._formatedObservacao()
                       + ' e foi encaminhado para devidas providências'
                       + self.footer
        }

    def _parametrosParaSetorCompetente(self):
        return {
            "to": [self.setorCompetenteMail],
            "subject": self.subject,
            "reply_to": self.reply_to,
            "message": self.subordinado['CHEFIA_TITULAR'].encode('utf-8')
                       + ", que exerce cargo de CHEFIA em " + self.subordinado["UNIDADE_EXERCICIO_CHEFIA"].encode('utf-8')
                       + ', removeu ' + self.subordinado['NOME_SERVIDOR'].encode('utf-8') + ', portador do SIAPE '
                       + str(self.subordinado['SIAPE_SERVIDOR']) + ' da sua lista de subordinados pelo motivo: '
                       + self._formatedObservacao() + self.footer
        }


class MailPROGEPE(object):
    def __init__(self, servidor):
        self.reply_to = "naoresponder.avaliacao@unirio.br"
        self.subject = "[DTIC/PROGEP] Avaliação Funcional e Institucional"
        self.setorCompetenteMail = "progepe.spmf@unirio.br"
        self.footer = "\r\n\r\n **** E-MAIL AUTOMÁTICO - NÃO RESPONDA ****"
        self.servidor = servidor

    def sendInformativoPROGEP(self, siape, nome):
        """


        :type nome: str
        :type siape: str
        :param siape: A matrícula SIAPE de um servidor que deveria fazer parte da unidade
        :param nome: O nome do servidor que deveria fazer parte da unidade
        """

        requerente = self._parametrosParaRequerente(siape, nome)
        setorCompetente = self._parametrosChefiaParaPROGEPE(siape, nome)

        current.mail.send(**requerente)
        current.mail.send(**setorCompetente)

    def _parametrosChefiaParaPROGEPE(self, siape, nome):
        return {
            "to": [self.setorCompetenteMail],
            "subject": self.subject,
            "reply_to": self.reply_to,
            "message": self.servidor['NOME_SERVIDOR'].encode('utf-8')
                       + ", em exercício no(a) " + self.servidor["UNIDADE_EXERCICIO_CHEFIA"].encode('utf-8')
                       + ', cujo e-mail é ' + self.servidor['EMAIL_SERVIDOR'].encode('utf-8') + 'afirma que o servidor '
                       + nome + ', portador do SIAPE ' + str(siape) + ', deveria constar em sua lista de subordinados.'
                       + self.footer
        }

    def _parametrosParaRequerente(self, siape, nome):
        return {
            "to": self.servidor['EMAIL_SERVIDOR'].encode('utf-8'),
            "subject": self.subject,
            "reply_to": self.reply_to,
            "message": self.servidor['NOME_SERVIDOR'].encode('utf-8')
                       + ', sua solicitação de inclusão do subordinado '
                       + nome + ', portador do SIAPE ' + str(siape) + ' foi enviada com sucesso ao setor responsável'
                       + self.footer
        }