
from gluon.tools import Crud

@auth.requires(auth.has_membership('PROGEPE') or auth.has_membership('DTIC'))
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

@auth.requires(auth.has_membership('PROGEPE') or auth.has_membership('DTIC'))
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
