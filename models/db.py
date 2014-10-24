# -*- coding: utf-8 -*-
db.define_table('PERIODOS_ABERTOS_AVAL',
                Field('ANO_EXERCICIO', 'integer'),
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
                Field('INFO_COMPLEMENTARES', 'string', length=4096),
                primarykey=['ANO_EXERCICIO', 'SIAPE_SERVIDOR']
)

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

# # create all tables needed by auth if not custom tables
auth.define_tables(username=True)
auth.settings.create_user_groups = False

# # configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.actions_disabled = ['register', 'retrieve_username', 'profile', 'lost_password']
db.auth_user.username.label = 'CPF'

from Servidor import Servidor

auth.settings.login_onaccept = Servidor().getDadosToSession()

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain

use_janrain(auth, filename='private/janrain.key')

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
