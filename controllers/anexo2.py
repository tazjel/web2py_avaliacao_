# coding=utf-8
from Avaliacao import Avaliacao
from FormAvaliacao import FormAvaliacao
from datetime import date


@auth.requires_login()
def index():
    if not session.avaliacao:
        session.flash = 'Você precisa selecionar uma avaliação e um ano de exercício para acessar este formulário.'
        redirect(URL('default', 'index'))

    if not session.avaliacaoTipo == 'autoavaliacao':
        session.flash = 'Este formulário não pode ser acessado pela chefia.'
        redirect(URL('default', 'index'))

    form = FormAvaliacao(session.servidorAvaliado).formAnexo2
    form.add_button('Última Página', URL('anexo1', 'pagina3'))

    if form.process().accepted:
        avaliacao = Avaliacao(session.ANO_EXERCICIO, session.servidorAvaliado['SIAPE_SERVIDOR'])
        avaliacao.salvarModificacoes(form.vars)
        redirect(URL('anexo1', 'pagina2'))

    return dict(form=form)