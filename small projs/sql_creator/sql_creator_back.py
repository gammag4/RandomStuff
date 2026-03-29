import random
import re


def getAllProbabilitiesFromRanges(values, i=0):
    res = []
    prevValues = []

    if i < len(values) - 1:
        prevValues = getAllProbabilitiesFromRanges(values, i + 1)

        for v in values[i]:
            for prevV in prevValues:
                res.append((v,) + prevV)

    else:
        res = [(v,) for v in values[i]]

    return res


# class Generator:
# 	def __init__(self, tableDocs, placeholders):
# 		tableDocs = re.findall(r"[\w']+", tableDocs)
# 		(tableName, columns) = (tableDocs[0], tableDocs[1:])

# 		self.tableName = tableName
# 		self.columns = columns
# 		self.placeholders = placeholders

# 	def getValue(self);
# 		res = []
# 		for ph in self.placeholders:
# 			res.append(ph.getNext())

# 		return tuple(res)

# 	def createValues(self, number=10):
# 		res = []
# 		for i in range(number):
# 			res.append(self.getValue())

# 		return res

# 	@staticmethod
# 	def valuesToString(values):
# 		return str(values)[1:-1]

# 	@staticmethod
# 	def getRangeFromValues(values, columnNumber):
# 		range = []
# 		for val in values:
# 			range.append(val[i])

# 	def __init__(self, tableDocs, placeholders, dependencies):
# 		super().__init__(tableDocs, placeholders)
# 		self.dependencies = []
# 		for dep in dependencies:
# 			depName = dep.tableName.lower()
# 			if depName not in self.columns:
# 				continue

# 			depIndex = self.columns.index(depName)


class Generator:
    def __init__(self, rangeSize=4):
        self.rangeSize = rangeSize

    def generate(self, generator):
        res = []
        for i in range(1, rangeSize + 1):
            res.append(self.getNext(i))

        return res

    def getNext(self, i):
        return None


class SequentialGenerator(Generator):
    def __init__(self, rangeSize=4):
        super().__init__(rangeSize)
        self.num = 1

    def getNext(self):
        res = self.num
        self.num += 1
        return res


class SequentialTextGenerator(Generator):
    def __init__(self, text, rangeSize=4):
        super().__init__(rangeSize)
        self.text = text

    def getNext(self, i):
        return f'{self.text} {i}'


class RangeTextGenerator(Generator):
    def __init__(self, textRange, rangeSize=4):
        super().__init__(rangeSize)
        self.textRange = textRange

    def getNext(self, i):
        return random.choice(self.textRange)


class PhoneGenerator(Generator):
    def __init__(self, rangeSize=4):
        super().__init__(rangeSize)

    def getNext(self, i):
        number = ''
        for _ in range(9):
            number += str(random.randrange(0, 10))

        return number


class NumberGenerator(Generator):
    def __init__(self, min, max, step, rangeSize=4):
        super().__init__(rangeSize)
        self.min = min
        self.max = max
        self.step = step

    def __init__(self, min, max, rangeSize=4):
        self.__init__(min, max, 1, rangeSize)

    def __init__(self, max, rangeSize=4):
        self.__init__(0, max, rangeSize)

    def getNext(self, i):
        return random.randrange(self.min, self.max, self.step)


class RangeNumberGenerator(Generator):
    def __init__(self, numberRange, rangeSize=4):
        super().__init__(rangeSize)
        self.numberRange = numberRange

    def getNext(self, i):
        return random.choice(self.numberRange)


class PredefinedGenerator(Generator):
    def __init__(self, mainGenerator, predVars, rangeSize=4):
        super().__init__(rangeSize)
        self.mainGenerator = mainGenerator
        self.predVars = predVars
        self.num = 0

    def getNext(self, i):
        if self.num < len(self.predVars):
            num = self.num
            self.num += 1
            return self.predVars[num]

        return self.mainGenerator.getNext(i - len(self.predVars))


class Table(Generator):
    def __init__(self, tableDocs, columnTypes):
        super().__init__(0)
        tableDocs = re.findall(r"[\w']+", tableDocs)
        (name, columns) = (tableDocs[0], tableDocs[1:])

        if len(columns) != len(columnTypes):
            raise "Number of columns and args differ!"

        self.name = name
        self.columns = columns
        self.columnTypes = columnTypes

    def generate(self, generator={}):
        # the created result is in generator (it returns the range of index values)
        if generator.get(self.name, None) == None:
            ranges = []
            for i in range(len(self.columns)):
                valRange = self.columnTypes[i].generate(generator)
                ranges.append(valRange)

            probs = getAllProbabilitiesFromRanges(ranges)

            generator[self.name] = {
                'columns': self.columns,
                'values': probs
            }

        else:
            probs = generator[self.name]['values']

        return [i for i in range(1, len(probs) + 1)]


rangeTotalCreditos = [164, 172, 144, 152, 120, 186, 200]

curso = Table("Curso(nome, totalcreditos)", [
    PredefinedGenerator(SequentialTextGenerator('Curso'), [
        "Engenharia da Computação",
        "Engenharia de Software",
        "Ciência da Computação"
    ], 4),
])
