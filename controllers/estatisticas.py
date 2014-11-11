# coding=utf-8
import pygal
from pygal.style import CleanStyle
from statistics import mean, median, mode


def index():
    charts = {
        "Fatores ": A(IMG(_src=URL('estatisticas', 'fatores')), _href=URL('estatisticas', 'fatores')),
        "Notas ": A(IMG(_src=URL('estatisticas', 'notas')), _href=URL('estatisticas', 'notas')),
    }
    return dict(charts=charts)

def notas():
    fields = ["NOTA_ASSIDUIDADE_CHEFIA", "NOTA_COMPROMISSO_CHEFIA", "NOTA_CONHECIMENTO_CHEFIA",
              "NOTA_DESENVOLVIMENTO_CHEFIA", "NOTA_INICIATIVA_CHEFIA", "NOTA_ORGANIZACAO_CHEFIA",
              "NOTA_PRODUTIVIDADE_CHEFIA", "NOTA_RESPONSABILIDADE_CHEFIA", "NOTA_ASSIDUIDADE",
              "NOTA_COMPROMISSO", "NOTA_CONHECIMENTO", "NOTA_DESENVOLVIMENTO", "NOTA_INICIATIVA",
              "NOTA_ORGANIZACAO", "NOTA_PRODUTIVIDADE", "NOTA_RESPONSABILIDADE", "NOTA_RELACIONAMENTO"]

    avals = db(db.AVAL_ANEXO_1.CIENTE_SERVIDOR == 'T').select(*[db.AVAL_ANEXO_1[x] for x in fields],
                                                              cache=(cache.ram, 3600), cacheable=True)

    notas = dict.fromkeys(fields, [])
    for aval in avals:
        for nota in aval:
            notas[nota].append(aval[nota])

    means = [mean(nota) for k, nota in notas.iteritems()]
    medians = [median(nota) for k, nota in notas.iteritems()]
    # modes = [mode(nota) for k, nota in notas.iteritems()]

    response.headers['Content-Type'] = 'image/svg+xml'

    bar_chart = pygal.Bar(style=CleanStyle)  # Then create a bar graph object
    bar_chart.x_labels = fields
    bar_chart.x_label_rotation = 90
    bar_chart.add('Media', means)
    bar_chart.add('Mediana', medians)
    # bar_chart.add('Moda', modes)
    return bar_chart.render()

    # box_plot = pygal.Box(
    #     range=(0,10),
    #     legend_font_size=8
    # )
    # box_plot.title = 'Desempenho dos servidores'
    # [box_plot.add(k,v) for k, v in notas.iteritems()]
    # return box_plot.render()

def fatores():
    fields = ['FATOR_ILUMINACAO', 'FATOR_TEMPERATURA', 'FATOR_RUIDOS', 'FATOR_INSTALACOES', 'FATOR_EQUIPAMENTOS']
    avals = db(db.AVAL_ANEXO_1.CIENTE_SERVIDOR == 'T').select(*[db.AVAL_ANEXO_1[x] for x in fields],
                                                              cache=(cache.ram, 3600), cacheable=True)

    # notas = dict.fromkeys(fields, {"s": 0, "n": 0}))     # Gera uma dicionário com as chaves corretas, mas apontam todos para a mesma lista
    notas = dict((k, {"s": 0, "n": 0}) for k in fields)
    for aval in avals:
        for fator in aval:
            notas[fator][aval[fator]] += 1

    bar = pygal.Bar(style=CleanStyle)
    bar.x_labels = fields
    bar.x_label_rotation = 90
    bar.add('Adequado', [notas[v]['s'] for v in notas])
    bar.add('Inadequado', [notas[v]['n'] for v in notas])

    response.headers['Content-Type'] = 'image/svg+xml'

    return bar.render()