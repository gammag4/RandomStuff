import random
import re


class Generator:
    def createValue(self, i, data):
        return self.getNext(i)

    def getNext(self, i):
        return None

    def getRange(self, *args):
        start = 0 if len(args) == 1 else args[0]
        stop = args[0] if len(args) == 1 else args[1]
        step = 1 if len(args) < 3 else args[2]

        values = []
        for i in range(start, stop, step):
            values.append(self.getNext(i))

        return values


class SequentialGenerator(Generator):
    def getNext(self, i):
        return i


class SequentialTextGenerator(Generator):
    def __init__(self, text):
        self.text = text

    def getNext(self, i):
        return f'{self.text} {i}'


class PhoneGenerator(Generator):
    def __init__(self, isString=False):
        self.isString = isString

    def getNext(self, i):
        number = ''
        for _ in range(9):
            number += str(random.randrange(0, 10))

        if(self.isString):
            return number

        return int(number)


class NumberGenerator(Generator):
    def __init__(self, *args):
        if len(args) == 0:
            raise Exception(
                f"Invalid amount of arguments passed to Number generator: {len(args)}"
            )

        self.start = 0 if len(args) == 1 else args[0]
        self.stop = args[0] if len(args) == 1 else args[1]
        self.step = 1 if len(args) < 3 else args[2]

    def getNext(self, i):
        return random.randrange(self.start, self.stop, self.step)


class RangeGenerator(Generator):
    def __init__(self, valueRange):
        self.valueRange = valueRange

    def getNext(self, i):
        return random.choice(self.valueRange)


class ApGenerator(Generator):
    def __init__(self, numAp, height):
        self.numAp = numAp
        self.height = height

    def getNext(self, i):
        ap = (i % self.numAp) + 1
        h = i // self.numAp
        return f'Ap {h}{str(ap).zfill(2)}'

    def getRange(self, *args):
        values = []
        for i in range(self.numAp * self.height):
            values.append(self.getNext(i))

        return values


class DateGenerator(Generator):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def getNext(self, i):
        yearS, monthS, dayS = [int(i) for i in self.start.split('-')]
        yearE, monthE, dayE = [int(i) for i in self.end.split('-')]


class SemesterGenerator(Generator):
    def __init__(self, startYear, endYear):
        self.start = startYear
        self.end = endYear

    def getNext(self, i):
        year = self.start + (i - 1) // 2
        year = str(year).zfill(4)
        sem = (i - 1) % 2 + 1
        return f'{year}.{sem}'

    def getRange(self, *args):
        values = []
        for i in range(1, (self.end - self.start) * 2 + 1):
            values.append(self.getNext(i))

        return values


class BooleanGenerator(Generator):
    def __init__(self, generator, probability):
        self.generator = generator
        self.probability = probability

    def getNext(self, i):
        if random.random() >= self.probability:
            return None

        return self.generator.getNext(i)


class AggregateGenerator(Generator):
    def __init__(self, *args):
        if isinstance(args[0], list):
            self.generators = args[0]
        else:
            self.generators = args

    def getNext(self, i):
        res = []
        for gen in self.generators:
            v = gen.getNext(i)
            v = '' if not v else v
            res.append(v)

        return ' '.join(res).strip()


class PredefinedGenerator(Generator):
    def __init__(self, mainGenerator, predVars):
        self.mainGenerator = mainGenerator
        self.predVars = predVars

    def getNext(self, i):
        i = i - 1
        if i < len(self.predVars):
            return self.predVars[i]

        return self.mainGenerator.getNext(i)


class AddressGenerator(Generator):
    def __init__(self, noSt, noMin, noMax, noAp, apHeight, noBlocks, probAp, probBlock):
        stGen = RangeGenerator(
            SequentialTextGenerator('Rua').getRange(noSt)
        )
        noGen = RangeGenerator(
            SequentialTextGenerator('No').getRange(noMin, noMax)
        )
        blocoGen = BooleanGenerator(
            RangeGenerator(
                SequentialTextGenerator(
                    'Bloco').getRange(1, noBlocks + 1)
            ),
            probBlock
        )
        apGen = BooleanGenerator(
            AggregateGenerator(
                RangeGenerator(
                    ApGenerator(noAp, apHeight).getRange()
                ),
                blocoGen
            ),
            probAp
        )

        self.generator = AggregateGenerator(
            stGen,
            noGen,
            apGen
        )

    def getNext(self, i):
        return self.generator.getNext(i)


class Table(Generator):
    def __init__(self, tableDocs, columnTypes, rangeSize):
        tableDocsList = re.findall(r":?\w+", tableDocs)
        name, columns = tableDocsList[0], tableDocsList[1:]
        keys = [False] * len(columns)

        print(f'Creating table {name}')

        for i in range(len(columns)):
            if columns[i][0] == ':':
                columns[i] = columns[i][1:]
                keys[i] = True

        if rangeSize <= 0:
            raise Exception("Number of created values cannot be zero")

        if len(columns) != len(columnTypes):
            raise Exception(
                f"Number of columns and args in table {name} differ"
            )

        self.docs = tableDocs
        self.name = name
        self.columns = columns
        self.keys = keys
        self.columnTypes = columnTypes
        self.rangeSize = rangeSize

    def initData(self, data):
        print(f'Initializing table {self.name}')

        data[self.name] = {
            'table': self,
            'columns': self.columns,
            'values': None
        }

    def createValue(self, i, data):
        return random.randint(1, len(data[self.name]['values']))

    def generate(self, data):
        if data[self.name]['values'] != None:
            return

        print(f'Generating table {self.name}')

        for ct in self.columnTypes:
            if isinstance(ct, str):
                ct = data[ct]['table']
                ct.generate(data)

        print(f'Creating values for table {self.name}')

        values = self.createValues(data)

        print(f'Setting values for table {self.name}')

        data[self.name]['order'] = len(data) + 1
        data[self.name]['values'] = values

    def createValues(self, data):
        values = {}
        i = 1
        while i <= self.rangeSize:
            val = []
            key = []

            for j, ct in enumerate(self.columnTypes):
                if isinstance(ct, str):
                    ct = data[ct]['table']

                v = ct.createValue(i, data)
                val.append(v)
                if self.keys[j]:
                    key.append(v)

            val = tuple(val)
            key = tuple(key) if len(key) else i
            if key not in values:
                values[key] = val
                i += 1

        return list(values.values())


class SqlGenerator:
    def __init__(self, tables):
        self.tables = tables

    def createData(self):
        data = {}

        for t in self.tables:
            t.initData(data)

        for t in self.tables:
            t.generate(data)

        return data

    def getSql(self):
        data = self.createData()
        dataList = list(data.items())
        dataList.sort(key=lambda i: i[1]['order'])

        sql = ''
        for table in self.tables:
            sql += f'-- {table.docs}\n'

        sql += '\n\n'

        for table in dataList:
            sql += SqlGenerator.getTableSql(table) + '\n\n'

        return sql

    def sqlToFile(self, filepath):
        sql = self.getSql()
        with open(filepath, 'w', encoding='utf-8') as fout:
            fout.write(sql)

    @staticmethod
    def getTableSql(table):
        tableName, tableData = table
        columns, values = tableData['columns'], tableData['values']

        sqlColumns = ', '.join((c for c in columns))
        sql = f'INSERT INTO {tableName} ({sqlColumns}) VALUES'
        sql += '\n    '
        sql += ',\n    '.join((str(i) for i in values))
        sql += ';\n'

        return sql
