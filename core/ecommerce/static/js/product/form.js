$(function () {
    $('#id_category').select2({
        theme: 'bootstrap4',
        language: 'es',
        placeholder: 'Seleccione la categoria.',
        ajax: {
            headers: {'X-CSRFToken': csrfToken},
            url: pathanme,
            type: 'POST',
            dataType: 'json',
            data: function (params) {
                return {
                    term: params.term,
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
});