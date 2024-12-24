(function($) {
    $(document).ready(function() {
        $('#id_categories').change(function() {
            var categoryId = $(this).val();
            var subCategoryField = $('#id_subcategories');

            if (categoryId) {
                $.ajax({
                    url: window.location.pathname,
                    data: {
                        categories__id__exact: categoryId
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
