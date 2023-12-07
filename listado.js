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
            fila.innerHTML = '<td align="center">' + producto.codigo + '</td>' +
                '<td align="center">' + producto.nombre + '</td>' +
                '<td align="center">' + producto.descripcion + '</td>' +
                '<td align="center">' + producto.categoria + '</td>' +
                '<td align="center">' + producto.cantidad + '</td>' +
                '<td align="center">' + producto.precio + '</td>' 
                
                
            tablaProductos.appendChild(fila);
        }
    })
    .catch(function (error) {
        // Código para manejar errores
        alert('Error al obtener los productos.');
});