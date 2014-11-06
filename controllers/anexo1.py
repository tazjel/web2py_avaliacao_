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
        else:
            """Caso alguém tente acessar esta página pulando a fase de seleção de tipo de avaliação..."""
            redirect(URL('default', 'index'))

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
                year=int(session.ANO_EXERCICIO))


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

    if form.process().accepted:
        avaliacao = Avaliacao(session.ANO_EXERCICIO, session.servidorAvaliado['SIAPE_SERVIDOR'])
        avaliacao.salvarModificacoes(form.vars)

        try:
            # Ao final de uma avaliacao
            email = MailAvaliacao(avaliacao)
            email.sendConfirmationEmail()
        except Exception:
            session.flash += ' Não foi possível enviar o email de confirmação. Verifique se o servidor ' \
                             'possui email cadastrado e indicador de correspondência marcado.'

        if session.avaliacaoTipo == 'subordinados':
            redirect(URL('subordinados', 'index'))
        elif session.avaliacaoTipo == 'autoavaliacao':
            redirect(URL('default', 'index'))

    return dict(form=form,
                resumo=formAvaliacao.resumoTable if session.avaliacaoTipo == 'autoavaliacao' else "",
                data=date.today())