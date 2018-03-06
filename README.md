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
	
El fichero dbconfig.py contiene el nombre de usuario y la contraseña de mysql, debe modificarse.
Ejecutamos este comando para cargar la base de datos:

		$ python db_setup.py

Para ejecutar usamos:

		$ python crimemap.py
	
Si necesitas que la petición venga por cualquier interfaz añade host='0.0.0.0' en el método clear después dede el parametro port=5300 y antes del parámetro 

¿Cómo funciona? 

Se ha obtenido la distancia entre dos puntos ejecutando la siguiente query: 
select ST_Distance_Sphere(
    point( (select longitude from crimes where id = '1'), (select latitude from crimes where id = '1')),
    point((select longitude from crimes where id = '2'), (select latitude from crimes where id = '2'))
)/1000

La función geo de mysql llamada st_distance_sphere recibe dos objetos posición y devuelve la distancia en metros entre ellos, lo que se ha hecho aquí es seleccionar los puntos según su id y mostrar la diferencia en km entre ellos dividiendo los metros entre 1000 para obtener kilómetros.

Esta query es la que recibe mysql si entramos a la aplicación poniendo solo localhost:5300, pero si accedemos utilizando la url localhost:5300/dist/3/1 por ejemplo mostrará la distancia entre los puntos con id 3 y 1, se ha conseguido haciendo lo siguiente: 

  
	def get_distancia(self,ide,point):
    connection = self.connect()
    try:
      data = {
      'po': point,
      'ide' : ide
      }
      query = "SELECT ST_Distance_Sphere(point((SELECT longitude from crimes where id = %(po)s), (select latitude from crimes where id = %(po)s)),point((select longitude from crimes where id = %(ide)s), (select latitude from crimes where id = %(ide)s)))/1000"
      with connection.cursor() as cursor:
        cursor.execute(query, data)
        dist = cursor.fetchone()
        return dist

    finally:
      connection.close()
    

Este trozo de código lo podeis encontrar en dbhelper.py donde se ejecuta la función get_distancia, se activa al entrar utilizando la url mencionada anteriormente y devuelve la distancia entre los dos puntos que recibe.

los devuelve a crimemap.py donde se renderiza la vista pasando además del resto de datos, la distancia entre los dos puntos que coge de la url: 

 
	@app.route("/dist/<int(min=0,max=9):point>/<int(min=0,max=9):ide>")
	def get_distancia_entre(point,ide,error_message=None):
	  crimes=DB.get_all_crimes()
	  distancia=DB.get_distancia(point,ide)
	  crimes = json.dumps(crimes, encoding='latin1')
	  distancia = json.dumps(distancia)
	  return render_template("home.html",crimes=crimes,
	       categories=categories, error_message=error_message, distance=distancia
	   )

y para ver todas las entradas podemos acceder a la url localhost:5300/all y nos devuelve todo, aunque no muestra el id y no puedo seguir trabajando en ello por ahora ya que me falta tiempo