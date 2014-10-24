# coding=utf-8
from SIEServidores import SIEChefiasImediatas
from gluon import current


class Servidor(object):
    def getDadosToSession(self):
        """
        Método invocado sempre que um usuário se autenticar no sistema. Ao se autenticar,
        buscam-se os dados do servidor e de suas chefias imediatas, utilizando o CPF.

        """
        if current.session.auth:
            APIChefias = SIEChefiasImediatas()
            dadosServidor = APIChefias.getChefiaForCPF(current.session.auth.user.username)
            current.session = dadosServidor

            if not dadosServidor:
                current.session.flash = "Os dados da sua chefia não foram encontrados. Entre em contato com a PROGEP."