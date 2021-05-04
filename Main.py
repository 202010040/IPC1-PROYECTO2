from flask import Flask, request, jsonify, redirect, render_template, make_response
from operator import itemgetter
import json, csv, pdfkit, operator


doctores = []

administrador = [{"nombre":"Javier", "apellido":"Golon", "usuario":"admin", "contraseña": "1234"}]

enfermeras = []

doctores = []


pacientes = []

medicamentos = []
citas = []
pedidos = [ ]
enfermedades = []
facturas = []




app = Flask (__name__)

@app.route ("/", methods = ["GET" ,"POST"])
def index ():
    return render_template ("inicio.html")

@app.route ("/cerrar_sesion_paciente", methods = ["POST"])
def cerrar_sesion_paciente():
  if request.method == "POST":
   pedidos.clear()
   return redirect ("/")


@app.route ("/inicio", methods = ["GET" , "POST"])
def inicio ():   
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
          paciente1 = busqueda_paciente [0]["nombre"]
          nombrepaciente0 = "/login_paciente/" + paciente1
          return redirect(nombrepaciente0 )

        elif (len (busqueda_doctor )> 0):
          doctor1 = busqueda_doctor [0]["nombre"]
          linkdoctor = "/login_doctor/" + doctor1
          return redirect(linkdoctor )
      
        elif (len (busqueda_enfermera )> 0):
          enefermera1 = busqueda_enfermera [0]["nombre"]
          nombreenfermera = "/login_enfermera/" + enefermera1
          return redirect(nombreenfermera)
         
    
        else:
          return render_template ("error de credenciales.html")
          
    return render_template ("index.html")

 #--------------------------MODULOS----------------------------------------

  #MODULO DE ADMINISTRACION
@app.route ("/login/admin", methods = ["GET" , "POST" ] )   
def administrar ():
      
    return render_template ("tabla_admin.html" , titulo = "Panel administrador" , lista_enfermeras = enfermeras, lista_doctores = doctores, lista_pacientes = pacientes, lista_medicamentos = medicamentos)
 
 
 #MODULO DE PACIENTES
@app.route ("/login_paciente/<string:nombrepaciente>", methods = ["GET" , "POST" ])   
def modulo_paciente (nombrepaciente):
    total = []
    for pedido in pedidos:
        total0 = pedido["cantidad"]*pedido["precio_unitario"]
        total.append (total0)
    total1 = (sum(total))

    return render_template ("Panel_paciente.html" , lista_medicamentos = medicamentos , lista_pedidos = pedidos, paciente_nombre = nombrepaciente, total_pedido = total1, lista_citas = citas)

 #MODULO DE ENFERMERA
@app.route ("/login_enfermera/<string:nombreenfermera>") 
def moduloenfermera (nombreenfermera):

     return render_template ("Panel_enfermera.html" , lista_citas = citas, enfermera_nombre = nombreenfermera, lista_doctores = doctores , lista_pacientes = pacientes)

#MODULO DE DOCTORES
@app.route ("/login_doctor/<string:nombredoctor>")
def modulodoctor (nombredoctor):
    return render_template ("Panel_doctor.html", lista_citas = citas, doctor_nombre = nombredoctor, lista_pacientes = pacientes)


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

#MODIFICAR ADMIN
@app.route ("/editar_admin")
def editar_admin ():
  if request.method == "POST":
     administrador [0] ["nombre"] = request.form ["nombre"]
     administrador [0] ["apellido"] = request.form ["apellido"]
     administrador [0] ["usuario"] = request.form ["usuario"]
     administrador [0] ["contraseña"] = request.form ["contraseña"]
     return redirect ("/login/admin")

  return render_template ("Editar admin.html" , admin_nombre = administrador [0] ["nombre"] , admin_apellido = administrador [0] ["apellido"], admin_usuario = administrador [0] ["usuario"] , admin_contraseña = administrador [0] ["contraseña"] )




