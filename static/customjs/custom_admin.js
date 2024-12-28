(function($) {
    $(document).ready(function() {
        $('#id_categories').change(function() {
            var categoryId = $(this).val();
            var subCategoryField = $('#id_subcategories');

            if (categoryId) {
                $.ajax({
                    url: '/super-admin/autocomplete/',
                    data: {
                        app_label: 'products',
                        model_name: 'subcategories',
                        field_name: 'categories',
                        term: categoryId
                    },
                    success: function(data) {
                        subCategoryField.html($(data).find('#id_subcategories option'));
                    }
                });
            } else {
                subCategoryField.html('<option value="">---------</option>');
            }
        });
    });
})(django.jQuery);