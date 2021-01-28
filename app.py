import functools
import os
from flask import Flask, render_template, request, flash, redirect, url_for, session, g
from markupsafe import escape
from utils import isUsernameValid, isPasswordValid, isEmailValid, isIdValid, isCantidadValid, isNombreValid, validarImagen, convertirANombreImagen_lista, convertirADatoBinario
import yagmail as yagmail
from datos import productos
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from random import SystemRandom
from datetime import datetime



app = Flask(__name__)


app.secret_key = os.urandom(24)


@app.route('/', methods=["GET","POST"])
def iniciar():
  if request.method == 'GET':
    return render_template("index.html")
  else:
    try:
      db = get_db()
      error = None

      usuario = escape(request.form['usuario'])
      password = escape(request.form['password'])
      esAdmin = request.form.get('esAdmin')


      if (esAdmin == "a"):
        esAdmin2 = True
      else:
        esAdmin2 = False

      msjeUs = ""
      msjePwd = ""

      if not usuario:
        msjeUs = 'Debe ingresar el usuario'

      if not password:
        msjePwd = 'Contraseña requerida'


      user = db.execute(
        'SELECT * FROM usuario WHERE nombre = ? AND rol= ?', (usuario, esAdmin2)
      ).fetchone()

      if (esAdmin == 'a'):  # si es administrador

        if (msjeUs != "" or msjePwd != ""):   # si hay errores en validaciones
          return render_template('index.html', mensajeUsuario=msjeUs, mensajeContrasena=msjePwd)
        else:
          if user is None:    # si no se encontro el registro en la base de datos
            error = 'Usuario inválido'
            return render_template('index.html', mensajeValidacion=error)
          else:
            if check_password_hash(user[3],password):
              session.clear()
              session['admin_id'] = user[0]  # sesion para registro en el campo ID
              return redirect(url_for('adminPrincipal',nombre=user[1]))
              # return render_template('administracion_productos.html', nombreAdministrador=user[1])
            
            else:
              return render_template('index.html', mensajeValidacion="Contraseña inválida")
      else:
        if (msjeUs != "" or msjePwd != ""):
          return render_template('index.html', mensajeUsuario=msjeUs, mensajeContrasena=msjePwd)
        else:
          if user is None:
            error = 'Usuario inválido'
            return render_template('index.html', mensajeValidacion=error)
          else:
            if check_password_hash(user[3], password):
              session.clear()
              session['user_id'] = user[0]
              return redirect(url_for('usuarioPrincipal',nombre=user[1]))
              # return render_template('usuario.html', nombreUsuario=user[1])
            else:
              return render_template('index.html', mensajeValidacion="Contraseña inválida")
          
        

    except:
      return render_template('index.html', mensajeValidacion="Error en la Pagina")
      

# Chequea si hay un usuario en la sesion y usa sus datos de la base de datos
@app.before_request
def load_logged_in_user():
  user_id = session.get('user_id')

  if user_id is None:  # si no hay usuario en la sesion
    g.user = None
  else:
    g.user = get_db().execute(
      'SELECT * FROM usuario WHERE id = ?', (user_id,)
    ).fetchone()

@app.before_request
def load_logged_in_admin():
  admin_id = session.get('admin_id')

  if admin_id is None:  # si no hay admin en la sesion
    g.admin = None
  else:
    g.admin = get_db().execute(
      'SELECT * FROM usuario WHERE id = ?', (admin_id,)
    ).fetchone()

