import os
import shutil
import string


def createPathIfNotExists(path):
	if not os.path.exists(path):
		os.makedirs(path)


def parseComment(line):
	sp = line.split('//')
	comment = ''
	if len(sp) > 1:
		line, comment = sp
	elif line[:2] == '//':
		line = ''
		comment = sp
	return line.rstrip(), comment.strip()


def splitAccessorDefault(line, default):
	line = line.strip()
	accessor = default
	if line[0] == '-':
		accessor = 'private'
		line = line[1:]
	if line[0] == '#':
		accessor = 'protected'
		line = line[1:]
	if line[0] == '+':
		accessor = 'public'
		line = line[1:]
	if line[0] == '~':
		accessor = ''
		line = line[1:]

	return accessor, line


def getCType(cname):
	cname = cname.strip()
	ctype = 'class'
	if (cname[0] == 'I') and (ord('A') <= ord(cname[1]) <= ord('Z')):
		ctype = 'interface'
	if (cname[0:4] == 'ENUM') and (ord('A') <= ord(cname[1]) <= ord('Z')):
		ctype = 'enum'

	return ctype


def parseExtendLine(line):
	line = line.strip()
	classes = map(lambda x: x.strip(), line.split(','))
	classes = list(filter(lambda x: x, classes))

	extend = []
	implement = []
	for c in classes:
		ctype = getCType(c)
		if ctype == 'class':
			extend.append(c)
		elif ctype == 'interface':
			implement.append(c)

	if len(extend) > 1:
		raise Exception('so pode extender uma classe')

	line = ''
	if len(extend) > 0:
		line = f'extends {extend[0]}'
	if len(implement) > 0:
		implementLine = ', '.join(implement)
		line += f' implements {implementLine}'

	return line.strip()


def parseCISignature(line):
	line, comment = parseComment(line)
	line = line.strip()
	hasAbstract, line = parseAbstract(line)
	accessor, line = splitAccessorDefault(line, 'public')

	l = line.split(':')
	cname, extendLine = l if len(l) > 1 else (l[0], '')
	cname = cname.strip()
	ctype = getCType(cname)
	extendLine = parseExtendLine(extendLine)

	if ctype == 'enum':
		cname = cname[4:]

	line = cname
	cname = cname.split('<')[0].strip()
	if extendLine:
		line = f'{line} {extendLine}'

	line = f'{ctype} {line}'
	if hasAbstract:
		line = f'abstract {line}'
	if accessor:
		line = f'{accessor} {line}'
	if comment:
		line = f'{line} // {comment}'

	return ctype, cname, line


def checkIsMethod(line):
	return '(' in line


def parseOverride(line):
	line = line.strip()
	hasOverride = False
	if 'override' in line[0:8]:
		line = line[8:].strip()
		hasOverride = True


	return hasOverride, line


def parseAbstract(line):
	line = line.strip()
	hasAbstract = False
	if 'abstract' in line[0:8]:
		line = line[8:].strip()
		hasAbstract = True


	return hasAbstract, line


def parseFinal(line):
	line = line.strip()
	hasFinal = False
	if 'final' in line[0:5]:
		line = line[5:].strip()
		hasFinal = True


	return hasFinal, line


def parseType(line):
	temp = line.split(')')[-1]
	ltype = temp.split(':')[-1]
	if ltype == temp:
		ltype = ''
	ltype = ltype.strip()
	if ltype != '':
		line = ':'.join(line.split(':')[:-1])

	return ltype, line.strip()


def splitProps(line):
	if not line.strip():
		return []

	numBraces = 0
	props = []
	chars = []
	for char in line:
		if char == '<':
			numBraces += 1
		elif char == '>':
			numBraces -= 1

		if numBraces < 0:
			raise Exception('numero de <> nao bate')

		if char == ',':
			if numBraces == 0:
				props.append(''.join(chars))
				chars = []
			else:
				chars.append(char)
		else:
			chars.append(char)

	if numBraces != 0:
		raise Exception('numero de <> nao bate')

	props.append(''.join(chars))
	return props


def parseMethodProps(line):
	start, line = line.split('(')
	sp = line.split(')')
	line, end = sp if len(sp) > 1 else ('', sp[0])

	props = splitProps(line)
	parsedProps = []
	for prop in props:
		prop = prop.strip()
		ptype, prop = parseType(prop)
		parsedProps.append(f'{ptype} {prop}')

	line = ', '.join(parsedProps)
	return f'{start}({line}){end}'