#MODIFICAR PACIENTES DESDE PACIENTES
@app.route("/editar_paciente_desde_paciente/<string:paciente_nombre>" , methods = ["GET" ,"POST", "PUT"])
def modificar_paciente_desde_paciente (paciente_nombre):
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

      return redirect ("/login_paciente/" +  busqueda_paciente[0]["nombre"] )

    return render_template ("Editar.html" , paciente_nombre = busqueda_paciente[0]["nombre"], paciente_apellido = busqueda_paciente [0]["apellido"], paciente_usuario = busqueda_paciente [0]["usuario"] , paciente_contraseña = busqueda_paciente [0]["contraseña"], paciente_numero = busqueda_paciente [0]["telefono"])

#MODIFICAR ENFERMERODESDE ENFERMERO
@app.route("/editar_enfermera_desde_enfermera/<string:enfermera_nombre>" , methods = ["GET" ,"POST", "PUT"])
def modificar_enfermera_desde_enfermera (enfermera_nombre):
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
      return redirect ("/login_enfermera/"+ busqueda_enfermera[0]["nombre"] )

    return render_template ("Editar.html" , paciente_nombre = busqueda_enfermera[0]["nombre"], paciente_apellido = busqueda_enfermera [0]["apellido"], paciente_usuario = busqueda_enfermera [0]["usuario"] , paciente_contraseña = busqueda_enfermera [0]["contraseña"], paciente_numero = busqueda_enfermera [0]["telefono"])

#MODIFICAR DOCTOR DESDE DOCTOR
@app.route("/editar_doctor_desde_doctor/<string:doctor_nombre>" , methods = ["GET" ,"POST", "PUT"])
def modificar_doctor_desde_doctor (doctor_nombre):
    busqueda_doctor= [doctor for doctor in doctores if doctor ["nombre"] == doctor_nombre]
    if request.method == "POST":

      busqueda_doctor[0]["nombre"] = request.form ["nombre"]
      busqueda_doctor[0]["apellido"] = request.form ["apellido"]
      busqueda_doctor[0]["fecha de nacimiento"] = request.form ["fecha de nacimiento"]
      busqueda_doctor[0]["sexo"] = request.form ["sexo"]
      busqueda_doctor[0]["especialidad"] = request.form ["especialidad"]
      busqueda_doctor[0]["usuario"] = request.form ["usuario"]
      busqueda_doctor[0]["contraseña"] = request.form ["contraseña"]
      busqueda_doctor[0]["telefono"] = request.form ["telefono"]
      return redirect ("/login_doctor/" + busqueda_doctor[0]["nombre"])

    return render_template ("Editar_doctor.html" , doctor_nombre = busqueda_doctor[0]["nombre"], doctor_apellido = busqueda_doctor [0]["apellido"], doctor_especialidad = busqueda_doctor [0]["especialidad"], doctor_usuario = busqueda_doctor [0]["usuario"] , doctor_contraseña = busqueda_doctor [0]["contraseña"], doctor_numero = busqueda_doctor [0]["telefono"])



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
  

#-------------------------AÑADIR AL CARRITO--------------------------------------------
@app.route("/añadir/orden/<string:orden_nombre>" , methods = ["GET" ,"POST", "PUT"])
def añadir_al_carrito (orden_nombre):
   if request.method == "POST": 
      redireccion = "/login_paciente/" + request.form ["paciente_nombre"]
      busqueda_medicamento = [medicamento for medicamento in medicamentos if medicamento ["nombre"] == orden_nombre]
      new_pedido = {
      "nombre": orden_nombre,
      "cantidad": int (request.form ["cantidad_ordenada"] ),
      "precio_unitario": busqueda_medicamento [0]["precio"],
      }
      busqueda_medicamento[0]["cantidad"] = busqueda_medicamento[0]["cantidad"] - int (request.form ["cantidad_ordenada"] )
      busqueda_medicamento[0]["vendidos"] = busqueda_medicamento[0]["vendidos"] + int (request.form ["cantidad_ordenada"] )

      pedidos.append(new_pedido)

      return redirect (redireccion)

#----------------------CARGA MASIVA -------------------------
@app.route ("/pantalla carga")
def pantalla_carga ():
  return render_template ("Carga masiva.html")

@app.route ("/carga_pacientes", methods  = ["GET", "POST"])
def carga_paciente():
  if request.method == "POST":
     ruta = request.form ["ruta"]

     archivo = csv.DictReader (open(ruta))
     for columnas in archivo:
             new_paciente = {
             "nombre": columnas ["nombre"],
             "apellido": columnas ["apellido"],
             "fecha de nacimiento": columnas ["fecha"],
             "sexo":columnas ["sexo"],
             "usuario": columnas ["usuario"],
             "contraseña":columnas ["password"],
             "telefono": columnas ["telefono"]
             }
             pacientes.append(new_paciente)

     return redirect ("/login/admin") 

  return render_template ("Carga masiva.html")
  
