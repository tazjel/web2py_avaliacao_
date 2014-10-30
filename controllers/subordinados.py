# coding=utf-8
from gluon.html import *
from Subordinados import Subordinados

def index():
    if not session.subordinados:
        session.flash = "Você não possui subordinados."
        redirect(URL('default', 'index'))

    # TODO criar lista de subordinados com links

    items = []
    for subordinado in session.subordinados:
        items.append(LI(
            INPUT(_type="checkbox", _name="subordinados", _value=subordinado['SIAPE_SERVIDOR']) + " " +
            A(subordinado['NOME_SERVIDOR'],
              _href=URL('anexo1', 'index', vars={'SIAPE_SERVIDOR': subordinado['SIAPE_SERVIDOR']}))
        ))

    form = FORM(
        UL(items),
        INPUT(_type="submit", _value="Não se encontra em exercício na unidade")
    )

    if form.process().accepted:
        subordinados = Subordinados()
        subordinados.removerSubordinados(form.vars.subordinados)
        redirect(URL('subordinados', 'index'))

        session.flash = "Servidores removidos com sucesso."

    return dict(lista=form)

