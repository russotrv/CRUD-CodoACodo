const url = "http://127.0.0.1:5000/"

fetch(url + "productos")
    .then(function (response) {
        if (response.ok) {return response.json(); }
    })
    .then(function (data) {
        let tablaProductos = document.querySelector('.tabla-productos');

        // Iteramos sobre los productos y agregamos filas a la tabla
        for (let producto of data) {
            let fila = document.createElement('tr');
            fila.innerHTML = '<td>' + producto.codigo + '</td>' +
                '<td>' + producto.nombre + '</td>' +
                '<td>' + producto.descripcion + '</td>' +
                '<td align="right">' + producto.cantidad + '</td>' +
                '<td align="right">' + producto.precio + '</td>' 
                // Mostrar miniatura de la imagen
                
            tablaProductos.appendChild(fila);
        }
    })
    .catch(function (error) {
        // Código para manejar errores
        alert('Error al obtener los productos.');
});