@app.route ("/carga_doctores", methods  = ["GET", "POST"])
def carga_doctores():
  if request.method == "POST":
     ruta = request.form ["ruta"]

     archivo = csv.DictReader (open(ruta))
     for columnas in archivo:
             new_doctor = {
             "nombre": columnas ["nombre"],
             "apellido": columnas ["apellido"],
             "fecha de nacimiento": columnas ["fecha"],
             "sexo":columnas ["sexo"],
             "especialidad":columnas ["especialidad"],
             "usuario": columnas ["usuario"],
             "contraseña":columnas ["password"],
             "telefono": columnas ["telefono"],
             "citas_atendidas": 0
             }
             doctores.append(new_doctor)

     return redirect ("/login/admin") 

  return render_template ("Carga masiva.html")

@app.route ("/carga_enfermera", methods  = ["GET", "POST"])
def carga_anfermera():
  if request.method == "POST":
     ruta = request.form ["ruta"]

     archivo = csv.DictReader (open(ruta))
     for columnas in archivo:
             new_paciente = {
             "nombre": columnas ["nombre"],
             "apellido": columnas ["apellido"],
             "fecha de nacimiento": columnas ["fecha"],
             "sexo":columnas ["sexo"],
             "usuario": columnas ["usuario"],
             "contraseña":columnas ["password"],
             "telefono": columnas ["telefono"]
             }
             enfermeras.append(new_paciente)

     return redirect ("/login/admin") 

  return render_template ("Carga masiva.html")

@app.route ("/carga_medicamentos", methods  = ["GET", "POST"])
def carga_medicamentos():
  if request.method == "POST":
     ruta = request.form ["ruta"]

     archivo = csv.DictReader (open(ruta))
     for columnas in archivo:
             new_medicamento = {
             "id":columnas ["nombre"].replace(" ", "_") ,
             "nombre": columnas ["nombre"],
             "precio": float ( columnas ["precio"]),
             "descripcion": columnas ["descripcion"],
             "cantidad": int (columnas ["cantidad"]),
             "vendidos": 0
             }
             medicamentos.append(new_medicamento)

     return redirect ("/login/admin") 

  return render_template ("Carga masiva.html")

#----------------------------------------------CITAS---------------------------------------------------------------

@app.route ("/solicitar_cita/<string:nombre>", methods = ["GET","POST"])
def solicitar_cita (nombre):
    if request.method == "POST":
      new_cita = {
        "paciente": nombre,
        "doctor": "",
        "fecha": request.form ["fecha"],
        "hora": request.form ["hora"],
        "motivo": request.form ["motivo"],
        "estado": "pendiente"
       }
      citas.append (new_cita)
      return redirect ("/login_paciente/" + nombre)
          
@app.route ("/<string:enfermera>/<string:motivo>", methods = ["GET", "POST", "PUT"])
def aceptar_cita_enfermero (motivo, enfermera):
     if request.method == "POST":
       busqueda_cita = [cita for cita in citas if cita ["motivo"] == motivo]
       busqueda_cita [0]["doctor"] = request.form ["doctor"]
       busqueda_cita [0]["estado"] = "aceptada"

       return redirect ("/login_enfermera/"+ enfermera)

@app.route ("/aceptar_cita_de_doctor/<string:doctor>/<string:motivo>", methods = ["GET", "POST", "PUT"])
def aceptar_cita_de_doctor (motivo, doctor):
     if request.method == "POST":
       busqueda_cita = [cita for cita in citas if cita ["motivo"] == motivo]
       busqueda_cita [0]["doctor"] = doctor
       busqueda_cita [0]["estado"] = "aceptada"
       return redirect ("/login_doctor/"+ doctor)


@app.route ("/rechazar/<string:enfermera>/<string:motivo>", methods = ["POST" , "PUT", "DELETE"])
def rechazar_cita(motivo, enfermera):
   if request.method == "POST":
       busqueda_cita = [cita for cita in citas if cita ["motivo"] == motivo]
       citas.remove (busqueda_cita [0])
       return redirect ("/login_enfermera/"+ enfermera)

