// Pagina: ADMINISTRACION PRODUCTOS (USUARIO)
// Filtrar productos por nombre en Buscador 

function filtrarProductos() {
  const buscarProducto = document.getElementById("buscarProductoAdmin");
  const texto = buscarProducto.value.toLowerCase();
  const productos = document.getElementsByClassName("nombreAccesorio");

  for (let i = 0; i < productos.length; i++) {
    const producto = productos[i].textContent.toLowerCase();
    if (producto.indexOf(texto) != -1) {

      // console.log(productos[i].textContent);
      productos[i].parentElement.style.display = "block";
    } else {
      productos[i].parentElement.style.display = "none";

    }
  }
}

// Pagina: ADMINISTRACION ACTUALIZAR / ELIMINAR (ADMIN)
// Filtrar productos por nombre en Buscador 

function filtrarInventarioPorID() {
  const buscarProducto = document.getElementById("buscarProductoAdmin");
  const texto = buscarProducto.value;

  const productosID = document.getElementsByClassName("producto__id");

  for (let i = 0; i < productosID.length; i++) {
    const accesorioID = productosID[i].textContent;

    if (accesorioID.indexOf(texto) != -1) {
      productosID[i].parentElement.parentElement.style.display = "block";
    } else {
      productosID[i].parentElement.parentElement.style.display = "none";
    }
    
  }
}

// Pagina: ADMINISTRACION PRODUCTOS (USUARIO)
// Filtrar productos por nombre en Buscador 

function filtrarUsuarios() {
  const buscarProducto = document.getElementById("buscarUsuario");
  const texto = buscarProducto.value.toLowerCase();
  const usuarios = document.getElementsByClassName("usuarioDatos__idUsuario");

  for (let i = 0; i < usuarios.length; i++) {
    const usuario = usuarios[i].textContent.toLowerCase();
    if (usuario.indexOf(texto) != -1) {

      // console.log(productos[i].textContent);
      usuarios[i].parentElement.style.display = "flex";
    } else {
      usuarios[i].parentElement.style.display = "none";

    }
  }
}