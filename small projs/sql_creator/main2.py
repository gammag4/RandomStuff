from sql_creator import *

tables = [
    Table(
        'book(:isbn, name, author, price, stock_amount)',
        [
            NumberGenerator(10000000000, 99999999999, 1),
            SequentialTextGenerator('Livro'),
            RangeGenerator(
                SequentialTextGenerator('Autor').getRange(1, 6)
            ),
            NumberGenerator(0.59, 120, 0.01),
            NumberGenerator(0, 200, 1)
        ],
        80
    ),
    Table(
        'employee(:id, name, salary, phone)',
        [
            NumberGenerator(100000000, 999999999, 1),
            SequentialTextGenerator('Funcionário'),
            NumberGenerator(1200, 6000, 0.01),
            PhoneGenerator()
        ],
        5
    ),
    Table(
        'customer(:id, name, phone)',
        [
            NumberGenerator(100000000, 999999999, 1),
            SequentialTextGenerator('Cliente'),
            PhoneGenerator()
        ],
        30
    ),
    Table(
        'sale(:customer_id, :employee_id, date)',
        [
            'customer',
            'employee',

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
