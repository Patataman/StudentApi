## StudentApi

	:shipit: *! ATENCION !* :shipit:

	ESTA API SE AUTODESTRUIRÁ EN 5- es broma, xdddd

	Para poder usar esta API deberás ser miembro de 
	la Universidad Carlos III de Madrid y saber tu 
	NIA y contraseña.

	Con ella se podrá principalmente:
		- Buscar usuarios dados su nia o nombre.
		- Obtener un token de verificación si el NIA
		  y contraseña son correctos Y ADEMÁS perteneces
		  a la Delegación de Estudiantes.
		- Verificar el Token generado
		- Poder verificar si una persona (NIA + contraseña)
		  pertenece a la Delegación de Estudiantes.
		- Conocer si dado un NIA esa persona es: 
			* Delegado de Curso
			* Delegado de Titulación
			* Delegado de Centro

### /

	Ruta base, permite verificar si la API está 
	levantada mediante el True que devuelve

### /student/<int:nia>

	Devuelve la información relacionada con el alumno
	del nia que se introduce.
	Concretamente devuelve:
		- Nombre
		- Correo
		- NIA

### /student/<string:name>

	Devuelve la información de todos los miembros
	de la universidad con el nombre introducido, 
	se dan dos situaciones:

	1- El número de resultados es muy grande (por ejemplo, 50)
		* Devuelve un codigo 500 y False

	2- El número de resultados es lo suficientemente pequeño:
		* Devuelve el array parseado en JSON con la información
		  de todos los alumnos encontrados.

	Ej: String = "Adrián" devolverá un 500
		String = "Adrián Alonso" puede devolver 
				 la información de 10 resultados
				 y un código 200.

### /auth 

	> Method = POST

	Permite generar el token correspondiente para poder
	utilizar la aplicación.

	Para ello deberá pasarse el NIA y la contraseña correspondiente.
	Con el nia, nombre y contraseña genera un token que tiene una duración válida de 1h.

	El token se devuelve en el apartado "Token" en la cabecera de la petición HTTP.

	> Method = GET

	Permite verificar si un token es válido.

	Para ello se debe pasar en la cabecera HTTP un apartado
	llamado 'Authorization', este campo debe tener el valor:

	```
	Bearer <token>
	```

	Si el token es correcto, devuelve un código 200 y True, si 
	es incorrecto se devuelve 401 y False.

### /login

	Permite verificar si la persona correspondiente pertenece
	a la tabla de Personas (Es decir, forma parte de alguna forma
	de la Delegacion)

	El método /auth (POST) lo utiliza para verificar 
	la identidad del usuario.

	Se puede utilizar sin necesidad del Token.

	Si todo funciona correctamente devuelve un código 200
	y True.

	Si la persona es miembro de la universidad pero no está
	en la tabla personas se devuelve un código 401 y False.
	Si ocurre algún error en el login se devuelve un 400 y False.

### /permisos/<int:nia>/<int:app_id>

	Permite obtener los permisos de un usuario (NIA)
	para cierta aplicación (app_id).

	Si la persona tiene permisos para esa aplicación se
	devuelve un código 200 y los permisos correspondientes.
	Si la persona no tiene permisos se devuelve un código 200,
	pero los permisos serán 0.

	Si ocurre algún error se devuelve un código 400 y False.

### /delegado/<int:nia>

	Permite conocer si cierta persona (NIA) es delegado/a.
	Para ello se comprueba con la tabla delegadoscurso de la BBDD.

	Si es delegado se devuelve un 200 y True.
	Si no es delegado se devuelve un código 200 y False.
	Si ocurre algún error se devuelve un código 400 y False.

### /delegadoTit/<int:nia>

	Permite conocer si cierta persona (NIA) es delegado/a de titulación.
	Para ello se comprueba con la tabla delegadostitulacion de la BBDD.

	Si es delegado se devuelve un 200 y True.
	Si no es delegado se devuelve un código 200 y False.
	Si ocurre algún error se devuelve un código 400 y False.

### /delegadoCen/<int:nia>

	Permite conocer si cierta persona (NIA) es delegado/a de titulación.
	Para ello se comprueba con la tabla delegadoscentro de la BBDD.

	Si es delegado se devuelve un 200 y su cargo correspondiente.
	Si no es delegado se devuelve un código 200 y False.
	Si ocurre algún error se devuelve un código 400 y False.