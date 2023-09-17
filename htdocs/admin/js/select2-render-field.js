const defaultProcessSearch = (params) => {
    return {
        search: params.term,
        page: params.page,
        limit: DEFAULT_PAGE_SIZE,
        offset: DEFAULT_PAGE_SIZE * params.page || 0,
        format: 'json'
    };
};

const defaultProcessResult = (data, params) => {
    params.page = params.page || 1;
    return {
        pagination: {
            more: Boolean(data.next)
        },
        results: $.map(data.results, function (obj) {
            return {
                id: obj.id,
                text: `${obj.label}`
            };
        })
    }
};

function select2RenderField($field,
                            processSearch = null, processResult = null,
                            ajax_settings = {}, select2_settings = {}) {
    const defaultAjaxSettings = {
        url: $field.data('ajax-url'),
        method: 'GET',
        dataType: 'json',
        delay: 250,
        data: function (params) {
            let funcToCall = processSearch || defaultProcessSearch;
            return funcToCall(params);
        },
        processResults: function (data, params) {
            let funcToCall = processResult || defaultProcessResult;
            return funcToCall(data, params);
        }
    };
    let settings = {
        allowClear: true,
        placeholder: $field.attr('placeholder') || $field.attr('label') || "Select from list",
        width: '100%',
        ajax: {
            ...defaultAjaxSettings,
            ...ajax_settings,
        },
        ...select2_settings
    }
    console.log(settings)
    $field.select2(settings);
}