function alert_success(msg) {
    var respuesta = msg
    Swal.fire({
        icon: 'success',
        title: respuesta,
        showConfirmButton: false,
        timer: 1500
    })
}

function alert_warning(msg) {
    var respuesta = msg
    Swal.fire({
        icon: 'warning',
        title: respuesta,
        showConfirmButton: false,
        timer: 800
    })
}

function alert_info(msg) {
    var respuesta = msg
    Swal.fire({
        icon: 'info',
        title: respuesta,
        showConfirmButton: false,
        timer: 800
    })
}

function alert_question(id) {
    Swal.fire({
        title: '¿Estas seguro?',
        text: "¡Tu no puedes revertir esto!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, Eliminalo!'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "/eliminar/"+id;
        }
    })
}