@app.route ("/rechazar_doctor/<string:doctor>/<string:motivo>", methods = ["POST" , "PUT", "DELETE"])
def rechazar_cita_doc(motivo, doctor):
   if request.method == "POST":
       busqueda_cita = [cita for cita in citas if cita ["motivo"] == motivo]
       citas.remove (busqueda_cita [0])
       return redirect ("/login_doctor/"+ doctor)

@app.route ("/completar_doctor/<string:doctornombre>/<string:motivo>", methods = ["POST" , "PUT", "DELETE"])
def completar_cita_doc(motivo, doctornombre):
   if request.method == "POST":
       busqueda_cita = [cita for cita in citas if cita ["motivo"] == motivo]
       busqueda_doctor = [doctor0 for doctor0 in doctores if doctor0 ["nombre"] == doctornombre]
       busqueda_doctor[0]["citas_atendidas"] = int (busqueda_doctor[0]["citas_atendidas"]) + 1
       citas.remove (busqueda_cita [0])
       print (busqueda_doctor[0])
       return redirect ("/login_doctor/"+ doctornombre)



#----------------------------------------------------------------------------------------
#                                 LISTADO
#----------------------------------------------------------------------------------------

@app.route("/admin_listado")
def PDF ():
  return render_template ("Generar PDF.html")

@app.route ("/generar_listado_de_pacientes", methods = ["GET", "POST"])
def imprimir_listado_pacientes ():
  if request.method == "POST":
    css = ["estilo.css"]
    html = render_template  ("tabla_muestra_pacientes.html", lista_pacientes = pacientes)
    pdf = pdfkit.from_string (html, False, css = "static/tabla_muestra/estilo.css")

    response = make_response  (pdf)
    response.headers ["Content-Type"] = "application/pdf"
    response.headers ["Content-Disposition"] = "inline; filename = Tabla pacientes.pdf"

    return response

@app.route ("/generar_listado_de_enfermeros", methods = ["GET", "POST"])
def imprimir_listado_enfermeros ():
  if request.method == "POST":
    css = ["estilo.css"]
    html = render_template  ("tabla_muestra_enfermeros.html", lista_enfermeros = enfermeras)
    pdf = pdfkit.from_string (html, False, css = "static/tabla_muestra/estilo.css")

    response = make_response  (pdf)
    response.headers ["Content-Type"] = "application/pdf"
    response.headers ["Content-Disposition"] = "inline; filename = Tabla enfermeros.pdf"

    return response

@app.route ("/generar_listado_de_doctores", methods = ["GET", "POST"])
def imprimir_listado_doctores ():
  if request.method == "POST":
    css = ["estilo.css"]
    html = render_template  ("tabla_muestra_doctores.html", lista_doctores = doctores)
    pdf = pdfkit.from_string (html, False, css = "static/tabla_muestra/estilo.css")

    response = make_response  (pdf)
    response.headers ["Content-Type"] = "application/pdf"
    response.headers ["Content-Disposition"] = "inline; filename = Listado de doctores.pdf"

    return response

@app.route ("/generar_listado_de_medicamentos", methods = ["GET", "POST"])
def imprimir_listado_medicamentos ():
  if request.method == "POST":
    css = ["estilo.css"]
    html = render_template  ("tabla_muestra_medicamentos.html", lista_medicamentos= medicamentos)
    pdf = pdfkit.from_string (html, False, css = "static/tabla_muestra/estilo.css")

    response = make_response  (pdf)
    response.headers ["Content-Type"] = "application/pdf"
    response.headers ["Content-Disposition"] = "inline; filename = Listado medicamentos .pdf"

    return response

@app.route ("/generar_factura", methods = ["GET", "POST"])
def generar_factura ():
  if request.method == "POST":
  
    html = render_template  ("tabla factura.html", paciente_nombre = request.form ["paciente"], doctor_nombre = request.form ["doctor"], fecha = request.form ["fecha"] , precio_consulta = request.form ["consulta"], precio_internado = request.form ["internado"] , precio_operacion = request.form ["operacion"], total = request.form ["total"] )
    pdf = pdfkit.from_string (html, False, css = "static/tabla_muestra/estilo_factura.css")

    response = make_response  (pdf)
    response.headers ["Content-Type"] = "application/pdf"
    response.headers ["Content-Disposition"] = "inline; filename = Factura.pdf"

    return response

