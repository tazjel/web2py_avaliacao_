# coding=utf-8
from gluon.html import *


def index():
    if not session.subordinados:
        session.flash = "Você não possui subordinados."
        redirect(URL('default', 'index'))

    # TODO criar lista de subordinados com links
    lista = UL([A(subordinado['NOME_SUBORDINADO'],
                  _href=URL('anexo1', 'index', vars=dict(CPF_SUBORDINADO_MASCARA=subordinado['CPF_SUBORDINADO_MASCARA']))
                  ) for subordinado in session.subordinados])

    return dict(lista=lista)


def exampleControllerFunction():
    class FormAvaliacao(object):
        def __init__(self):
            self.servidor = current.session.dadosServidor
            # TODO Por causa de um UnicodeEncodeError, foi necessário colocar essa gambi. Resolver ou utilizar DBSM.REMOVEACENTOS na View
            self.tipo = current.session.avaliacaoTipo

        @property
        def exampleError(self):
            return FORM(
                INPUT(_name='NOME_SERVIDOR', _type='text', _value=self.servidor['NOME_SERVIDOR'], _readonly='true')
            )

        @property
        def exampleOk(self):
            return self.servidor['NOME_SERVIDOR']

    form = FormAvaliacao().exampleError
    form = FormAvaliacao().exampleOk

    return dict(form=form)