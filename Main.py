from flask import Flask, request, jsonify, redirect, render_template
from usuarios import administrador, doctores, enfermeras, pacientes, medicamentos
import json

app = Flask (__name__)

@app.route ("/", methods = ["GET" ,"POST"])
def index ():
    
    if request.method == "POST":
        # creo variables de busqueda, si el resultado coincide, la variable no quedara vacia
        busqueda_admin = [admi for admi in administrador if admi ["usuario"] == request.form ["usuario"] and admi ["contraseña"] == request.form ["contraseña"] ] 
        busqueda_paciente = [paciente for paciente in pacientes if paciente ["usuario"] == request.form ["usuario"] and paciente ["contraseña"] == request.form ["contraseña"]]
        busqueda_doctor = [doctor for doctor in doctores if doctor ["usuario"] == request.form ["usuario"] and doctor ["contraseña"] == request.form ["contraseña"]]
        busqueda_enfermera = [enfermera for enfermera in enfermeras if enfermera ["usuario"] == request.form ["usuario"] and enfermera["contraseña"] == request.form["contraseña"] ]
        
        
        if (len (busqueda_admin) > 0):
          print ("has iniciado sesion como administrador")
          return redirect ("/login/admin")

        elif (len (busqueda_paciente )> 0):
          nombrepaciente0 = "/login_paciente/" + busqueda_paciente [0]["nombre"]
          return redirect(nombrepaciente0)

        elif (len (busqueda_doctor )> 0):
          print ("Has iniciado sesion como doctor")
      
        elif (len (busqueda_enfermera )> 0):
          print ("Has iniciado sesion como enfermera")
    
        else:
          return jsonify ({"mensaje":"credenciales no encontradad"})
          
    return render_template ("index.html")

 #--------------------------MODULOS----------------------------------------

  #MODULO DE ADMINISTRACION
@app.route ("/login/admin", methods = ["GET" , "POST" ])   
def administrar ():
      
    return render_template ("tabla_admin.html" , titulo = "Panel administrador" , lista_enfermeras = enfermeras, lista_doctores = doctores, lista_pacientes = pacientes, lista_medicamentos = medicamentos)
 
 
 #MODULO DE PACIENTES
@app.route ("/login_paciente/<string:nombrepaciente>", methods = ["GET" , "POST" ])   
def modulo_paciente (nombrepaciente):
    return render_template ("Panel_paciente.html" , lista_medicamentos = medicamentos )

  
#-----------------------------ELIMINAR----------------------------------

#ELIMINAR PACIENTES
@app.route ("/eliminar/paciente/<string:paciente_nombre>", methods = ["GET", "POST", "DELETE"])
def eliminar_paciente (paciente_nombre):
   busqueda_paciente = [paciente for paciente in pacientes if paciente ["nombre"] == paciente_nombre]
   if (len (busqueda_paciente ) > 0):
     pacientes.remove (busqueda_paciente[0])
   return redirect ("/login/admin")

#ELIMINAR ENFERMEROS
@app.route ("/eliminar/enfermero/<string:enfermero_nombre>", methods = ["GET", "POST", "DELETE"])
def eliminar_enfermero (enfermero_nombre):
   busqueda_enfermera = [enfermera for enfermera in enfermeras if enfermera ["nombre"] == enfermero_nombre]
   if (len (busqueda_enfermera ) > 0):
     enfermeras.remove (busqueda_enfermera[0])
   return redirect ("/login/admin")

#ELIMINAR DOCTORES
@app.route ("/eliminar/doctor/<string:doctor_nombre>", methods = ["GET", "POST", "DELETE"])
def eliminar_doctor (doctor_nombre):
   busqueda_doctor = [doctor for doctor in doctores if doctor ["nombre"] == doctor_nombre]
   if (len (busqueda_doctor ) > 0):
     doctores.remove (busqueda_doctor[0])
   return redirect ("/login/admin")

#ELIMINAR MEDICAMENTOS
@app.route ("/eliminar/medicamento/<string:medicamento_nombre>", methods = ["GET", "POST", "DELETE"])
def eliminar_medicamento (medicamento_nombre):
   busqueda_medicamento = [medicamento for medicamento in medicamentos if medicamento ["nombre"] == medicamento_nombre]
   if (len (busqueda_medicamento ) > 0):
     medicamentos.remove (busqueda_medicamento[0])
   return redirect ("/login/admin")

#------------------------------MODIFICAR--------------------------------------#

#MODIFICAR PACIENTES 
@app.route("/editar_paciente/<string:paciente_nombre>" , methods = ["GET" ,"POST", "PUT"])
def modificar_paciente (paciente_nombre):
    busqueda_paciente = [paciente for paciente in pacientes if paciente ["nombre"] == paciente_nombre]
    print ("Modificar paciente")
    if request.method == "POST":

      busqueda_paciente[0]["nombre"] = request.form ["nombre"]
      busqueda_paciente[0]["apellido"] = request.form ["apellido"]
      busqueda_paciente[0]["fecha de nacimiento"] = request.form ["fecha de nacimiento"]
      busqueda_paciente[0]["sexo"] = request.form ["sexo"]
      busqueda_paciente[0]["usuario"] = request.form ["usuario"]
      busqueda_paciente[0]["contraseña"] = request.form ["contraseña"]
      busqueda_paciente[0]["telefono"] = request.form ["telefono"]

      return redirect ("/login/admin")

    return render_template ("Editar.html" , paciente_nombre = busqueda_paciente[0]["nombre"], paciente_apellido = busqueda_paciente [0]["apellido"], paciente_usuario = busqueda_paciente [0]["usuario"] , paciente_contraseña = busqueda_paciente [0]["contraseña"], paciente_numero = busqueda_paciente [0]["telefono"])