# Chequea si hay un usuario cargado en la sesion para usarlo en las rutas que pueda acceder
def login_required_admin(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.admin is None:
      return redirect(url_for('iniciar'))
    return view(**kwargs)
  
  return wrapped_view

def login_required_user(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('iniciar'))
    return view(**kwargs)
  
  return wrapped_view



# Recuperar Contrasena
@app.route('/recuperarcontrasena/', methods=['GET','POST'])
def recuperarPwd():
  if request.method == "GET":
    return render_template("recuperar_contrasena.html")
  else:
    try:
      db = get_db()
      error = "Este correo no está registrado"

      email = escape(request.form['correo'])

      msjCorreo = ''

      if not email:
        msjCorreo = 'Por favor ingresar su correo'

      correo = db.execute(
        'SELECT * FROM usuario WHERE correo = ?', (email,)
      ).fetchone()

      if msjCorreo == '':
        if correo is not None:
           # Variables para crear contraseña aleatoria
          longitud = 8
          valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
          cryptogen = SystemRandom()
          newPwd = ""
          while longitud > 0:
            newPwd = newPwd + cryptogen.choice(valores)
            longitud = longitud - 1

          newPwdHash = generate_password_hash(newPwd)

          db.execute(
            'UPDATE usuario SET contraseña = ? WHERE correo = ?', (newPwdHash, email)
          )
          db.commit()

          yag = yagmail.SMTP('testmg202021@gmail.com','Prueba1234')
          yag.send(to=email, subject='MG Inventario: Recupere su Contraseña', contents=f'Tu contraseña es {newPwd}, por favor ingresa de nuevo <a href="http://localhost:5000/">aqui</a>')
          return render_template("recuperar_contrasena.html", mensajeConfirmado = "Un correo se ha enviado para reestablecer la contraseña")
        else:
          return render_template("recuperar_contrasena.html", mensajeCorreo=error)
      else:
        return render_template("recuperar_contrasena.html",  mensajeCorreo=msjCorreo)
    except:
      return render_template('recuperar_contrasena.html', mensajeConfirmado="Error en la página")


def consultarUsuario(nombre):
  db = get_db()
  query = db.execute('SELECT id FROM usuario WHERE nombre = ?', (nombre,)).fetchone()
  idUsuario = query[0]
  return idUsuario


@app.route('/administracion/<string:nombre>')
@login_required_admin
def adminPrincipal(nombre):
  db = get_db()
  productos = db.execute('SELECT * FROM accesorios').fetchall()

  listaAccesorios = convertirANombreImagen_lista(productos)
  return render_template("administracion_productos.html", productosLista=listaAccesorios, nombreAdministrador=nombre, nombreID=consultarUsuario(nombre))

# Para INCLUIR EN EL URL EL NOMBRE DEL ADMINISTRADOR Y SE VEA AL LADO DEL AVATAR
# @app.route('/administracion/<string:nombre>')
# def adminPrincipal(nombre):
#   return render_template("administracion_productos.html", productosLista=productos,nombreAdministrador=nombre)

@app.route('/administracion/')
@login_required_admin
def adminPrincipalActualizar():
    return redirect(url_for('iniciar'))


@app.route('/administracion/<string:nombre>/registro/', methods=['GET','POST'])
@login_required_admin
def adminRegistro(nombre):
  if request.method == 'GET':
    return render_template("registro_usuarios.html",nombreAdministrador=nombre,nombreID=consultarUsuario(nombre))
  else:
    try:
      db = get_db()

      usuario = escape(request.form['usuario'])
      password = escape(request.form['password'])
      email = escape(request.form['correo'])

      msjeUs = ""
      msjePwd = ""
      msjCorreo = ""

      if (not isUsernameValid(usuario)):
        msjeUs = "Usuario no es valido"

      if (not isPasswordValid(password)):
        msjePwd = "Password no es valido"

      if (not isEmailValid(email)):
        msjCorreo = "Ingresar un correo valido"

      if not usuario:
        msjeUs = 'Debe ingresar el usuario'

      if not password:
        msjePwd = 'Contraseña requerida'

      if not email:
        msjCorreo= "Debe ingresar un correo"

      if (msjeUs != "" or msjePwd != "" or msjCorreo != ""):
        return render_template("registro_usuarios.html", mensajeUsuario=msjeUs, mensajeContrasena=msjePwd, mensajeCorreo=msjCorreo,nombreAdministrador=nombre,nombreID=consultarUsuario(nombre))
      else:
        # Validar para que no se crea un usuario con un nombre existente
        if db.execute('SELECT id FROM usuario WHERE nombre = ?', (usuario,)).fetchone() is not None:
          msjeUs = 'Este usuario ya existe. Intente con otro.'
          return render_template("registro_usuarios.html", mensajeUsuario=msjeUs,nombreAdministrador=nombre,nombreID=consultarUsuario(nombre))
        
        # Validar para que no se crea un usuario con un correo existente
        if db.execute('SELECT id FROM usuario WHERE correo = ?', (email,)).fetchone() is not None:
          msjCorreo = 'El correo ya existe en la base de datos'
          return render_template("registro_usuarios.html", mensajeCorreo=msjCorreo,nombreAdministrador=nombre,nombreID=consultarUsuario(nombre))

        pwdHash = generate_password_hash(password)
        db.execute(
          'INSERT INTO usuario (nombre, correo, contraseña) VALUES (?,?,?)',
          (usuario, email, pwdHash)
        )
        db.commit()

        yag = yagmail.SMTP('testmg202021@gmail.com', 'Prueba1234')
        yag.send(to=email, subject='MG Inventario: Nueva Cuenta Usuario',contents=f'Su nueva cuenta de usuario es {usuario} y su contraseña {password}')
        return render_template("registro_usuarios.html", mensajeNuevoUs="Creación de usuario exitoso",nombreAdministrador=nombre,nombreID=consultarUsuario(nombre))

    except:
      return render_template('registro_usuarios.html', mensajeNuevoUs="Error en la página",nombreAdministrador=nombre,nombreID=consultarUsuario(nombre))



@app.route('/administracion/<string:nombreUser>/crearAccesorio/', methods=['GET','POST'])
@login_required_admin
def adminCrearAccesorio(nombreUser):
  try:
    if request.method == 'GET':
      return render_template("crear_accesorio.html",nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))
    else:
      db = get_db()

      id = escape(request.form['identificador'])
      nombre = escape(request.form['producto'])
      cantidad = escape(request.form['cantidad'])

      msjId = ""
      msjNombre = ""
      msjCantidad = ""

      # ARREGLAR VALIDACION PARA ID
      if (not isIdValid(id)):
        msjId = 'Ingresar un ID válido'

      if (not isNombreValid(nombre)):
        msjNombre = 'Ingresar un nombre sólo incluyendo letras o números'

      if (not isCantidadValid(cantidad)):
        msjCantidad = 'Ingresar una cantidad válida'

      if not id:
        msjId = 'Debe ingresar un ID'

      if not nombre:
        msjNombre = 'Debe ingresar un nombre para el accesorio'

      if not cantidad:
        msjCantidad = 'Debe ingresar una cantidad'

      # Llamar a la funcion validar Imagen para que retorne un mensaje
      msjImagen = validarImagen()

      # Si hay errores en validacion:
      if (msjId != "" or msjCantidad != "" or msjImagen[1] == "Error"):
        return render_template("crear_accesorio.html", mensajeId=msjId, mensajeNombre=msjNombre, mensajeCantidad=msjCantidad, mensajeImagen=msjImagen[0],nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))

      # Si la validacion fue exitosa:
      else:
        # Verifica si este ID ya existe
        if db.execute('SELECT id FROM accesorios WHERE id = ?', (id,)).fetchone() is not None:
          msjId = 'Este ID para este accesorio ya existe'
          return render_template("crear_accesorio.html", mensajeError=msjId,nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))


      
        db.execute(
          'INSERT INTO accesorios (id, nombre, cantidad, imagen) VALUES (?,?,?,?)',
          (id, nombre, cantidad, msjImagen[1])
        )
        db.commit()
        return render_template("crear_accesorio.html", mensajeConfirmado="Accesorio Creado",nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))

  except:
    return render_template("crear_accesorio.html", mensajeError="Error en la página",nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))
      
