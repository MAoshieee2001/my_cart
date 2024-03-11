let product = {
    list: function () {
        $('#data').DataTable({
            serverSide: true,
            processing: true,
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                headers: {'X-CSRFToken': csrfToken},
                data: {
                    action: 'get_products',
                }, // parametros
                dataSrc: "data",

            },
            columns: [
                {"data": "position"},
                {"data": "imagen"},
                {"data": "category.names"},
                {"data": "names"},
                {"data": "description"},
                {"data": "stock"},
                {"data": "pvp"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img class="img-fluid" style="width: 50px; height: 50px;" src="' + data + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a class="btn btn-warning btn-sm" href="' + pathanme + 'update/' + data + '/"><i class="fas fa-edit"></i></a> ' +
                            '<a class="btn btn-danger btn-sm" href="' + pathanme + 'delete/' + data + '/"><i class="fas fa-trash"></i></a>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'S/ ' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            initComplete: function (settings, json) {
            }
        });
    }
}

$(function () {
    product.list();
});