#MODIFICAR DOCTORES 
@app.route("/editar_doctor/<string:doctor_nombre>" , methods = ["GET" ,"POST", "PUT"])
def modificar_doctor (doctor_nombre):
    busqueda_doctor= [doctor for doctor in doctores if doctor ["nombre"] == doctor_nombre]
    print ("Modificar doctor")
    if request.method == "POST":

      busqueda_doctor[0]["nombre"] = request.form ["nombre"]
      busqueda_doctor[0]["apellido"] = request.form ["apellido"]
      busqueda_doctor[0]["fecha de nacimiento"] = request.form ["fecha de nacimiento"]
      busqueda_doctor[0]["sexo"] = request.form ["sexo"]
      busqueda_doctor[0]["especialidad"] = request.form ["especialidad"]
      busqueda_doctor[0]["usuario"] = request.form ["usuario"]
      busqueda_doctor[0]["contraseña"] = request.form ["contraseña"]
      busqueda_doctor[0]["telefono"] = request.form ["telefono"]
      return redirect ("/login/admin")

    return render_template ("Editar_doctor.html" , doctor_nombre = busqueda_doctor[0]["nombre"], doctor_apellido = busqueda_doctor [0]["apellido"], doctor_especialidad = busqueda_doctor [0]["especialidad"], doctor_usuario = busqueda_doctor [0]["usuario"] , doctor_contraseña = busqueda_doctor [0]["contraseña"], doctor_numero = busqueda_doctor [0]["telefono"])


#MODIFICAR ENFERMEROS 
@app.route("/editar_enfermera/<string:enfermera_nombre>" , methods = ["GET" ,"POST", "PUT"])
def modificar_enfermera (enfermera_nombre):
    busqueda_enfermera = [enfermera for enfermera in enfermeras if enfermera ["nombre"] == enfermera_nombre]
    print ("Modificar paciente")
    if request.method == "POST":

      busqueda_enfermera[0]["nombre"] = request.form ["nombre"]
      busqueda_enfermera[0]["apellido"] = request.form ["apellido"]
      busqueda_enfermera[0]["fecha de nacimiento"] = request.form ["fecha de nacimiento"]
      busqueda_enfermera[0]["sexo"] = request.form ["sexo"]
      busqueda_enfermera[0]["usuario"] = request.form ["usuario"]
      busqueda_enfermera[0]["contraseña"] = request.form ["contraseña"]
      busqueda_enfermera[0]["telefono"] = request.form ["telefono"]
      return redirect ("/login/admin")

    return render_template ("Editar.html" , paciente_nombre = busqueda_enfermera[0]["nombre"], paciente_apellido = busqueda_enfermera [0]["apellido"], paciente_usuario = busqueda_enfermera [0]["usuario"] , paciente_contraseña = busqueda_enfermera [0]["contraseña"], paciente_numero = busqueda_enfermera [0]["telefono"])


#MODIFICAR MEDICAMENTOS 
@app.route("/editar_medicamento/<string:medicamento_nombre>" , methods = ["GET" ,"POST", "PUT"])
def modificar_medicamento (medicamento_nombre):
    busqueda_medicamento = [medicamento for medicamento in medicamentos if medicamento ["nombre"] == medicamento_nombre]
    print ("Modificar medicamento")
    if request.method == "POST":

      busqueda_medicamento[0]["nombre"] = request.form ["nombre"]
      busqueda_medicamento[0]["precio"] = request.form ["precio"]
      busqueda_medicamento[0]["descripcion"] = request.form ["descripcion"]
      busqueda_medicamento[0]["cantidad"] = request.form ["cantidad"]
      return redirect ("/login/admin")

    return render_template ("Editar_medicamento.html" , medicamento_nombre = busqueda_medicamento[0]["nombre"], medicamento_precio = busqueda_medicamento [0]["precio"], medicamento_descripcion = busqueda_medicamento [0]["descripcion"] ,medicamento_cantidad = busqueda_medicamento [0]["cantidad"] )


#------------------------------------CREAR CUENTA----------------------------------

@app.route ("/crear_cuenta" , methods = ["GET", "POST"])
def crear_cuenta ():
  if request.method == "POST":  
     new_paciente = {
     "nombre":request.form ["nombre"],
     "apellido":request.form ["apellido"],
     "fecha de nacimiento":request.form ["fecha de nacimiento"],
     "sexo":request.form ["sexo"],
     "usuario":request.form ["usuario"],
     "contraseña":request.form ["contraseña"],
     "telefono":request.form ["telefono"]
     }
     pacientes.append (new_paciente) 
     return redirect ("/") 
  return render_template ("Nuevo_paciente.html" )
  

  
if __name__ == "__main__":
   app.run( "0.0.0.0", port = 4040, debug = True)

## python Main.py