@app.route('/administracion/<string:nombreUser>/editarAccesorio/', methods=['GET','POST'])
@login_required_admin
def adminEditarAccesorio(nombreUser):
  try:
    if request.method == 'GET':
      db = get_db()
      productos = db.execute('SELECT * FROM accesorios').fetchall()
      
      listaAccesorios = convertirANombreImagen_lista(productos)
      return render_template("actualizar_eliminar.html", productosLista=listaAccesorios,nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))
    else:
      msjNombre = ""
      msjCantidad = ""

      archivoCargado = request.files['accesorioImagen']
      nombreArchivo = secure_filename(archivoCargado.filename)

      print(nombreArchivo)

      db = get_db()
      productos = db.execute('SELECT * FROM accesorios').fetchall()
      
      listaAccesorios = convertirANombreImagen_lista(productos)

      id = escape(request.form['id'])
      nombre = escape(request.form['accesorioNombre'])
      cantidad = escape(request.form['accesorioCantidad'])

      print(id)
      print(nombre)
      print(cantidad)

      # Codigo para ACTUALIZAR
      if request.form['actualizar_eliminar'] == 'Actualizar':
        if (not isNombreValid(nombre)):
          msjNombre = 'Ingresar un nombre sólo incluyendo letras o números'
        if (not isCantidadValid(cantidad)):
          msjCantidad = 'Ingresar una cantidad válida'

        if not nombre and not cantidad:
          error = "Debe ingresar un nombre y una cantidad para el producto"
          return render_template('actualizar_eliminar.html',msjError=error,productosLista=listaAccesorios,nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))
        elif not nombre:
          error = "Debe ingresar un nombre para el producto"
          return render_template('actualizar_eliminar.html', msjError=error, productosLista=listaAccesorios,nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))
        elif not cantidad:
          error = "Debe ingresar una cantidad para el producto"
          return render_template('actualizar_eliminar.html', msjError=error, productosLista=listaAccesorios,nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))

        if msjNombre != "" or msjCantidad != "":
          return render_template('actualizar_eliminar.html', msjError=f"{msjNombre}. {msjCantidad}", productosLista=listaAccesorios,nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))

        if nombreArchivo == "":
          db.execute(
            'UPDATE accesorios SET nombre = ?, cantidad = ? WHERE id = ?', (nombre, cantidad, id)
          )
          db.commit()
          productos = db.execute('SELECT * FROM accesorios').fetchall()
          listaAccesorios = convertirANombreImagen_lista(productos)
          return render_template('actualizar_eliminar.html', msjError="Accesorio actualizado", productosLista=listaAccesorios,nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))

        else:
          archivoCargado.save('static/imagenes/cargadas/' + nombreArchivo)
          imgBinario = convertirADatoBinario('static/imagenes/cargadas/' + nombreArchivo)
          db.execute(
            'UPDATE accesorios SET nombre = ?, cantidad = ?, imagen = ? WHERE id = ?', (nombre, cantidad, imgBinario, id)
          )
          db.commit()
          productos = db.execute('SELECT * FROM accesorios').fetchall()
          listaAccesorios = convertirANombreImagen_lista(productos)
          return render_template('actualizar_eliminar.html', msjError="Accesorio actualizado",
                                 productosLista=listaAccesorios,nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))


        # db.execute(
        #   'UPDATE usuario SET contraseña = ? WHERE correo = ?', (newPwdHash, email)
        # )
        # db.commit()


        # Codigo para ELIMINAR
      elif request.form['actualizar_eliminar'] == 'Eliminar':
        db.execute(
            'DELETE FROM accesorios WHERE id = ?', (id,)
          )
        db.commit()
        productos = db.execute('SELECT * FROM accesorios').fetchall()
        listaAccesorios = convertirANombreImagen_lista(productos)
        return render_template('actualizar_eliminar.html', msjError="Accesorio eliminado",
                                 productosLista=listaAccesorios,nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))
  

  except:
    return "Error en la Pagina"

      
