# -*- coding: utf-8 -*-
from Avaliacao import Avaliacao
from gluon import current
from gluon.validators import IS_INT_IN_RANGE, IS_NOT_EMPTY
from gluon.html import *


class FormAvaliacao(object):
    def __init__(self, servidor):
        self.servidor = servidor
        # TODO Por causa de um UnicodeEncodeError, foi necessário colocar essa gambi. Resolver ou utilizar DBSM.REMOVEACENTOS na View
        self.tipo = current.session.avaliacaoTipo

    @property
    def formIdentificao(self):
        return FORM(
            FIELDSET(
                LEGEND('1. Identificação do Servidor Avaliado'),
                LABEL('Nome: ', _for='nome'),
                INPUT(_name='NOME_SERVIDOR', _type='text', _value=self.servidor['NOME_SERVIDOR'].encode('utf8'),
                      _readonly='true'),
                BR(),
                LABEL('Matrícula SIAPE: ', _for='siape'),
                INPUT(_name='SIAPE_SERVIDOR', _type='text', _value=self.servidor['SIAPE_SERVIDOR'],
                      _readonly='true'),
                BR(),
                LABEL('Cargo: ', _for='cargo'),
                INPUT(_name='CARGO_SERVIDOR', _type='text', _value=self.servidor['CARGO_SERVIDOR'].encode('utf8'),
                      _readonly='true'),
                BR(),
                LABEL('Unidade em exercício: ', _for='unidade'),
                INPUT(_name='UNIDADE_EXERCICIO_SERVIDOR', _type='text',
                      _value=self.servidor['UNIDADE_EXERCICIO_SERVIDOR'].encode('utf8'), _readonly='true'),
                BR(),
                LABEL('E-mail: ', _for='EMAIL_SERVIDOR'),
                INPUT(_name='EMAIL_SERVIDOR', _type='text',
                      _value=self.servidor['EMAIL_SERVIDOR'].encode('utf8'), _readonly='true'),
                BR(),
                _class='dadosServidor'),
            FIELDSET(
                LEGEND('2. Identificação da Chefia Imediata'),
                LABEL('Nome: ', _for='nome'),
                INPUT(_name='CHEFIA_TITULAR', _type='text', _value=self.servidor['CHEFIA_TITULAR'].encode('utf8'),
                      _readonly='true'),
                BR(),
                LABEL('Matrícula SIAPE: ', _for='siape'),
                INPUT(_name='SIAPE_CHEFIA', _type='text', _value=self.servidor['SIAPE_CHEFIA_TITULAR'],
                      _readonly='true'),
                BR(),
                LABEL('Unidade em exercício: ', _for='unidade'),
                INPUT(_name='UNIDADE_EXERCICIO_CHEFIA', _type='text',
                      _value=self.servidor['UNIDADE_EXERCICIO_CHEFIA'].encode('utf8'), _readonly='true'),
                BR(),
                LABEL('E-mail: ', _for='EMAIL_CHEFIA_TITULAR'),
                INPUT(_name='EMAIL_CHEFIA_TITULAR', _type='text',
                      _value=self.servidor['EMAIL_CHEFIA_TITULAR'].encode('utf8'), _readonly='true'),
                BR(),
                _class='dadosServidor'), BR(),

                BR(),
            INPUT(_value='Próximo', _type='submit')
        )

    @property
    def resumoTable(self):
        if not self.tipo == 'subordinados':
            return TABLE(
                TBODY(
                    TR(
                        TD('Fatores'),
                        TD('Pontos por Fator**')
                        , _class='tableHeader'
                    ),
                    TR(
                        TD('1 - Assiduidade/Pontualidade', _class='cellTitle'),
                        TD(Avaliacao.pontosPorFator('ASSIDUIDADE'))
                    ),
                    TR(
                        TD('2 - Compromisso com qualidade', _class='cellTitle'),
                        TD(Avaliacao.pontosPorFator('COMPROMISSO'))
                    ),
                    TR(
                        TD('3 - Conhecimento', _class='cellTitle'),
                        TD(Avaliacao.pontosPorFator('CONHECIMENTO'))
                    ),
                    TR(
                        TD('4 - Cooperação/Desenvolvimento', _class='cellTitle'),
                        TD(Avaliacao.pontosPorFator('DESENVOLVIMENTO'))
                    ),
                    TR(
                        TD('5 - Iniciativa', _class='cellTitle'),
                        TD(Avaliacao.pontosPorFator('INICIATIVA'))
                    ),
                    TR(
                        TD('6 - Organização/Planejamento', _class='cellTitle'),
                        TD(Avaliacao.pontosPorFator('ORGANIZACAO'))
                    ),
                    TR(
                        TD('7 - Produtividade/Eficiência', _class='cellTitle'),
                        TD(Avaliacao.pontosPorFator('PRODUTIVIDADE'))
                    ),
                    TR(
                        TD('8 - Responsabilidade', _class='cellTitle'),
                        TD(Avaliacao.pontosPorFator('RESPONSABILIDADE'))
                    ),
                    TR(
                        TD('9 - Relacionamento Interpessoal', _class='cellTitle'),
                        TD(Avaliacao.pontosPorFator('RELACIONAMENTO'))
                    ),
                    TR(
                        TD('Nota final'),
                        TD(Avaliacao.notaFinal())
                        , _class='tableFooter')
                )
                , _class='greyTableSmall')

    def notaForColumn(self, column):
        """


        :rtype : int
        :param column: Nome de uma
        :return: inteiro relativo a nota requisitada
        """
        if current.session.avaliacao and column in current.session.avaliacao and current.session.avaliacao[column]:
            return int(current.session.avaliacao[column])

    def contentForColumn(self, column):
        """
        Dada uma determianda coluna, retorna a string com seu valor, ou uma string vazia
        :param column:
        :return:
        """
        if current.session.avaliacao and column in current.session.avaliacao and current.session.avaliacao[column]:
            return current.session.avaliacao[column]

    def columnShouldBeReadonlyForCurrentSession(self, column):
        """
        Caso o tipo de avaliação seja uma Autoavaliação e a coluna seja do tipo CHEFIA,
        o campo deve ser readonly para a sessão em questão. O mesmo se aplica, caso o usuário
        em questão seja um chefe avaliando um subordinado.
        Caso o campo deva ser preenchido pelo servidor da sessao mas o mesmo já finalizou a
        sua avaliacao e deu o seu CIENTE, o campo deve ser apresentado como readonly

        :rtype : bool
        :param column: uma coluna do banco AVAL_ANEXO_1
        :return:
        """
        if Avaliacao.columnNeedChefia(column) and self.tipo == 'autoavaliacao':
            return True
        elif not Avaliacao.columnNeedChefia(column) and self.tipo == 'subordinados':
            return True
        elif not Avaliacao.columnNeedChefia(column) and self.tipo == 'autoavaliacao':
            if 'CIENTE_SERVIDOR' in current.session.avaliacao and current.session.avaliacao['CIENTE_SERVIDOR'] == 'T':
                return True
        elif Avaliacao.columnNeedChefia(column) and self.tipo == 'subordinados':
            if 'CIENTE_CHEFIA' in current.session.avaliacao and current.session.avaliacao['CIENTE_SERVIDOR'] == 'T':
                return True

    def printNotasSelectBox(self, column):
        """
        Dada uma sessão de usuário e o tipo de avaliação, a função retorna um SELECT para que seja
        efetuada a seleção de uma nota, caso o usuário possa editar ou um INPUT com atributo readonly.

        :type column: str
        :param column: uma coluna do banco AVAL_ANEXO_1
        :rtype: gluon.html.INPUT
        :return: SELECT ou INPUT de uma nota
        """

        extraClass = "chefia" if Avaliacao.columnNeedChefia(column) else "servidor"
        if self.columnShouldBeReadonlyForCurrentSession(column):
            return INPUT(_name=column, _value=self.notaForColumn(column), _type='text', _readonly=ON,
                         _class='notaField ' + extraClass)
        else:
            # TODO refazer forma como essa lista e opção está sendo criar por solução mais elegante
            options = [""]
            options.extend(range(0, 11))
            return SELECT(options, _name=column, value=self.notaForColumn(column), _class='notaSelect ' + extraClass,
                          requires=IS_INT_IN_RANGE(0, 11, error_message='A nota deve ser um número entre 0 e 10'))

    def printTextarea(self, column):
        """

        :type column: str
        :param column: uma coluna do banco AVAL_ANEXO_1
        :rtype : gluon.html.TEXTAREA
        :return: TEXTAREA com o conteúdo de uma coluna
        """
        if self.columnShouldBeReadonlyForCurrentSession(column):
            return TEXTAREA(_name=column, value=self.contentForColumn(column), _readonly=ON)
        else:
            return TEXTAREA(_name=column, value=self.contentForColumn(column))

    def printCienteInput(self):
        """

        :rtype : gluon.html.DIV
        """
        if self.tipo == 'subordinados':
            column = 'CIENTE_CHEFIA'
        elif self.tipo == 'autoavaliacao':
            column = 'CIENTE_SERVIDOR'

        if not Avaliacao.isCiente():
            # Removi _checked=v por não achar necessário. Caso haja algum problema, reavaliar necessidade
            return INPUT(_name=column, _value='T', _type='checkbox', requires=IS_NOT_EMPTY())
        else:
            return IMG(_src=URL('static/images', 'checked.png'), _alt='Ciente')

    @property
    def formPagina2(self):
        return FORM(
            TABLE(
                TR(
                    TD('Fatores', _rowspan=2),
                    TD('Muito Bom', BR(), '9 - 10', _rowspan=2),
                    TD('Bom', BR(), '7 - 8', _rowspan=2),
                    TD('Regular', BR(), '5 - 6', _rowspan=2),
                    TD('Ruim', BR(), '0 - 4', _rowspan=2),
                    TD('Pontos', _colspan=2),
                    TD('Pontos por Fator**', _rowspan=2), _class='tableHeader'
                ),
                TR(
                    TD('Servidor'),
                    TD('Chefia'), _class='tableHeader'
                ),
                TR(
                    TD(
                        SPAN('1. Assiduidade/Pontualidade', _class='cellTitle'),
                        SPAN(
                            'Comparecimento com regularidade e exatidão ao lugar onde tem de desempenhar suas tarefas em horário determinado')
                    ),
                    TD('Não registra faltas nem atrasos'),
                    TD(
                        'Suas faltas, saídas antecipadas e/ou atrasos ocorrem de maneira justificada, dentro dos limites possíveis.'),
                    TD(
                        'Suas faltas, saídas antecipadas e/ou atrasos as vezes ultrapassam os limites possíveis da Instituição,  às vezes injustificados.'),
                    TD(
                        'Suas faltas, saídas antecipadas e/ou atrasos são injustificados ultrapassando os limites da Instituição.'),
                    TD(self.printNotasSelectBox('NOTA_ASSIDUIDADE')),  # db.NOTA_ASSIDUIDADE
                    TD(self.printNotasSelectBox('NOTA_ASSIDUIDADE_CHEFIA')),  # db.NOTA_ASSIDUIDADE_CHEFIA
                    TD(SPAN('10', _class='ppf NOTA_ASSIDUIDADE'))
                ),
                TR(
                    TD(
                        SPAN('2. Compromisso com qualidade', _class='cellTitle'),
                        SPAN('Trabalho executado com exatidão, clareza e correção dentro de prazos estabelecidos')
                    ),
                    TD(
                        'Realiza suas atividades sempre visando o compromisso com a qualidade do trabalho, reconhecendo as falhas como desafio do processo que precisam ser superados'),
                    TD(
                        'Procura realizar suas atividades visando a qualidade do trabalho, mas nem sempre os prazos são respeitados'),
                    TD(
                        'Realiza esforços para realizar as atividades com qualidade, necessitando de constante supervisão para superar as falhas e cumprir prazos'),
                    TD('Não se esforça em realizar suas atividades com compromisso e qualidade'),
                    TD(self.printNotasSelectBox('NOTA_COMPROMISSO')),  # db.NOTA_COMPROMISSO
                    TD(self.printNotasSelectBox('NOTA_COMPROMISSO_CHEFIA')),
                    # db.NOTA_ASSIDUIDADE_CHEFIA
                    TD(SPAN('10', _class='ppf NOTA_COMPROMISSO'))
                ),
                TR(
                    TD(
                        SPAN('3. Conhecimento', _class='cellTitle'),
                        SPAN('Domínio de conhecimentos teóricos e práticos para a execução das tarefas')
                    ),
                    TD(
                        'Apresenta conhecimentos teóricos práticos adequados. Procura sempre manter-se atualizado em relação aos conhecimentos de sua área'),
                    TD(
                        'Apresenta conhecimentos necessários para o desempenho das atividades. Demonstra interesse em adquirir novos conhecimentos em sua área'),
                    TD(
                        'Apresenta conhecimentos “essenciais” para o desempenho das suas atividades e só adquire novos conhecimentos quando há exigência superior'),
                    TD(
                        'Não apresenta conhecimentos para o desempenho de suas atividades e não demonstra interesse em adquirir novos conhecimentos em sua área'),
                    TD(self.printNotasSelectBox('NOTA_CONHECIMENTO')),
                    TD(self.printNotasSelectBox('NOTA_CONHECIMENTO_CHEFIA')),
                    TD(SPAN('10', _class='ppf NOTA_CONHECIMENTO'))
                ),
                TR(
                    TD(
                        SPAN('4. Cooperação/Desenvolvimento', _class='cellTitle'),
                        SPAN('Colaboração com o grupo de trabalho e envolvimento nas tarefas a serem executadas')
                    ),
                    TD('Coopera e se envolve nas atividades, ultrapassando as expectativas.'),
                    TD('Coopera e se envolve nas atividades de maneira satisfatória'),
                    TD(
                        'Nem sempre coopera e se envolve com as atividades . Precisa, por vezes, ser chamado a colaborar'),
                    TD('Não coopera. Precisa ser constantemente solicitado mesmo nas atividades rotineiras'),
                    TD(self.printNotasSelectBox('NOTA_DESENVOLVIMENTO')),
                    TD(self.printNotasSelectBox('NOTA_DESENVOLVIMENTO_CHEFIA')),
                    TD(SPAN('10', _class='ppf NOTA_DESENVOLVIMENTO'))
                ),
                TR(
                    TD(
                        SPAN('5. Iniciativa', _class='cellTitle'),
                        SPAN('Capacidade de propor ou empreender uma ação, sem que tenha sido solicitado para isso')
                    ),
                    TD('Antecipa-se na resolução de problemas que influenciam diretamente no seu trabalho'),
                    TD('Frequentemente resolve os problemas pertinentes a sua função'),
                    TD(
                        'Tem pouca iniciativa. De vez em quando resolve pequenos problemas, mas na maioria das vezes aguarda ordens'),
                    TD(
                        'Não faz nada sem que tenha sido solicitado ou explicado. Deixa pequenos problemas tomarem vulto aguardando solução de alguém'),
                    TD(self.printNotasSelectBox('NOTA_INICIATIVA')),
                    TD(self.printNotasSelectBox('NOTA_INICIATIVA_CHEFIA')),
                    TD(SPAN('10', _class='ppf NOTA_INICIATIVA'))
                ),
                TR(
                    TD(
                        SPAN('6. Organização/Planejamento', _class='cellTitle'),
                        SPAN(
                            'Capacidade de estabelecer prioridades e planejar ações na melhor forma de execução das tarefas')
                    ),
                    TD('Planeja e organiza as ações de sua área de trabalho visando o desenvolvimento de toda UNIRIO'),
                    TD('Planeja e organiza as ações relacionadas ao desenvolvimento de sua área de trabalho'),
                    TD('Planeja e/ou organiza as ações de sua área de trabalho necessitando  constante revisão'),
                    TD('Não planeja e organiza as ações de sua área de trabalho'),
                    TD(self.printNotasSelectBox('NOTA_ORGANIZACAO')),
                    TD(self.printNotasSelectBox('NOTA_ORGANIZACAO_CHEFIA')),
                    TD(SPAN('10', _class='ppf NOTA_ORGANIZACAO'))
                ),
                TR(
                    TD(
                        SPAN('7. Produtividade/Eficiência', _class='cellTitle'),
                        SPAN(
                            'Quantidade de trabalho realizado, dentro dos padrões estabelecidos para a função utilizando os recursos necessários.')
                    ),
                    TD('Realiza as tarefas atribuídas com total aproveitamento dos recursos'),
                    TD('Realiza as tarefas atribuídas com satisfatório aproveitamento dos recursos'),
                    TD(
                        'Realiza a maior parte das tarefas atribuídas utilizando os recursos de forma pouco satisfatória'),
                    TD('Realiza as tarefas atribuídas com dificuldade e utiliza os recursos insatisfatoriamente'),
                    TD(self.printNotasSelectBox('NOTA_PRODUTIVIDADE')),
                    TD(self.printNotasSelectBox('NOTA_PRODUTIVIDADE_CHEFIA')),
                    TD(SPAN('10', _class='ppf NOTA_PRODUTIVIDADE'))
                ),
                TR(
                    TD(
                        SPAN('8. Responsabilidade', _class='cellTitle'),
                        SPAN('Cumprimento dos deveres e obrigações relacionados ao exercício das tarefas')
                    ),
                    TD('Destaca-se pelo cumprimento dos deveres e obrigações no que se refere ao trabalho'),
                    TD('Cumpre satisfatoriamente seus deveres e obrigações no que se refere ao trabalho'),
                    TD('Nem sempre cumpre seus deveres e obrigações no que se refere ao trabalho'),
                    TD('Não se empenha em cumprir seus deveres e obrigações no que se refere ao trabalho'),
                    TD(self.printNotasSelectBox('NOTA_RESPONSABILIDADE')),
                    TD(self.printNotasSelectBox('NOTA_RESPONSABILIDADE_CHEFIA')),
                    TD(SPAN('10', _class='ppf NOTA_RESPONSABILIDADE'))
                ),
                TR(
                    TD(
                        SPAN('9. Relacionamento Interpessoal', _class='cellTitle'),
                        SPAN(
                            'Habilidade no trato com pessoas independente do nível hierárquico, profissional ou social')
                    ),
                    TD(
                        'Sabe lidar e estabelecer relações com as diferentes pessoas no ambiente de trabalho. È um facilitador'),
                    TD(
                        'Interage com os colegas e chefia de trabalho com respeito e colaboração, facilitando o trabalho em equipe'),
                    TD('Se relaciona com respeito ao grupo de trabalho, interagindo somente quando solicitado'),
                    TD('Assume comportamentos conflituosos no grupo de trabalho gerando constante insatisfação.'),
                    TD(self.printNotasSelectBox('NOTA_RELACIONAMENTO')),
                    TD(self.printNotasSelectBox('NOTA_RELACIONAMENTO_CHEFIA')),
                    TD(SPAN('10', _class='ppf NOTA_RELACIONAMENTO'))
                ), _class='greyTable'
            ),
            INPUT(_value='Próximo', _type='submit'),
        )

    @property
    def formPagina3(self):
        return FORM(
            FIELDSET(
                LEGEND('10. Conclusões e informações complementares sobre o desempenho do servidor avaliado'),
                LABEL('Servidor: ', _for='INFO_COMPLEMENTAR_SERVIDOR'),
                self.printTextarea('INFO_COMPLEMENTAR_SERVIDOR'), BR(),
                LABEL('Chefia: ', _for='INFO_COMPLEMENTAR_CHEFIA'), BR(),
                self.printTextarea('INFO_COMPLEMENTAR_CHEFIA')
            ),
            FIELDSET(
                LEGEND('11. Sugestões para melhoria do desempenho do servidor avaliado'),
                LABEL('Servidor: ', _for='SUGESTOES_SERVIDOR'),
                self.printTextarea('SUGESTOES_SERVIDOR'), BR(),
                LABEL('Chefia: ', _for='SUGESTOES_CHEFIA'), BR(),
                self.printTextarea('SUGESTOES_CHEFIA')
            ),
            FIELDSET(
                LEGEND('12. Resultado da avaliação de desempenho individual'),
                DIV('Declaro que li e concordo com todos os itens desta avaliação: ',
                    self.printCienteInput()
                    , _class='centered important'
                )
            ),
            INPUT(_value='Enviar', _type='submit')
        )

    def printAnexo2RadioOptions(self, column):
        """


        :rtype : list
        :param column: uma coluna do banco AVAL_ANEXO_1
        :return: A list of form components
        """
        options = []
        checkedValue = self.contentForColumn(column)
        isReadonly = self.columnShouldBeReadonlyForCurrentSession(column)

        options.append(
            INPUT(_name=column, _type='radio', _value='s', requires=IS_NOT_EMPTY(), _disabled=isReadonly,
                  value=checkedValue))
        options.append('Adequada')
        options.append(
            INPUT(_name=column, _type='radio', _value='n', requires=IS_NOT_EMPTY(), _disabled=isReadonly,
                  value=checkedValue))
        options.append('Inadequada')

        return options

    @property
    def formAnexo2(self):
        return FORM(
            FIELDSET(
                LEGEND('2. Condições de trabalho oferecidas pela instituição'),
                LABEL('Iluminação: ', _for='p1'),
                TAG[''](self.printAnexo2RadioOptions('FATOR_ILUMINACAO')), BR(),
                LABEL('Temperatura: ', _for='p2'),
                TAG[''](self.printAnexo2RadioOptions('FATOR_TEMPERATURA')), BR(),
                LABEL('Ruídos: ', _for='p3'),
                TAG[''](self.printAnexo2RadioOptions('FATOR_RUIDOS')), BR(),
                LABEL('Equipamentos: ', _for='p4'),
                TAG[''](self.printAnexo2RadioOptions('FATOR_EQUIPAMENTOS')), BR(),
                LABEL('Instalações de trabalho: ', _for='p5'),
                TAG[''](self.printAnexo2RadioOptions('FATOR_INSTALACOES')), BR(),
            ),
            FIELDSET(
                LEGEND('3. Informações complementares sobre entraves que atrapalham o desenvolvimento das atividades'),
                self.printTextarea('INFO_COMPLEMENTARES')
            ),
            INPUT(_type='submit', _value='Próximo'),
            _class='anexo2'
        )
