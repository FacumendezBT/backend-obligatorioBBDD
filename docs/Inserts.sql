USE escuela_deportes;



INSERT INTO escuela_deportes.actividad (descripcion, costo, restriccion_edad) VALUES
                                                                                  ('snowboard', 500, 12),
                                                                                  ('ski', 600, 10),
                                                                                  ('moto de nieve', 700, 15);

INSERT INTO escuela_deportes.turnos (hora_inicio, hora_fin) VALUES
                                                                ('09:00:00', '11:00:00'),
                                                                ('12:00:00', '14:00:00'),
                                                                ('16:00:00', '18:00:00');
INSERT INTO escuela_deportes.instructor (ci, nombre, apellido) VALUES
                                                                   (12345678, 'Juan', 'Pérez'),
                                                                   (87654321, 'Lucía', 'González'),
                                                                   (11223344, 'Carlos', 'Rodríguez');
INSERT INTO escuela_deportes.alumno (ci, nombre, apellido, fecha_nacimiento, telefono_contacto, correo_electronico) VALUES
                                                                                                                        (22334455, 'María', 'López', '2005-06-15', '099123456', 'maria.lopez@example.com'),
                                                                                                                        (33445566, 'Pablo', 'Sánchez', '2008-09-22', '099987654', 'pablo.sanchez@example.com'),
                                                                                                                        (44556677, 'Ana', 'Martínez', '2010-01-10', '099654321', 'ana.martinez@example.com');
INSERT INTO escuela_deportes.clase (ci_instructor, id_actividad, id_turno, dictada, fecha) VALUES
                                                                                               (12345678, 1, 1, TRUE, '2024-10-01'),
                                                                                               (87654321, 2, 2, TRUE, '2024-10-02'),
                                                                                               (11223344, 3, 3, FALSE, '2024-10-03');


INSERT INTO escuela_deportes.equipamiento (id_actividad, descripcion, costo) VALUES
                                                                                 (1, 'Tablas de snowboard', 100),
                                                                                 (2, 'Esquís y bastones', 150),
                                                                                 (3, 'Casco de moto de nieve', 200);
INSERT INTO escuela_deportes.alumno_clase (id_clase, ci_alumno, id_equipamiento) VALUES
                                                                                     (1, 22334455, 1),
                                                                                     (2, 33445566, 2),
                                                                                     (3, 44556677, 3);


