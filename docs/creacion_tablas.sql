DROP DATABASE IF EXISTS escuela_deportes;
CREATE DATABASE escuela_deportes;

USE escuela_deportes;

CREATE TABLE login
(
    correo     VARCHAR(320), # Según RFC 3696
    contrasena VARCHAR(50) NOT NULL,
    admin      BOOLEAN     NOT NULL,

    PRIMARY KEY (correo)
);

CREATE TABLE actividad
(
    id               INT AUTO_INCREMENT,
    descripcion      TEXT NOT NULL,
    costo            INT  NOT NULL,
    restriccion_edad INT  NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE equipamiento
(
    id           INT AUTO_INCREMENT,
    id_actividad INT  NOT NULL,
    descripcion  TEXT NOT NULL,
    costo        INT  NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (id_actividad) REFERENCES actividad (id)
);

CREATE TABLE instructor
(
    ci       INT,
    nombre   VARCHAR(40) NOT NULL,
    apellido VARCHAR(40) NOT NULL,
    correo_electronico     VARCHAR(320),


    PRIMARY KEY (ci)
);

CREATE TABLE turnos
(
    id          INT AUTO_INCREMENT,
    hora_inicio TIME NOT NULL,
    hora_fin    TIME NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE alumno
(
    ci                 INT,
    nombre             VARCHAR(50) NOT NULL,
    apellido           VARCHAR(50) NOT NULL,
    fecha_nacimiento   DATE        NOT NULL,
    telefono_contacto  VARCHAR(20),
    correo_electronico VARCHAR(320), # Según RFC 3696

    PRIMARY KEY (ci)
);

CREATE TABLE clase
(
    id            INT AUTO_INCREMENT,
    ci_instructor INT,
    id_actividad  INT     NOT NULL,
    id_turno      INT,
    dictada       BOOLEAN NOT NULL,
    fecha         DATE    NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (ci_instructor) REFERENCES instructor (ci) ON DELETE SET NULL ,
    FOREIGN KEY (id_actividad) REFERENCES actividad (id),
    FOREIGN KEY (id_turno) REFERENCES turnos (id) ON DELETE SET NULL
);

CREATE TABLE alumno_clase
(
    id_clase        INT NOT NULL,
    ci_alumno       INT NOT NULL,
    id_equipamiento INT NOT NULL,

    PRIMARY KEY (id_clase, ci_alumno),
    FOREIGN KEY (id_clase) REFERENCES clase (id),
    FOREIGN KEY (ci_alumno) REFERENCES alumno (ci),
    FOREIGN KEY (id_equipamiento) REFERENCES equipamiento (id)
);