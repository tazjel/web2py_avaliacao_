
from gluon.tools import Crud


def avaliacaoes():
    busca = SQLFORM.grid(
        db.AVAL_ANEXO_1,
        deletable=False,
        editable=False,
        create=False,
        fields=[
            db.AVAL_ANEXO_1.id,
            db.AVAL_ANEXO_1.ANO_EXERCICIO,
            db.AVAL_ANEXO_1.SIAPE_SERVIDOR,
            db.AVAL_ANEXO_1.SIAPE_CHEFIA
        ],
        orderby=db.AVAL_ANEXO_1.DATA_DOCUMENTO,
        paginate=50
    )
    return dict(busca=busca)


def naoFinalizadas():
    from gluon.tools import Crud

    crud = Crud(db)

    avaliacaoes = crud.select(db.AVAL_ANEXO_1,
                              db.AVAL_ANEXO_1.CIENTE_SERVIDOR == 'F',
                              fields=[
                                  db.AVAL_ANEXO_1.id,
                                  db.AVAL_ANEXO_1.ANO_EXERCICIO,
                                  db.AVAL_ANEXO_1.SIAPE_SERVIDOR,
                                  db.AVAL_ANEXO_1.SIAPE_CHEFIA
                              ]
    )
    return dict(avaliacoes=avaliacaoes)


def estatisticas():
    import pygal
    from pygal.style import CleanStyle
    from statistics import mean, median, mode

    fields = ["NOTA_ASSIDUIDADE_CHEFIA", "NOTA_COMPROMISSO_CHEFIA", "NOTA_CONHECIMENTO_CHEFIA",
              "NOTA_DESENVOLVIMENTO_CHEFIA", "NOTA_INICIATIVA_CHEFIA", "NOTA_ORGANIZACAO_CHEFIA",
              "NOTA_PRODUTIVIDADE_CHEFIA", "NOTA_RESPONSABILIDADE_CHEFIA", "NOTA_ASSIDUIDADE",
              "NOTA_COMPROMISSO", "NOTA_CONHECIMENTO", "NOTA_DESENVOLVIMENTO", "NOTA_INICIATIVA",
              "NOTA_ORGANIZACAO", "NOTA_PRODUTIVIDADE", "NOTA_RESPONSABILIDADE", "NOTA_RELACIONAMENTO"]

    avals = db(db.AVAL_ANEXO_1.CIENTE_SERVIDOR == 'T').select(
        *[db.AVAL_ANEXO_1[x] for x in fields]
    )

    notas = dict.fromkeys(fields, [])
    for aval in avals:
        for nota in aval:
            notas[nota].append(aval[nota])

    means = [mean(nota) for k, nota in notas.iteritems()]
    medians = [median(nota) for k, nota in notas.iteritems()]
    modes = [mode(nota) for k, nota in notas.iteritems()]

    response.headers['Content-Type'] = 'image/svg+xml'

    bar_chart = pygal.Bar(style=CleanStyle)  # Then create a bar graph object
    bar_chart.x_labels = fields
    bar_chart.x_label_rotation = 90
    bar_chart.add('Media', means)
    bar_chart.add('Mediana', medians)
    bar_chart.add('Moda', modes)
    return bar_chart.render()


    # box_plot = pygal.Box(
    #     range=(0,10),
    #     legend_font_size=8
    # )
    # box_plot.title = 'Desempenho dos servidores'
    # [box_plot.add(k,v) for k, v in notas.iteritems()]
    # return box_plot.render()