# coding=utf-8
from Avaliacao import Avaliacao
from FormAvaliacao import FormAvaliacao
from datetime import date


@auth.requires_login()
def index():
    if not session.avaliacao:
        avaliacao = Avaliacao(date.today().year, session.dadosServidor["SIAPE_SERVIDOR"])
        session.avaliacao = avaliacao.dados

    form = FormAvaliacao().formAnexo2
    form.add_button('Última Página', URL('anexo1', 'pagina3'))

    if form.process().accepted:
        session.avaliacao.update(form.vars)

    return dict(form=form)