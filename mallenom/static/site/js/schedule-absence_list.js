$(document).ready(
    function() {
        var current_language = $("select[name='language']").val()
        var starts_after = $("#id_start__gte")
        var ends_before = $("#id_end__lte")

        // Disable form fields autocomplete
        $('#id_employee').attr('autocomplete', 'off');
        starts_after.attr('autocomplete', 'off');
        ends_before.attr('autocomplete', 'off');
        $("#id_year_month").attr('autocomplete', 'off');

        // Add datepicker to form date fields
        starts_after.datepicker($.extend(
                $.datepicker.regional[current_language]
            ));
        ends_before.datepicker($.extend(
            $.datepicker.regional[current_language]
        ));

        // Auto submit form when fields changed
        starts_after.change(function() {
            $(this).parents("form").submit();
        });
        ends_before.change(function() {
            $(this).parents("form").submit();
        });
        $("#id_staff_units").change(function() {
            $(this).parents("form").submit();
        });
    }
);
