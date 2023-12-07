const URL = "http://127.0.0.1:5000/"

document.addEventListener('DOMContentLoaded', function () {
    var nombre = document.getElementById("nombre")
    var descripcion = document.getElementById("descripcion")
    var categoria = document.getElementById("categoria")
    var cantidad = document.getElementById("cantidad")
    var precio = document.getElementById("precio")

    function agregarProducto(e){
        e.preventDefault();   

        let nombreValor = nombre.value;
        let descripcionValor = descripcion.value;
        let categoriaValor = categoria.value;
        let cantidadValor = cantidad.value;
        let precioValor = precio.value;

        var formData = new FormData();
        formData.append('nombre', nombreValor);
        formData.append('descripcion', descripcionValor);
        formData.append('categoria', categoriaValor);
        formData.append('cantidad', cantidadValor);
        formData.append('precio', precioValor);

        fetch(URL + 'productos', {
            method: 'POST',
            body: formData // Aquí enviamos formData en lugar de JSON
        })
        .then(function (response) {
            if (response.ok) { return response.json(); }
        })
        .then(function (data) {
            alert('Producto agregado correctamente.');
            // Limpiar el formulario para el proximo producto
            limpiarCampos()
        })
        .catch(function (error) {
            // Mostramos el error, y no limpiamos el form.
            alert('Error al agregar el producto.' + error);
        });
    }

    function limpiarCampos(){
        nombre.value = '';
        descripcion.value = '';
        categoria.value = '';
        cantidad.value = '';
        precio.value = ''; 
    }

    let btnEnviar = document.getElementById("btnEnviar");
    btnEnviar.addEventListener("click", agregarProducto);

    let btnCancelar = document.getElementById("btnCancelar");
    btnCancelar.addEventListener("click", limpiarCampos)

});