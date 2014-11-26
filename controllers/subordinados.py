# coding=utf-8
from gluon.html import *
from Subordinados import Subordinados
from gluon.validators import IS_NOT_EMPTY


def index():
    if not session.subordinados:
        session.flash = "Você não possui subordinados."
        redirect(URL('default', 'index'))

    session.avaliacao = None

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
        P("Clique no botão abaixo para remover os seridores da lista."),
        INPUT(_type="submit", _value=db(db.TIPOS_EXCLUSAO.id == 1).select(db.TIPOS_EXCLUSAO.TIPO).first().TIPO, _name="submit1"),
        INPUT(_type="submit", _value=db(db.TIPOS_EXCLUSAO.id == 2).select(db.TIPOS_EXCLUSAO.TIPO).first().TIPO, _name="submit2")
    )

    if form.process().accepted:
        subordinados = Subordinados()
        siapes = form.vars.subordinados if isinstance(form.vars.subordinados, list) else [form.vars.subordinados]
        # TODO: 1 if bla else 2... GAMBIARRA DO CARALHO ! Remover esta merda e os dois botões acima.
        subordinados.removerSubordinados(
            siapes,
            1 if form.vars.submit1 else 2,
            form.vars.OBSERVACAO
        )
        redirect(URL('subordinados', 'index'))

        session.flash = "Servidores removidos com sucesso."

    return dict(lista=form)


def informarProgepe():
    from MailAvaliacao import MailPROGEPE

    form = FORM(
        LABEL("SIAPE: ", _for='siape'),
        INPUT(_name='siape', requires=IS_NOT_EMPTY()),
        LABEL("Nome: ", _for='nome'),
        INPUT(_name='nome', requires=IS_NOT_EMPTY()),
        BR(),
        INPUT(_type='submit', _value='Enviar comunicado')
    )

    if form.process().accepted:
        email = MailPROGEPE(session.dadosServidor)
        email.sendInformativoPROGEP(form.vars.siape, form.vars.nome)

        session.flash = 'Comunicado enviado com sucesso para PROGEPE.'
        redirect(URL('subordinados', 'index'))

    return dict(form=form)