@app.route('/administracion/<string:nombreUser>/consultarUsuario/', methods=['GET','POST'])
@login_required_admin
def adminConsultaUsuario(nombreUser):
  try:
    if request.method == 'GET':
      db = get_db()
      listaUsuarios = db.execute('SELECT * FROM usuario_consulta').fetchall()
      
      
      return render_template("consulta_usuarios.html", usuariosLista=listaUsuarios,nombreAdministrador=nombreUser,nombreID=consultarUsuario(nombreUser))
  except:
    return "Error en la pagina"

@app.route('/usuario/<string:nombre>/')
@login_required_user
def usuarioPrincipal(nombre):
  db = get_db()
  productos = db.execute('SELECT * FROM accesorios').fetchall()

  listaAccesorios = convertirANombreImagen_lista(productos)

  return render_template("usuario.html", productosLista=listaAccesorios, nombreUsuario=nombre,nombreID=consultarUsuario(nombre))

@app.route('/usuario/<string:nombre>/<int:idProducto>/')
@login_required_user
def usuarioConsulta(nombre,idProducto):
  db = get_db()
  usuarioID=consultarUsuario(nombre)

  ahora = datetime.now()  # Hora actual
  fecha_formato = ahora.strftime("%d/%m/%Y %H:%M:%S")  # Hora en formato: 16/12/2020 21:39:14

  db.execute(
          'INSERT INTO usuario_consulta (usuario_id, usuario_nombre, accesorio_id, fecha_hora) VALUES (?,?,?,?)',
          (usuarioID, nombre, idProducto, fecha_formato)
        )
  db.commit()
  productos = db.execute('SELECT * FROM accesorios').fetchall()

  listaAccesorios = convertirANombreImagen_lista(productos)


  print(ahora)
  return render_template("usuario.html", productosLista=listaAccesorios, nombreUsuario=nombre,nombreID=consultarUsuario(nombre))



@app.route('/usuario/')
@login_required_user
def usuario():
    return redirect(url_for('iniciar'))
    # db = get_db()
    # accesorio = db.execute(
    #     'SELECT cantidad FROM accesorios WHERE id = ?', (idProducto,)
    #   ).fetchone()
    # return render_template("usuario.html",)
    # MIRAR OTRA OPCION
  
  



@app.route('/cerrar/')
def cerrarSesion():
  session.clear()
  return redirect(url_for('iniciar'))
# @app.route('/usuario/<string:nombre>')
# def usuarioPrincipal(nombre):
#   return render_template("usuario.html", productosLista=productos,nombreUsuario=nombre)

# Refrescar Cache
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    # r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# if __name__ == "__main__":
#   app.run(port='80',host='0.0.0.0')
if __name__ == "__main__":
  app.run(port='443',host='0.0.0.0',ssl_context=('cert01.pem','llav01.pem'))