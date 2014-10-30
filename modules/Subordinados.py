from gluon import current


class Subordinados(object):
    def __init__(self):
        self.subordinados = current.session.subordinados

    def removerSubordinados(self, subordinados):
        """


        :type subordinados: list
        :param subordinados: Lista de subordinados a serem removidos
        """
        # TODO Procurar forma mais eficiente de realizar essa busca
        for s in subordinados:
            for subordinado in self.subordinados:
                if s == str(subordinado["SIAPE_SERVIDOR"]):
                    self.subordinados.remove(subordinado)