@app.route ("/generar_pedido/<paciente>", methods = ["GET", "POST"])
def generar_pedido(paciente):
  if request.method == "POST":

    total = []
    for pedido in pedidos:
        total0 = pedido["cantidad"]*pedido["precio_unitario"]
        total.append (total0)
    total1 = (sum(total))
  
    html = render_template  ("tabla pedido.html", paciente_nombre = paciente, lista_pedidos = pedidos , total = total1)
    pdf = pdfkit.from_string (html, False, css = "static/tabla_muestra/estilo_factura.css")

    response = make_response  (pdf)
    response.headers ["Content-Type"] = "application/pdf"
    response.headers ["Content-Disposition"] = "inline; filename = Pedido.pdf"

    return response

@app.route ("/generar_receta", methods = ["GET", "POST"])
def generar_receta ():
  if request.method == "POST":
    busqueda_enfermedades = [enfermedad for enfermedad in enfermedades if enfermedad ["nombre"] == request.form ["enfermedad"].lower()]
    if (len (busqueda_enfermedades) > 0):
      busqueda_enfermedades [0]["frecuencia"] = int (busqueda_enfermedades [0]["frecuencia"] ) + 1 
    else:
       new_enfermedad = {
        "nombre":request.form ["enfermedad"].lower(),
        "frecuencia": 1
       }
       enfermedades.append (new_enfermedad)
    print (enfermedades)


    html = render_template  ("tabla receta.html", paciente_nombre = request.form ["paciente"], fecha = request.form ["fecha"], padecimiento =  request.form ["enfermedad"] , descripcion = request.form ["descripcion"])
    pdf = pdfkit.from_string (html, False, css = "static/tabla_muestra/estilo_factura.css")

    response = make_response  (pdf)
    response.headers ["Content-Type"] = "application/pdf"
    response.headers ["Content-Disposition"] = "inline; filename = Receta.pdf"

    return response

@app.route ("/top3_doctores", methods = ["GET", "POST"])
def top3_doctores ():
    if request.method == "POST":
     doctores.sort (key = itemgetter ("citas_atendidas"), reverse = True)

     pt1 = doctores [0]["nombre"] + " " + doctores [0]["apellido"]
     pt2 = doctores [1]["nombre"] + " " + doctores [1]["apellido"]
     pt3 = doctores [2]["nombre"] + " " + doctores [2]["apellido"]

     v1 = doctores [0]["citas_atendidas"] 
     v2 = doctores [1]["citas_atendidas"] 
     v3 = doctores [2]["citas_atendidas"] 
  
     html = render_template  ("top 5 doctores.html", puesto1 = pt1, visitas1 = v1,   puesto2 = pt2,  visitas2 = v2,   puesto3 = pt3 , visitas3 = v3 )
     pdf = pdfkit.from_string (html, False, css = "static/tabla_muestra/estilo_podio.css")

     response = make_response  (pdf)
     response.headers ["Content-Type"] = "application/pdf"
     response.headers ["Content-Disposition"] = "inline; filename = Top doctores.pdf"

     return response

@app.route ("/top5_medicamentos", methods = ["GET", "POST"])
def top5_medicamentos ():
    if request.method == "POST":
     medicamentos.sort (key = itemgetter ("vendidos"), reverse = True)

     pt1 = medicamentos [0]["nombre"] 
     pt2 = medicamentos [1]["nombre"] 
     pt3 = medicamentos [2]["nombre"] 
     pt4 = medicamentos [3]["nombre"] 
     pt5 = medicamentos [4]["nombre"] 

     v1 = medicamentos [0]["vendidos"] 
     v2 = medicamentos [1]["vendidos"] 
     v3 = medicamentos [2]["vendidos"] 
     v4 = medicamentos [3]["vendidos"] 
     v5 = medicamentos [4]["vendidos"] 
  
     html = render_template  ("top 5medicamentos.html", clave1 = "Top 5 medicamentos", clave2 = "Cantidad de ventas", clave3 = "Top 5 medicamentos mas vendidos" , puesto1 = pt1, visitas1 = v1,   puesto2 = pt2,  visitas2 = v2,   puesto3 = pt3 , visitas3 = v3, puesto4 = pt4 , visitas4 = v4, puesto5 = pt5 , visitas5 = v5 )
     pdf = pdfkit.from_string (html, False, css = "static/tabla_muestra/estilo_podio.css")

     response = make_response  (pdf)
     response.headers ["Content-Type"] = "application/pdf"
     response.headers ["Content-Disposition"] = "inline; filename = Top doctores.pdf"

     return response

