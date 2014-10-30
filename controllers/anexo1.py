# coding=utf-8
from Avaliacao import Avaliacao
from FormAvaliacao import FormAvaliacao
from datetime import date


@auth.requires_login()
def index():
    if not session.avaliacao:
        if session.avaliacaoTipo == 'subordinados':
            siapeServidor = request.vars.SIAPE_SERVIDOR
        elif session.avaliacaoTipo == 'autoavaliacao':
            siapeServidor = session.dadosServidor["SIAPE_SERVIDOR"]

        avaliacao = Avaliacao(session.ANO_EXERCICIO, siapeServidor)
        session.avaliacao = avaliacao.dados

    form = FormAvaliacao(session.servidorAvaliado).formIdentificao
    form.add_button('Voltar', URL('default', 'index'))

    if form.process().accepted:
        if session.avaliacaoTipo == 'subordinados':
            redirect(URL('anexo1', 'pagina2'))
        elif session.avaliacaoTipo == 'autoavaliacao' and Avaliacao.isChefiaCiente():
            redirect(URL('anexo2', 'index'))
        else:
            session.flash = "Sua chefia imediata ainda não enviou sua avaliação."
            redirect(URL('default', 'index'))

    return dict(form=form,
                year=date.today().year)


@auth.requires_login()
def pagina2():
    if not session.avaliacao:
        session.flash = 'Você precisa selecionar uma avaliação e um ano de exercício para acessar este formulário.'
        redirect(URL('default', 'index'))

    form = FormAvaliacao(session.servidorAvaliado).formPagina2
    form.add_button('Voltar', URL('anexo2', 'index'))

    if form.process().accepted:
        avaliacao = Avaliacao(session.ANO_EXERCICIO, session.servidorAvaliado['SIAPE_SERVIDOR'])
        avaliacao.salvarModificacoes(form.vars)
        redirect(URL("anexo1", "pagina3"))

    return dict(form=form)


@auth.requires_login()
def pagina3():
    from MailAvaliacao import MailAvaliacao

    if not session.avaliacao:
        session.flash = 'Você precisa selecionar uma avaliação e um ano de exercício para acessar este formulário.'
        redirect(URL('default', 'index'))

    formAvaliacao = FormAvaliacao(session.servidorAvaliado)
    form = formAvaliacao.formPagina3
    form.add_button('Voltar', URL('anexo1', 'pagina2'))
    form.add_button('Primeira Página', URL('anexo2', 'index'))

    resumo = formAvaliacao.resumoTable

    if form.process().accepted:
        avaliacao = Avaliacao(session.ANO_EXERCICIO, session.servidorAvaliado['SIAPE_SERVIDOR'])
        avaliacao.salvarModificacoes(form.vars)

        # Ao final de uma avaliacao
        email = MailAvaliacao(avaliacao)
        email.sendConfirmationEmail()

        if session.avaliacaoTipo == 'subordinados':
            redirect(URL('subordinados', 'index'))
        elif session.avaliacaoTipo == 'autoavaliacao':
            redirect(URL('default', 'index'))

    return dict(form=form,
                resumo=resumo,
                data=date.today())