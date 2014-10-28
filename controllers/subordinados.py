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