@app.route ("/top5_enfermedades", methods = ["GET", "POST"])
def top5_enfermedades ():
    if request.method == "POST":
     enfermedades.sort (key = itemgetter ("frecuencia"), reverse = True)
     if (len (enfermedades) == 0):
       pt1 = "" 
       pt2 = ""
       pt3 = ""
       pt4 = ""
       pt5 = ""

       v1 = ""
       v2 = ""
       v3 = ""
       v4 = ""
       v5 = ""
     elif (len(enfermedades) == 1):
       pt1 = enfermedades [0]["nombre"] 
       pt2 = ""
       pt3 = ""
       pt4 = ""
       pt5 = ""

       v1 = enfermedades [0]["frecuencia"] 
       v2 = ""
       v3 = ""
       v4 = ""
       v5 = ""
     elif (len(enfermedades) == 2):
       pt1 = enfermedades [0]["nombre"] 
       pt2 = enfermedades [1]["nombre"] 
       pt3 = ""
       pt4 = ""
       pt5 = ""

       v1 = enfermedades [0]["frecuencia"] 
       v2 = enfermedades [1]["frecuencia"] 
       v3 = ""
       v4 = ""
       v5 = ""
     elif (len(enfermedades) == 3):
       pt1 = enfermedades [0]["nombre"] 
       pt2 = enfermedades [1]["nombre"] 
       pt3 = enfermedades [2]["nombre"] 
       pt4 = ""
       pt5 = ""

       v1 = enfermedades [0]["frecuencia"] 
       v2 = enfermedades [1]["frecuencia"] 
       v3 = enfermedades [2]["frecuencia"] 
       v4 = ""
       v5 = ""
     elif (len(enfermedades) == 4):
       pt1 = enfermedades [0]["nombre"] 
       pt2 = enfermedades [1]["nombre"] 
       pt3 = enfermedades [2]["nombre"] 
       pt4 = enfermedades [3]["nombre"] 
       pt5 = ""

       v1 = enfermedades [0]["frecuencia"] 
       v2 = enfermedades [1]["frecuencia"] 
       v3 = enfermedades [2]["frecuencia"] 
       v4 = enfermedades [3]["frecuencia"] 
       v5 = ""

     elif (len(enfermedades) >= 5):

       pt1 = enfermedades [0]["nombre"] 
       pt2 = enfermedades [1]["nombre"] 
       pt3 = enfermedades [2]["nombre"] 
       pt4 = enfermedades [3]["nombre"] 
       pt5 = enfermedades [4]["nombre"] 

       v1 = enfermedades [0]["frecuencia"] 
       v2 = enfermedades [1]["frecuencia"] 
       v3 = enfermedades [2]["frecuencia"] 
       v4 = enfermedades [3]["frecuencia"] 
       v5 = enfermedades [4]["frecuencia"] 
  
     html = render_template  ("top 5medicamentos.html", clave1 = "Top 5 enfermedades", clave2 = "Casos registrados", clave3 = "Top 5 enfermedades mas comunes" , puesto1 = pt1, visitas1 = v1,   puesto2 = pt2,  visitas2 = v2,   puesto3 = pt3 , visitas3 = v3, puesto4 = pt4 , visitas4 = v4, puesto5 = pt5 , visitas5 = v5 )
     pdf = pdfkit.from_string (html, False, css = "static/tabla_muestra/estilo_podio.css")

     response = make_response  (pdf)
     response.headers ["Content-Type"] = "application/pdf"
     response.headers ["Content-Disposition"] = "inline; filename = Top enfermedades.pdf"

     return response




if __name__ == "__main__":
   app.run ("0.0.0.0", port = 4545, debug = True)

## python Main.py
