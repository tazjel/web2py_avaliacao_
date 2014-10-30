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
        BR(),
        TEXTAREA(_placeholder="Opcional: Insira uma justificativa que ajude a interpretar a fonte do problema.", _name="OBSERVACAO"),
        P("Clique no botão abaixo para remover os seridores da lista, ou clique no nome de um servidor para iniciar sua avaliação."),
        INPUT(_type="submit", _value="Não se encontra em exercício na unidade")
    )

    if form.process().accepted:
        subordinados = Subordinados()
        siapes = form.vars.subordinados if isinstance(form.vars.subordinados, list) else [form.vars.subordinados]
        subordinados.removerSubordinados(siapes, form.vars.OBSERVACAO)
        redirect(URL('subordinados', 'index'))

        session.flash = "Servidores removidos com sucesso."

    return dict(lista=form)

