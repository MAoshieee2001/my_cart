let select_category;

$(function () {
    select_category = $('#id_category');

    select_category.select2({
        placeholder: 'Seleccione la categoria',
        theme: 'bootstrap4',
        language: 'es',
        ajax: {
            headers: {'X-CSRFToken': csrfToken},
            url: pathanme,
            type: 'POST',
            dataType: 'json',
            data: function (params) {
                return {
                    term: params.term, // search term
                    action: 'get_categories',
                };
            },
            processResults: function (data, params) {
                return {
                    results: data,
                };
            },

        }
    });

    select_category.change(function () {
        $.ajax({
            headers: {'X-CSRFToken': csrfToken},
            url: pathanme,
            type: 'POST',
            dataType: 'json',
            data: {
                action: 'get_products_category',
                id_category: $(this).val(),
            },
            beforeSend: function () {
                loading();
            },
            success: function (response) {
                console.log(response);
                if (!response.hasOwnProperty('error')) {
                    $('#rowCard').html('');
                    $.each(response, function (key, value) {
                        $('#rowCard').append('            <div class="col-sm-3 mb-2">\n' +
                            '                <div class="card" style="width: 18rem;">\n' +
                            '                    <img src="' + value['imagen'] + '" loading="lazy" class="card-img-custom">\n' +
                            '                    <div class="card-body">\n' +
                            '                        <h5 class="card-title">' + value['names'] + '</h5>\n' +
                            '                        <p class="card-text">\n' +
                            '                            Unidades :' + value['stock'] + ' <br>\n' +
                            '                            Precio : S/. ' + value['pvp'] + '\n' +
                            '                        </p>\n' +
                            '                        <div class="d-flex justify-content-center">\n' +
                            '                            <a href="#" class="btn btn-primary position-relative"><i class="fas fa-cart-plus"></i> Añadir carrito</a>\n' +
                            '                        </div>\n' +
                            '                    </div>\n' +
                            '                </div>\n' +
                            '            </div>');
                    })
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
    });
});