$(document).ready(
    function() {
        var current_language = $("select[name='language']").val()
        var date_after = $("#id_date__gte")
        var date_before = $("#id_date__lte")

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

        // Auto submit form when fields changed
        date_after.change(function() {
            $(this).parents("form").submit();
        });
        date_before.change(function() {
            $(this).parents("form").submit();
        });
        $("#id_day_type").change(function() {
            $(this).parents("form").submit();
        });
    }
);
