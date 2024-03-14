let product = {
    list: function () {
        // Cargar los 10 primeros registros de nuestro producto
        $.ajax({
            headers: {'X-CSRFToken': csrfToken},
            url: pathanme,
            type: 'POST',
            dataType: 'json',
            data: {
                action: 'get_products',
            },
            success: function (response) {
                if (!response.hasOwnProperty('error')) {
                    $.each(response.products, function (key, value) {
                        $('#product-container').append('' +
                            '           <div class="col-sm-6 col-lg-3 mb-3">' +
                            '                <div class="card  h-100">' +
                            '                    <img src="' + value['imagen'] + '" class="card-img-custom" alt="...">' +
                            '                    <div class="card-body">' +
                            '                        <h5 class="card-title">' + value['names'] + '</h5>' +
                            '                        <p class="card-text">' +
                            '                            Unidades Disponibles : ' + value['stock'] + ' <br>' +
                            '                            Precio : S/ ' + value['pvp'] + '' +
                            '                        </p>' +
                            '                    </div>' +
                            '                    <div class="card-footer">' +
                            '                        <div class="d-flex justify-content-center">' +
                            '                            <button type="button" title="Agregar al carrito" data-id="' + value['id'] + '" class="btn btn-primary text-center" id="btnAddCart">' +
                            '                                <i class="fas fa-plus"></i> Añadir Carrito' +
                            '                            </button>' +
                            '                        </div>' +
                            '                    </div>' +
                            '                </div>' +
                            '            </div>' +
                            ''
                        );
                    });
                    $('#pagination').append(`
                    <li class="page-item ${response['previous'] !== null ? '' : 'disabled'}">
                        <a class="page-link"  title="Ir a la pagina ${response['previous'] || '#'}" id="previous" value="${response['previous'] || '#'}">Previous</a>
                    </li>
                    <li class="page-item ${response['next'] !== null ? '' : 'disabled'}">
                        <a class="page-link" title="Ir a la pagina ${response['next']}" id="next" value="${response['next'] || '#'}">Next</a>
                    </li>
                `);

                    return false;
                }
            },
            error: function (xhr, errorType, errorMesssage) {
                get_errors(errorType + ' ' + errorMesssage);
            }
        });
    }
}

$(function () {
    product.list();

    $('#product-container').on('click', '#btnAddCart', function () {
        let data_id = $(this).attr('data-id');
        $.ajax({
            headers: {'X-CSRFToken': csrfToken},
            url: pathanme,
            type: 'POST',
            dataType: 'json',
            data: {
                action: 'add_cart',
                product_id: data_id,
            }
        });
    });
});