def parseMethodLine(line, ctype):
	hasAbstract, line = parseAbstract(line)
	hasOverride, line = parseOverride(line)
	hasFinal, line = parseFinal(line)
	accessor, line = splitAccessorDefault(line, 'public')
	ltype, line = parseType(line)
	line = parseMethodProps(line)

	if ltype:
		line = f'{ltype} {line}'
	if hasFinal:
		line = 'final ' + line
	if hasAbstract:
		line = 'abstract ' + line
	if accessor:
		line = f'{accessor} {line}'

	line = f'\t{line}'
	if hasOverride:
		line = f'\t@Override\n{line}'

	if ctype == 'class':
		line += ' { }'
	elif ctype == 'interface':
		line += ';'
	return line


def parsePropLine(line):
	accessor, line = splitAccessorDefault(line, 'private')
	ltype, prop = parseType(line)
	line = f'{ltype} {prop};'
	if accessor:
		line = f'{accessor} {line}'

	return f'\t{line}'


def parseEnumLine(line):
	return line + ','


def parseLine(line, ctype):
	line, comment = parseComment(line)

	if ctype == 'enum':
		line = parseEnumLine(line)
	elif checkIsMethod(line):
		line = parseMethodLine(line, ctype)
	else:
		line = parsePropLine(line)

	if comment:
		line = f'{line} // {comment}'

	return line


def createImportsString(packages):
	usings = []
	for p in packages:
		usings.append(f'import {p}.*;\n')

	return ''.join(usings)


def createClass(packageLine, allPackages, cstr, dst):
	package, packageCcomment = parseComment(packageLine)
	packageLine = f'package {package};'
	if packageCcomment:
		packageLine = f'{packageLine} // {packageCcomment}'
	packageLine += '\n'

	pathes = '/'.join(package.split('.')) + '/'
	folderPath = dst + pathes
	createPathIfNotExists(folderPath)

	clines = list(filter(lambda x: parseComment(x)[0].strip(), cstr.split('\n')))

	lines = []
	lines.append(packageLine)
	lines.append(createImportsString(allPackages))
	ctype, cname, line1 = parseCISignature(clines[0])
	lines.append(line1 + ' {')
	clines = clines[1:]

	for line in clines:
		line = parseLine(line, ctype)
		lines.append(line + '\n')

	if len(clines) > 0:
		lines[-1] = lines[-1][:-1]

	lines.append('}')
	cstr = '\n'.join(lines) + '\n'
	with open(folderPath + cname + '.java', 'w') as f:
		f.write(cstr)


def splitClasses(file):
	lines = file.split('\n')
	lines = list(filter(lambda x: x.strip(), lines))

	classes = []
	currLines = []
	for line in lines:
		if line[0] not in string.whitespace:
			classes.append('\n'.join(currLines))
			currLines = [line]
		else:
			currLines.append(line)

	classes.append('\n'.join(currLines))

	classes = list(filter(lambda x: x.strip(), classes))
	return classes


def createClassesFromFile(file, allPackages, rootpath):
	dst = rootpath + 'src/'
	packageLine = file.split('\n')[0].strip()
	file = '\n'.join(file.split('\n')[1:]).strip()

	classes = splitClasses(file)
	for i in classes:
		createClass(packageLine, allPackages, i, dst)


def createClassesFromFolder(folderPath):
	rootpath = folderPath + 'generated/JavaReverse/'
	if os.path.exists(rootpath) and os.path.isdir(rootpath):
		shutil.rmtree(rootpath)

	files = list(filter(lambda x: '.txt' in x[-4:], os.listdir(folderPath)))

	packages = set()
	packages.add('java.util')
	packages.add('java.awt')
	packages.add('java.math')
	for path in files:
		with open(folderPath + path, 'r') as f:
			package = f.read().split('\n')[0].strip()
			package = parseComment(package)[0]
			packages.add(package)

	packages = list(packages)
	packages.sort()

	for path in files:
		with open(folderPath + path, 'r') as f:
			createClassesFromFile(f.read(), packages, rootpath)


if __name__ == '__main__':
	createClassesFromFolder('./')
