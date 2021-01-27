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