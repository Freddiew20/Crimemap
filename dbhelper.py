import pymysql
import dbconfig
import datetime

class DBHelper:
  def connect(self, database="crimemap"):
    return pymysql.connect(host='localhost',
                           user=dbconfig.db_user,
                           passwd=dbconfig.db_password,
                           db=database)
  
  def add_crime(self,category,date,latitude,longitude,description):
     connection=self.connect()
     try:
       query = "INSERT INTO crimes(category,date,latitude,longitude,description) \
                VALUES(%s, %s, %s, %s, %s)"
       with connection.cursor() as cursor:
         cursor.execute(query,(category,date,latitude,longitude,description))
         connection.commit()
     except Exception as e:
       print(e)
     finally:
       connection.close()
       ''' llll '''

  def get_all_crimes(self):
    connection = self.connect()
    try:
      query = "SELECT latitude,longitude,date,category,description FROM crimes;"
      with connection.cursor() as cursor:
        cursor.execute(query)
      named_crimes=[]
      for crime in cursor:
        named_crime = {
          'latitude':crime[0],
          'longitude':crime[1],
          'date':datetime.datetime.strftime(crime[2],'%Y-%m-%d'),
          'category':crime[3],
          'description':crime[4],
        }
        named_crimes.append(named_crime)
      return named_crimes
    finally:
      connection.close()


  def get_all_crimenes(self):
    connection = self.connect()
    try:
      query = "SELECT id, latitude,longitude,date,category,description FROM crimes;"
      with connection.cursor() as cursor:
        cursor.execute(query)
      named_crimes=[]
      for crime in cursor:
        named_crime = {
          'id':crime[0],
          'latitude':crime[1],
          'longitude':crime[2],
          'date':datetime.datetime.strftime(crime[3],'%Y-%m-%d'),
          'category':crime[4],
          'description':crime[5],
        }
        named_crimes.append(named_crime)
      return named_crimes
    finally:
      connection.close()

  def get_distance(self):
    connection = self.connect()
    try:
      data = {
      'po':1,
      'ide' : 2
      }
      query = "SELECT ST_Distance_Sphere(point((SELECT longitude from crimes where id = %(po)s), (select latitude from crimes where id = %(po)s)),point((select longitude from crimes where id = %(ide)s), (select latitude from crimes where id = %(ide)s)))/1000"
      with connection.cursor() as cursor:
        cursor.execute(query, data)
        dist = cursor.fetchone()
        return dist

    finally:
      connection.close()
  

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
    


  def get_all_inputs(self):
    connection = self.connect()
    try:
      query = "SELECT description FROM crimes;"
      with connection.cursor() as cursor:
        cursor.execute(query)
      return cursor.fetchall()
    finally:
      connection.close()

  def add_input(self, data):
    connection = self.connect()
    try:
      # The following introduces a deliberate security flaw.
      #See section on SQL injection below
      query = "INSERT INTO crimes (description) VALUES (%s);".format(data)
      with connection.cursor() as cursor:
        cursor.execute(query,data)
        connection.commit()
    finally:
        connection.close()

  def clear_all(self):
    connection = self.connect()
    try:
      query = "DELETE FROM crimes;"
      with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
    finally:
        connection.close()

