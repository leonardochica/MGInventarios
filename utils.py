import os
import re
from flask import request
from validate_email import validate_email
from werkzeug.utils import secure_filename


pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{8,}$"
user_reguex = "^[a-zA-Z0-9 _.-]+$"
id_reguex = "^[0-9]+$"
F_ACTIVE = 'ACTIVE'
F_INACTIVE = 'INACTIVE'
EMAIL_APP = 'EMAIL_APP'
REQ_ACTIVATE = 'REQ_ACTIVATE'
REQ_FORGOT = 'REQ_FORGOT'
U_UNCONFIRMED = 'UNCONFIRMED'
U_CONFIRMED = 'CONFIRMED'


def isEmailValid(email):
    is_valid = validate_email(email)

    return is_valid


def isUsernameValid(user):
    if re.search(user_reguex, user):
        return True
    else:
        return False


def isPasswordValid(password):
    if re.search(pass_reguex, password):
        return True
    else:
        return False


def isIdValid(id):
    if re.search(id_reguex, id):
        return True
    else:
        return False

def isNombreValid(nombre):
    if re.search(user_reguex, nombre):
        return True
    else:
        return False


def isCantidadValid(cantidad):
    if re.search(id_reguex, cantidad):
        return True
    else:
        return False


# UPLOAD_FOLDER = '/path/to/the/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']
# app.config['UPLOAD_FOLDER'] = 'UPLOAD_FOLDER'  # configuracion para directorio en el servidor

def validarImagen():
    msj = ""
    archivoCargado = request.files['imagen']
    nombreArchivo = secure_filename(archivoCargado.filename)

    if nombreArchivo != '':
        archivoExtension = os.path.splitext(nombreArchivo)[1]  # divido el archivo para ver la extension de ese archivo
        if archivoExtension not in ['.jpg', '.png', '.jpeg']:
            msj = "Tipo de archivo no es válido"
            return (msj,"Error")

        # msj = f"El archivo {nombreArchivo} cargo exitosamente"
        archivoCargado.save(
            'static/imagenes/cargadas/' + nombreArchivo)  # graba la imagen donde este guardado este archivo de python app.py
        # archivoCargado.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreArchivo))  # Se guarda en un directorio en el servidor
        print(archivoCargado.filename)
        print(type(archivoCargado))

        img = convertirADatoBinario('static/imagenes/cargadas/'+archivoCargado.filename)
        # print(img)
        return (msj,img)

    else:
        msj = "Por favor cargar un archivo"
        return (msj,"Error")

def convertirADatoBinario(imagen):
    with open(imagen, 'rb') as archivo:
        blob = archivo.read()
    return blob


def convertirANombreImagen_lista(productos):
    lista = []
    for p in productos:
        registro_accesorio = list(p)
        registro_accesorio[3] = convertirBinarioAImagen(p[0],p[3])
        p = tuple(registro_accesorio)
        lista.append(p)
    return lista





def convertirBinarioAImagen(id_foto,binario):
    with open('static/imagenes/cargadas/accesorio_{}.jpg'.format(id_foto),'wb') as archivo:
        archivo.write(binario)

    return "accesorio_{}.jpg".format(id_foto)
