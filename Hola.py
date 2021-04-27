from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask (__name__)

@app.route ("/", methods = ["GET", "POST"]) 
def saludar (): 
    titulo = "inicio uwu"
    lista = {"JUAN", "PEDRO", "PABLO"}
    return render_template ("signup.html", titulo0 = titulo) #Se le manda parametros al html

    
@app.route ("/login", methods = ["GET","POST"])
def login ():  
    if request.method == "POST":
         return "credenciales ingresadas"
    return render_template ("index.html")
    
if __name__ == "__main__":
   app.run ("0.0.0.0", port = 4545, debug = True)