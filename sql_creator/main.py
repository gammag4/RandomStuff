from sql_creator import *

tables = [
    Table(
        'Curso(nome, totalcreditos)',
        [
            PredefinedGenerator(
                SequentialTextGenerator('Curso'),
                [
                    'Engenharia da Computação',
                    'Ciência da Computação',
                    'Administração'
                ]
            ),
            NumberGenerator(80, 161, 20)
        ],
        9
    ),
    Table(
        'Aluno(nome, endereco, cidade, telefone, numcurso)',
        [
            PredefinedGenerator(
                SequentialTextGenerator('Aluno'),
                [
                    'Marcos João Casanova',
                    'Ailton Castro',
                    'Edvaldo Carlos Silva'
                ]
            ),
            AddressGenerator(26, 150, 301, 15, 6, 3, 0.2, 0.04),
            RangeGenerator(
                SequentialTextGenerator('Cidade').getRange(1, 4)
            ),
            PhoneGenerator(),
            'Curso'
        ],
        250
    ),
    Table(
        'Professor(nome, areapesquisa)',
        [
            PredefinedGenerator(
                SequentialTextGenerator('Professor'),
                [
                    'Ramon Travanti',
                    'Marcos Salvador',
                    'Abgair'
                ]
            ),
            RangeGenerator(
                SequentialTextGenerator('Área de Pesquisa').getRange(1, 11)
            )
        ],
        35
    ),
    Table(
        'Disciplina(nome, quantcreditos)',
        [
            PredefinedGenerator(
                SequentialTextGenerator('Disciplina'),
                [
                    'Cálculo Numérico',
                    'Banco de Dados',
                    'Engenharia de Software'
                ]
            ),
            NumberGenerator(2, 9, 2)
        ],
        60
    ),
    Table(
        'DisciplinaCurso(:numdisp, :numcurso)',
        [
            'Disciplina',
            'Curso'
        ],
        150
    ),
    Table(
        'Aula(:semestre, nota, :numaluno, :numprof, :numdisp)',
        [
            RangeGenerator(
                SemesterGenerator(1997, 2000).getRange()
            ),
            NumberGenerator(2, 11),
            'Aluno',
            'Professor',
            'Disciplina'
        ],
        5000
    )
]

generator = SqlGenerator(tables)
generator.sqlToFile('./out.sql')
