function get_sweetAlert2(args) {
    if (!args.hasOwnProperty('icon')) {
        args.icon = 'success';
    }
    if (!args.hasOwnProperty('tittle')) {
        args.title = 'Notificación del sistema!';
    }
    if (!args.hasOwnProperty('html')) {
        args.html = '';
    }
    if (!args.hasOwnProperty('timer')) {
        args.timer = 2000;
    }

    Swal.fire({
        icon: args.icon,
        title: args.title,
        html: args.html,
        timer: args.timer,
        animation: false,
        timerProgressBar: true,
    }).then(function () {
        args.callback();
    });
}

function get_errors(items) {
    let errors = '';

    if (typeof (items) === 'object') {
        errors = '<ul>';
        $.each(items, function (key, value) {
            errors += '<li>' + value + '</li>';
        });
        errors += '</ul>';
    } else {
        errors = items;
    }

    get_sweetAlert2({
        icon: 'error',
        html: errors,
        callback: function () {

        }
    });

}

function loading() {
    $.LoadingOverlay("show", {
        image: "",
        fontawesome: "fa fa-cog fa-spin",
    });
}

function get_dialogConfirm(args) {
    if (!args.hasOwnProperty('title')) {
        args.title = 'Notificación del sistema!';
    }
    if (!args.hasOwnProperty('content')) {
        args.content = '¿Estas seguro que deseas realizar la siguiente acción?';
    }

    $.confirm({
        icon: 'fas fa-info-circle',
        title: args.title,
        content: args.content,
        theme: 'Modern',
        columnClass: 'medium',
        animation: 'bottom',
        closeAnimation: 'zoom',
        draggable: false,
        animationSpeed: 200,
        buttons: {
            confirmar: {
                text: 'Confimar',
                btnClass: 'btn-blue',
                action: function () {
                    args.confirm();
                }
            },
            cancel: {
                text: 'Cancelar',
                btnClass: 'btn-danger',
                action: function () {
                    args.cancel();
                }
            },
        }
    });

}

function set_data_server(args) {

    if (!args.hasOwnProperty('content')) {
        args.content = '¿Estas seguro que deseas realizar la siguiente acción?';
    }

    get_dialogConfirm({
        content: args.content,
        confirm: function () {
            $.ajax({
                headers: {'X-CSRFToken': csrfToken},
                url: pathanme,
                type: 'POST',
                dataType: 'json',
                contentType: false,
                processData: false,
                data: args.params,
                beforeSend: function () {
                    loading();
                },
                success: function (response) {
                    if (!response.hasOwnProperty('error')) {
                        args.success();
                        return false;
                    }
                    get_errors(response.error);
                },
                error: function (xhr, errorType, errorMessage) {
                    get_errors(errorType + ' ' + errorMessage);
                },
                complete: function () {
                    $.LoadingOverlay("hide");
                }
            });
        },
        cancel: function () {

        }
    });
}