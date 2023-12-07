const URL = "http://127.0.0.1:5000/";

document.getElementById('boton-consulta').addEventListener('click', function (event) {
    event.preventDefault();
    var tablaProductosBody= document.getElementById("tablaProductosBody");
    let categoria = document.getElementById("categoria").value;
    let cantidad = document.getElementById("cantidad").value;

    fetch(URL + 'productos/')
        .then(function (response) {
            if (response.ok) {return response.json(); }
        })
        .then(function(data) {
            // Redirige a la página de visualización con los resultados
            for(let producto of data){
                //if(producto.categoria == categoria){    
                    let fila = document.createElement("tr");
                    fila.innerHTML =  
                        '<td align="center">' + producto.codigo + '</td>' +
                        '<td align="center">' + producto.nombre + '</td>' +
                        '<td align="center">' + producto.descripcion + '</td>' +
                        '<td align="center">' + producto.cantidad + '</td>' +
                        '<td align="center">' + producto.precio + '</td>'  ;
                    tablaProductosBody.appendChild(fila);
              //}
            }
        })
        .catch(error => console.error('Error:', error));
});
