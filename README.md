# IPC1-PROYECTO2
from flask import Flask, request, jsonify, redirect
from usuarios import administrador, doctores, enfermeras, pacientes
import json

app = Flask (__name__)

@app.route ("/login", methods = ["POST"])
def index ():
   # Creo variables de busqueda, si el resultado coincide, la variable no quedara vacia
    usqueda_admin = [admi for admi in administrador if admi ["usuario"] == request.json ["usuario"] and admi ["contraseña"] == request.json ["contraseña"] ] 
    busqueda_paciente = [paciente for paciente in pacientes if paciente ["usuario"] == request.json ["usuario"] and paciente ["contraseña"] == request.json ["contraseña"]]
    busqueda_doctor = [doctor for doctor in doctores if doctor ["usuario"] == request.json ["usuario"] and doctor ["contraseña"] == request.json ["contraseña"]]
    busqueda_enfermera = [enfermera for enfermera in enfermeras if enfermera ["usuario"] == request.json ["usuario"] and enfermera["contraseña"] == request.json["contraseña"] ]
    
    # se verifica que la variable no este vacia en cada caso
    if (len (busqueda_admin) > 0):
        print ("has iniciado sesion como administrador")
        return redirect ("/login/admin")
    elif (len (busqueda_paciente )> 0):
          print ("Has iniciado sesion como paciente")
          return jsonify (request.json)
    elif (len (busqueda_doctor )> 0):
          print ("Has iniciado sesion como doctor")
          return jsonify (request.json)
    elif (len (busqueda_enfermera )> 0):
          print ("Has iniciado sesion como enfermera")
          return jsonify (request.json)
    else:
          return jsonify ({"mensaje":"credenciales no encontradad"})
 
 #MODULO DE ADMINISTRACION
@app.route ("/login/admin", methods = ["GET"])   
def administrar ():
    return jsonify ({"mensaje":"Hola"})

@app.route ("/login/admin", methods = ["POST"])


#CREAR CUENTA DE CADA COSA
@app.route ("/crear_cuenta", methods = ["POST"])
def crear ():
    if (request.json["crear"]== "doctor"):
        return redirect ("/crear_cuenta/doctor")
    elif(request.json ["crear"] == "enfermera"):
        return redirect ("/crear_cuenta/enfermera")
    elif (request.json ["crear"] == "paciente"):
        return redirect ("/crear_cuenta/paciente")

@app.route ("/crear_cuenta/doctor", methods = ["POST"])
 def crear_doctor ():
     new_doctor = {
     
     }
 
@app.route ("/crear_cuenta/enfermera", methods = ["POST"] )
 def crear_enfermera 
 
@app.route ("/crear_cuenta/paciente", methods = ["POST"])
 def crear_paciente ():


      
    
    

if __name__ == "__main__":
   app.run( "0.0.0.0", port = 4040, debug = True)
