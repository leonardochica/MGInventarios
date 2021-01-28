// Pagina LOGIN
// ==========================================
function validarFormulario(e) {
  let usuarioValido = validarUsuario();
  let passwordValido = validarPassword();
  if (!usuarioValido || !passwordValido) {
    e.preventDefault();
  }
}

// Otra forma de usar eventos
// inputUsuario.addEventListener('keyup',validarUsuario);
// inputPassword.addEventListener('keyup',validarPassword);

// Validar Usuario
function validarUsuario() {
  const inputUsuario = document.getElementById("usuario");
  let valid;
  let errorUsuario = document.querySelector(".forma__error--usuario");
  let msgUsuario;

  if (inputUsuario.value.trim() == "") {
    msgUsuario = "Por favor llenar este campo";
    inputUsuario.style.border = "1px solid var(--color-error)";
    valid = false;
  // } else if (inputUsuario.value.length < 8) {
  //   msgUsuario = "Requiere minimo 8 caracteres";
  //   inputUsuario.style.border = "1px solid var(--color-error)";
  //   valid = false;
  } else {
    valid = true;
    inputUsuario.style.border = "1px solid var(--color-medio)";
  }
  errorUsuario.textContent = msgUsuario;
  return valid;
}

// Validar Password
function validarPassword() {
  const inputPassword = document.getElementById("password");
  let valido;
  let errorPassword = document.querySelector(".forma__error--password");

  let msgPassword;

  if (inputPassword.value.trim() == "") {
    msgPassword = "Por favor llenar este campo";
    inputPassword.style.border = "1px solid var(--color-error)";
    valido = false;
  } else if (inputPassword.value.length < 8) {
    msgPassword = "Requiere minimo 8 caracteres";
    inputPassword.style.border = "1px solid var(--color-error)";
    valido = false;
  } else {
    valido = true;
    inputPassword.style.border = "1px solid var(--color-medio)";
  }
  errorPassword.textContent = msgPassword;

  return valido;
}

// Mostrar y Ocultar Password
ver = true;
function mostrarPwd() {
  let inputPassword = document.querySelector(".input__password");
  let ojoAbierto = document.querySelector(".fa-eye");
  let ojoCerrado = document.querySelector(".fa-eye-slash");

  if (ver) {
    inputPassword.type = "text";
    ojoAbierto.style.visibility = "hidden";
    ojoCerrado.style.visibility = "visible";
    ver = false;
  } else {
    inputPassword.type = "password";
    ojoAbierto.style.visibility = "visible";
    ojoCerrado.style.visibility = "hidden";
    ver = true;
  }
}

// Pagina OLVIDAR PASSWORD
// ==========================================

function validarFormaPassword(e) {
  let correoValido = validarCorreo();

  if (!correoValido) {
    e.preventDefault();
  }
}

function validarCorreo() {
  const correoInput = document.getElementById("correo");
  const errorCorreo = document.querySelector(".forma__error--correo");
  let valido;
  let msgCorreo;

  if (correoInput.value.trim() == "") {
    msgCorreo = "Por favor llenar este campo";
    correoInput.style.border = "1px solid var(--color-error)";
    valido = false;
  } 
  else if (!correoInput.validity.valid) {
    msgCorreo = "Por favor ingrese un correo valido";
    correoInput.style.border = "1px solid var(--color-error)";
    valido = false;
  } else {
    valido = true;
    correoInput.style.border = "1px solid var(--color-medio)";
  }

  errorCorreo.textContent = msgCorreo;

  return valido;
}

// Pagina REGISTRAR USUARIOS
// ==========================================
function validarFormaRegistro(e) {
  let usuarioValido = validarUsuario();
  let passwordValido = validarPassword();
  let correoValido = validarCorreo();

  if (!usuarioValido || !passwordValido || !correoValido) {
    e.preventDefault();
  }
}

// Pagina CREAR ACCESORIO
// ==========================================
function validarFormaCrearProducto(e) {
  let idValido = validarID();
  let productoValido = validarProducto();
  let cantidadValida = validarCantidad();
  // let imagenValida = validarImagen();

  if (!idValido || !productoValido || !cantidadValida) {
    e.preventDefault();
  }

}


function validarID() {
  const idInput = document.getElementById("identificador");
  const errorID = document.querySelector(".forma__error--productoID");

  let valido;
  let msgID;

  if (idInput.value.trim() == "") {
    msgID = "Por favor llenar este campo";
    idInput.style.border = "1px solid var(--color-error)";
    valido = false;
  } else if (!Number.isInteger(Number(idInput.value))) {
    msgID = "Por favor ingresa un numero valido";
    idInput.style.border = "1px solid var(--color-error)";
    valido = false;
  } else {
    valido = true;
    idInput.style.border = "1px solid var(--color-medio)";
  }

  errorID.textContent = msgID;

  return valido;
}

function validarProducto() {
  const productoInput = document.getElementById("producto");
  const errorProducto = document.querySelector(".forma__error--productoNombre");

  let valido;
  let msgProducto;

  if (productoInput.value.trim() == "") {
    msgProducto = "Por favor llenar este campo";
    productoInput.style.border = "1px solid var(--color-error)";
    valido = false;
  } else if (productoInput.value.length > 50) {
    msgProducto = "Este campo tiene un maximo de 50 caracteres";
    productoInput.style.border = "1px solid var(--color-error)";
    valido = false;
  } else {
    productoInput.style.border = "1px solid var(--color-medio)";
    valido = true;
  }

  errorProducto.textContent = msgProducto;
  return valido;
}

function validarCantidad() {
  const cantidadInput = document.getElementById("cantidad");
  const errorCantidad = document.querySelector(
    ".forma__error--productoCantidad"
  );

  let valido;
  let msgCantidad;

  if (cantidadInput.value.trim() == "") {
    msgCantidad = "Por favor llenar este campo";
    cantidadInput.style.border = "1px solid var(--color-error)";
    valido = false;
  } else if (!Number.isInteger(Number(cantidadInput.value))) {
    msgCantidad = "Ingrese una cantidad valida";
    cantidadInput.style.border = "1px solid var(--color-error)";
    valido = false;
  } else {
    cantidadInput.style.border = "1px solid var(--color-medio)";
    valido = true;
  }

  errorCantidad.textContent = msgCantidad;
  return valido;
}

function validarImagen() {
  const imagenInput = document.getElementById("imagen");
  const errorImagen = document.querySelector(".forma__error--productoImagen");

  let valido;
  let msgImagen;

  if (imagenInput.files.length == 0) {
    msgImagen = "Por favor seleccionar un archivo";
    valido = false;
  } else {
    valido = true;
  }

  errorImagen.textContent = msgImagen;

  return valido;
}
