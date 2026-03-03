DROP DATABASE constantec_testing;
INSERT INTO constancia_tipos (tipo, descripcion) VALUES
('Constancia de inscritos', 'Documento que certifica que un estudiante está actualmente inscrito en una institución educativa, indicando generalmente el semestre o ciclo escolar en curso.'),
('Constancia de promedio general', 'Documento que muestra el promedio general de todos los semestre cursados por el estudiante, sirviendo como prueba de que el estudiante aún sigue formando parte de la institución.'),
('Constancia de promedio semestre anterior', 'Documento que detalla las materias cursadas y calificaciones obtenidas en el semestre inmediatamente anterior al actual.'),
('Constancia de promedio dos últimos semestres', 'Documento que detalla las materias cursadas y calificaciones obtenidas en los dos semestres previos al actual.'),
('Constancia de egresado', 'Documento que el estudiante ha concluido en totalidad de sus estudios superiores, aunque aún no haya recibido el título oficial.'),
('Constancia de bachillerato', 'Documento que certifica que el estudiante ha concluido la totalidad de sus estudios medio superior, aunque aún no haya recibido el certificado oficial.'),
('Constancia de maestría', 'Documento que indica que el egresado a iniciado el proceso de maestría y que cuenta con su título profesional ante la autoridad educativa correspondiente.'),
('Constancia de título en trámite', 'Documento que acredita que el estudiante ha finalizado su carrera y queda en espera de su título.'),
('Constancia con número de seguro social', 'Documento que incluye el número de seguro social.');

INSERT INTO solicitud_estatus (tipo, descripcion) VALUES 
('pendiente', 'La solicitud esta pendiente' ),
('revision', 'La solicitud esta en revision' ),
('completo', 'La constancia esta lista' );

INSERT INTO estado_comprobante (tipo, descripcion) VALUES
('sin comprobante', 'No has enviado el comprobante para su revisión.' ),
('pendiente', 'Tu comprobante está en revisión. Espera la validación del personal administrativo.' ),
('rechazado', 'Debes explicar el motivo.' ),
('aprovado', 'Tu comprobante fue aprobado. Ya puedes continuar con el trámite.' );

INSERT INTO Trabajadores (nombre, apellidos, fecha_nacimiento, edad, cargo, telefono, correo_institucional, fecha_inicio) VALUES 
('Jorge', 'Méndez Suárez', '1995-08-12', 30, 'Servicios escolares', '477 890 3463', 'jorge.mendez@leon.tecnm.mx', '2000-06-12'),
('Jessica', 'Rosas Flores', '1989-03-25', 36, 'Servicios escolares', '477 349 1211', 'jessica.rosas@leon.tecnm.mx', '1990-07-20'),
('Camilo', 'Salazar Godínez', '1998-07-05', 27, 'Servicios escolares', '477 571 9712', 'camilo.salazar@leon.tecnm.mx', '2001-05-11');

INSERT INTO [dbo].[estudiantes] ([apellidos], [password], [correo_institucional], [edad], [semestre], [carrera], [fecha_nacimiento], [fecha_registro], [municipio], [no_control], [nombre], [primer_ingreso]) values 
('Rocha', '$2b$12$71/Hi78TNE/eFLx.4j3UB.N5szktjHT0JJ1ArZL4ooDK79wPXa0dK', '123@leon.tecnm.mx', 21, 6, 'Sistemas', '2004-04-21', '2025-06-01', 'Leon', '123', 'Jeshua', 0);

INSERT INTO [dbo].[Usuarios_administradores] ([username], [password], [is_active], [is_superuser]) values 
('admin', '$2b$12$71/Hi78TNE/eFLx.4j3UB.N5szktjHT0JJ1ArZL4ooDK79wPXa0dK', 1, 1);

--- Consultas
DELETE FROM estudiantes WHERE id = 24;

SELECT * FROM usuarios_administradores;
SELECT * FROM estudiantes;
SELECT * FROM solicitudes;
SELECT * FROM solicitud_estatus;
SELECT * FROM constancia_tipos;
SELECT * FROM constancia_opciones;
SELECT * FROM estado_comprobante;
SELECT * FROM encuesta_satisfaccion;
SELECT * FROM constancias;
SELECT * FROM trabajadores;
SELECT * FROM comprobantes_pago;
SELECT * FROM estado_comprobante;