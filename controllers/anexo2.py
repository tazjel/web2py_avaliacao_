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

        avaliacao = Avaliacao(date.today().year, siapeServidor)
        session.avaliacao = avaliacao.dados

    form = FormAvaliacao().formAnexo2
    form.add_button('Última Página', URL('anexo1', 'pagina3'))

    if form.process().accepted:
        session.avaliacao.update(form.vars)

    return dict(form=form)