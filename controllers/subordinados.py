# coding=utf-8
from gluon.html import *


def index():
    if not session.subordinados:
        session.flash = "Você não possui subordinados."
        redirect(URL('default', 'index'))

    # TODO criar lista de subordinados com links
    lista = UL([A(subordinado['NOME_SERVIDOR'],
                  _href=URL('anexo1', 'index', vars={'SIAPE_SERVIDOR': subordinado['SIAPE_SERVIDOR']})
                  ) for subordinado in session.subordinados])

    return dict(lista=lista)

