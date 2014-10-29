# coding=utf-8
from Avaliacao import Avaliacao
from FormAvaliacao import FormAvaliacao
from datetime import date


@auth.requires_login()
def index():

    if session.avaliacaoTipo == 'subordinados':
        siapeServidor = request.vars.SIAPE_SERVIDOR
    elif session.avaliacaoTipo == 'autoavaliacao':
        siapeServidor = session.dadosServidor["SIAPE_SERVIDOR"]

    avaliacao = Avaliacao(date.today().year, siapeServidor)
    session.avaliacao = avaliacao.dados

    form = FormAvaliacao().formIdentificao
    form.add_button('Voltar', URL('default', 'index'))

    if form.process().accepted:
        if session.avaliacaoTipo == 'subordinados':
            redirect(URL('anexo1', 'pagina2'))
        elif session.avaliacaoTipo == 'autoavaliacao' and avaliacao.isChefiaCiente():
            redirect(URL('anexo2', 'index'))
        else:
            session.flash = "Sua chefia imediata ainda não enviou sua avaliação."
            redirect(URL('default', 'index'))

    return dict(form=form,
                year=date.today().year)

@auth.requires_login()
def pagina2():
    if not session.avaliacao:
        avaliacao = Avaliacao(date.today().year, session.dadosServidor["SIAPE_SERVIDOR"])
        session.avaliacao = avaliacao.dados

    form = FormAvaliacao().formPagina2
    form.add_button('Voltar', URL('anexo2', 'index'))

    if form.process().accepted:
        session.avaliacao.update(form.vars)

    return dict(form=form)


@auth.requires_login()
def pagina3():
    if not session.avaliacao:
        avaliacao = Avaliacao(date.today().year, session.dadosServidor["SIAPE_SERVIDOR"])
        session.avaliacao = avaliacao.dados

    form = FormAvaliacao().formPagina3
    form.add_button('Voltar', URL('anexo1', 'pagina2'))
    form.add_button('Primeira Página', URL('anexo2', 'index'))

    if form.process().accepted:
        session.avaliacao.update(form.vars)
        response.flash = "Formulário salvo com sucesso."

    return dict(form=form,
                data=date.today())