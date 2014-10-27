# coding=utf-8
from Avaliacao import Avaliacao
from FormAvaliacao import FormAvaliacao
from datetime import date


@auth.requires_login()
def index():
    if not session.avaliacao:
        avaliacao = Avaliacao(date.today().year, session.dadosServidor["SIAPE_SERVIDOR"])
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
    form = FormAvaliacao().formPagina2
    form.add_button('Voltar', URL('anexo2','index'))

    if form.process().accepted:
        session.avaliacao.update(form.vars)


@auth.requires_login()
def pagina3():
    pass