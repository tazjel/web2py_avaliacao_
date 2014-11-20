# coding=utf-8
from SIEServidores import SIEChefiasImediatas, SIESubordinados
from gluon import current, redirect, URL


class Servidor(object):
    @property
    def isChefia(self):
        return True if current.session.subordinados else False

    @property
    def __dadosChefiaImediata(self):
        APIChefias = SIEChefiasImediatas()
        return APIChefias.getChefiaForCPF(current.session.auth.user.username)

    @property
    def __subordinados(self):
        APISubordinados = SIESubordinados()
        # TODO para fins de desenvolvimento. Alterar linha para testes finais e produção
        subordinados = APISubordinados.getSubordinados(current.session.auth.user.username)
        # subordinados = APISubordinados.getSubordinados('12467599779')
        excluidos = current.db(current.db.SUBORDINADOS_EXCLUIR.SIAPE_CHEFIA_TITULAR==current.session.dadosServidor["SIAPE_SERVIDOR"]).select()
        # excluidos = current.db(current.db.SUBORDINADOS_EXCLUIR.SIAPE_CHEFIA_TITULAR==current.session.dadosServidor["SIAPE_CHEFIA_TITULAR"]).select()
        for excluido in excluidos:
            for subordinado in subordinados:
                if excluido.SIAPE_SERVIDOR == subordinado["SIAPE_SERVIDOR"]:
                    subordinados.remove(subordinado)
        return subordinados

    def getDadosToSession(self):
        """
        Método invocado sempre que um usuário se autenticar no sistema. Ao se autenticar,
        buscam-se os dados do servidor e de suas chefias imediatas, utilizando o CPF.

        """
        if current.session.auth and not current.session.dadosServidor:
            current.session.dadosServidor = self.__dadosChefiaImediata

            if not current.session.dadosServidor:
                raise Exception("Os dados da sua chefia não foram encontrados. Entre em contato com a PROGEP.")

            subordinados = self.__subordinados
            if subordinados:
                # Se o servidor possuir subordinados, armazenamos os mesmos, ordenados ASC por NOME_SUBORDINADO
                from operator import itemgetter
                current.session.subordinados = sorted(subordinados, key=itemgetter('NOME_SERVIDOR'))
            redirect(URL('default', 'mensagem'))