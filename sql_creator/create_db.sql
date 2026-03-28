CREATE TABLE IF NOT EXISTS Curso (
    numcurso serial,
    nome varchar(128),
    totalcreditos integer,

    CONSTRAINT curso_pkey PRIMARY KEY (numcurso)
);

CREATE TABLE IF NOT EXISTS Aluno (
    numaluno serial,
    nome varchar(128),
    endereco varchar(128),
    cidade varchar(64),
    telefone varchar(9),
    numcurso integer,

    CONSTRAINT aluno_pkey PRIMARY KEY (numaluno),
    CONSTRAINT aluno_fkey_curso
        FOREIGN KEY (numcurso)
        REFERENCES Curso (numcurso)
);

CREATE TABLE IF NOT EXISTS Professor (
    numprof serial,
    nome varchar(128),
    areapesquisa varchar(128),

    CONSTRAINT professor_pkey PRIMARY KEY (numprof)
);

CREATE TABLE IF NOT EXISTS Disciplina (
    numdisp serial,
    nome varchar(128),
    quantcreditos integer,

    CONSTRAINT disciplina_pkey PRIMARY KEY (numdisp)
);

CREATE TABLE IF NOT EXISTS Aula (
    semestre varchar(6),
    nota numeric,
    numaluno integer,
    numprof integer,
    numdisp integer,

    CONSTRAINT aula_pkey PRIMARY KEY (semestre, numaluno, numprof, numdisp),
    CONSTRAINT aula_fkey_aluno
        FOREIGN KEY (numaluno)
        REFERENCES Aluno (numaluno),
    CONSTRAINT aula_fkey_professor
        FOREIGN KEY (numprof)
        REFERENCES Professor (numprof),
    CONSTRAINT aula_fkey_disciplina
        FOREIGN KEY (numdisp)
        REFERENCES Disciplina (numdisp)
);

CREATE TABLE IF NOT EXISTS DisciplinaCurso (
    numdisp integer,
    numcurso integer,

    CONSTRAINT disciplina_curso_pkey PRIMARY KEY (numdisp, numcurso),
    CONSTRAINT disciplina_curso_fkey_disciplina
        FOREIGN KEY (numdisp)
        REFERENCES Disciplina (numdisp),
    CONSTRAINT disciplina_curso_fkey_curso
        FOREIGN KEY (numcurso)
        REFERENCES Curso (numcurso)
);
