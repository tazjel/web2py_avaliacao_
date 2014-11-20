# coding=utf-8
from datetime import date
from Avaliacao import Avaliacao
from gluon.html import OPTION


@auth.requires_login()
def index():
    session.ANO_EXERCICIO = None
    session.avaliacaoTipo = None
    session.avaliacao = None

    avaliacao = Avaliacao(date.today().year, session.dadosServidor["SIAPE_SERVIDOR"])

    form = FORM(
        BR(),
        LABEL('Exercício: ', _for='ANO_EXERCICIO'),
        SELECT([OPTION(ano.ANO_EXERCICIO, _value=ano.ANO_EXERCICIO) for ano in avaliacao.anosDeExercicio()],
               _name='ANO_EXERCICIO'),
        BR(),BR(),
        LABEL('Tipo: ', _for='avaliacaoTipo'),
        SELECT([OPTION(v, _value=k) for k, v in avaliacao.tiposDeAvaliacaoesForCurrentSession().iteritems()],
               _name='avaliacaoTipo',
               _class='avaliacaoTipo',
               _value='autoavaliacao'),
        BR(),
        INPUT(_value='Próximo', _type='submit')
    )

    if form.process().accepted:
        session.ANO_EXERCICIO = form.vars.ANO_EXERCICIO
        session.avaliacaoTipo = form.vars.avaliacaoTipo

        if form.vars.avaliacaoTipo == 'autoavaliacao':
            redirect(URL('anexo1', 'index'))

        elif form.vars.avaliacaoTipo == 'subordinados':
            redirect(URL('subordinados', 'index'))

    return dict(form=form)

def mensagem():
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(
        form=auth()
    )


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

