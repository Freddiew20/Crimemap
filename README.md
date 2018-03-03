	# crimeapp
	Este proyecto es una aplicación que registra crimenes, dónde suceden, cuando suceden y el mensaje que escribe el usuario
	
	Puedes crear un entorno virtual con
	        $python3 -m virtualenv env
	
	Para acceder al entorno virtual de python creado ejecutamos
	        $source env/bin/activate

	Este proyecto presenta tres dependencias:
	
	La primera es el framework Flask que la instalaremos ejecutando
	        $pip install flask
	
	La segunda es mysql:
	        $pip install pymysql
	
	La tercera es datetime:
	        $pip install datetime
	
	        $pip install dateparser
	
	
	Secuencia de instalación del proyecto:
	
	En segundo lugar se debe ejecutar el fichero db_setup.py para que cree la base de datos crimeapp.
	
	El fichero dbconfig.py contiene el nombre de usuario y la contraseña, debe modificarse.
	
	Para ejecutar usamos python db_setup.py
	
	Ejecutamos la aplicación con python crimemap.py
	
	Si necesitas que la petición venga por cualquier interfaz añade host='0.0.0.0' en el método clear después dede el parametro port=5300 y antes del parámetro
