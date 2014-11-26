# -*- coding: utf-8 -*-
from gluon import current


db.define_table('PERIODOS_ABERTOS_AVAL',
                Field('ANO_EXERCICIO', 'integer'),
                Field('DT_INICIO', 'date'),
                Field('DT_FIM', 'date'),
                primarykey=['ANO_EXERCICIO']
)

db.define_table('AVAL_ANEXO_1',
                Field('NOTA_FINAL', 'float', readable=True, writable=True),
                Field('DATA_DOCUMENTO', 'date', readable=True, required=True, writable=True, notnull=True),
                Field('ANO_EXERCICIO', db.PERIODOS_ABERTOS_AVAL),
                Field('SIAPE_CHEFIA', 'integer', readable=True, notnull=True),
                Field('CIENTE_CHEFIA', 'string', length=1, writable=True, readable=True, default='F'),
                Field('SUGESTOES_CHEFIA', 'string', length=4096, writable=True, readable=True),
                Field('INFO_COMPLEMENTAR_CHEFIA', 'string', length=4096, writable=True, readable=True),
                Field('NOTA_ASSIDUIDADE_CHEFIA', 'integer', required=False, requires=True, writable=True,
                      readable=True),
                Field('NOTA_COMPROMISSO_CHEFIA', 'integer', required=False, requires=True, writable=True,
                      readable=True),
                Field('NOTA_CONHECIMENTO_CHEFIA', 'integer', required=False, requires=True, writable=True,
                      readable=True),
                Field('NOTA_DESENVOLVIMENTO_CHEFIA', 'integer', required=False, requires=True, writable=True,
                      readable=True),
                Field('NOTA_INICIATIVA_CHEFIA', 'integer', required=False, requires=True, writable=True, readable=True),
                Field('NOTA_ORGANIZACAO_CHEFIA', 'integer', required=False, requires=True, writable=True,
                      readable=True),
                Field('NOTA_PRODUTIVIDADE_CHEFIA', 'integer', required=False, requires=True, writable=True,
                      readable=True),
                Field('NOTA_RESPONSABILIDADE_CHEFIA', 'integer', required=False, requires=True, writable=True,
                      readable=True),
                Field('NOTA_RELACIONAMENTO_CHEFIA', 'integer', required=False, requires=True, writable=True,
                      readable=True),
                Field('SIAPE_SERVIDOR', 'integer', notnull=True),
                Field('CIENTE_SERVIDOR', 'string', length=1, writable=True, readable=True, default='F'),
                Field('SUGESTOES_SERVIDOR', 'string', length=4096, writable=True, readable=True),
                Field('INFO_COMPLEMENTAR_SERVIDOR', 'string', length=4096, writable=True, readable=True),
                Field('NOTA_ASSIDUIDADE', 'integer', required=False, requires=True, writable=True, readable=True),
                Field('NOTA_COMPROMISSO', 'integer', required=False, requires=True, writable=True, readable=True),
                Field('NOTA_CONHECIMENTO', 'integer', required=False, requires=True, writable=True, readable=True),
                Field('NOTA_DESENVOLVIMENTO', 'integer', required=False, requires=True, writable=True, readable=True),
                Field('NOTA_INICIATIVA', 'integer', required=False, requires=True, writable=True, readable=True),
                Field('NOTA_ORGANIZACAO', 'integer', required=False, requires=True, writable=True, readable=True),
                Field('NOTA_PRODUTIVIDADE', 'integer', required=False, requires=True, writable=True, readable=True),
                Field('NOTA_RESPONSABILIDADE', 'integer', required=False, requires=True, writable=True, readable=True),
                Field('NOTA_RELACIONAMENTO', 'integer', required=False, requires=True, writable=True, readable=True),
                Field('FATOR_ILUMINACAO', 'string', length=1),
                Field('FATOR_TEMPERATURA', 'string', length=1),
                Field('FATOR_RUIDOS', 'string', length=1),
                Field('FATOR_INSTALACOES', 'string', length=1),
                Field('FATOR_EQUIPAMENTOS', 'string', length=1),
                Field('INFO_COMPLEMENTARES', 'string', length=4096)
)

db.define_table("TIPOS_EXCLUSAO",
    Field("TIPO", "string"),
    Field("DESCRICAO", "text")
)

db.define_table("SUBORDINADOS_EXCLUIR",
    Field('SIAPE_SERVIDOR', 'integer'),
    Field('SIAPE_CHEFIA_TITULAR', 'integer'),
    Field('OBSERVACAO', 'text'),
    Field('UNIDADE_EXERCICIO_SERVIDOR', 'string'),
    Field('TIPO', db.TIPOS_EXCLUSAO)
)



current.db = db

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

# # create all tables needed by auth if not custom tables
auth.define_tables(username=True)
auth.settings.create_user_groups = False

# # configure email
mail = auth.settings.mailer
# mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.server = 'smtp.gmail.com:587'  # 'logging'
mail.settings.sender = 'naoresponder.avaliacao@unirio.br'         # your email
mail.settings.login = 'naoresponder.avaliacao@unirio.br:' + emailPass      # your credentials or None

current.mail = mail

# Se a requisição for local, utiliza base auth de teste, caso contrário, utiliza LDAP

if not request.is_local:
    from gluon.contrib.login_methods.ldap_auth import ldap_auth
    auth.settings.login_methods = [ldap_auth(mode='uid', server='10.224.16.100', base_dn='ou=people,dc=unirio,dc=br')]

from Servidor import Servidor
db.auth_user.username.label = 'CPF'
auth.settings.actions_disabled = ['register',
                                  'retrieve_username',
                                  'remember_me',
                                  'profile',
                                  'change_password',
                                  'request_reset_password']

auth.settings.remember_me_form = False
# login_next Não está funcionando e segundo a documentação, deveria funcionar
auth.settings.login_next = URL('default', 'mensagem')
# Faço o redirect para URL acima, no método abaixo
auth.settings.login_onaccept = Servidor().getDadosToSession()

