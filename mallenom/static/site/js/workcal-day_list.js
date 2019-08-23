$(document).ready(
    function() {
        var current_language = $("select[name='language']").val()
        var date_after = $("#id_date__gte")
        var date_before = $("#id_date__lte")
        var day_type = $("#id_day_type")

        // Disable form fields autocomplete
        date_after.attr('autocomplete', 'off');
        date_before.attr('autocomplete', 'off');

        // Add datepicker to form date fields
        date_after.datepicker($.extend(
                $.datepicker.regional[current_language]
            ));
        date_before.datepicker($.extend(
            $.datepicker.regional[current_language]
        ));

        // Add search option to form selects
        day_type.select2({
            minimumResultsForSearch: Infinity,
            width: '150pt',
        })

        // Auto submit form when fields changed
        date_after.change(function() {
            $(this).parents("form").submit();
        });
        date_before.change(function() {
            $(this).parents("form").submit();
        });
        day_type.change(function() {
            $(this).parents("form").submit();
        });
    }
);
