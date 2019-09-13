$(document).ready(
    function() {
        var current_language = $("select[name='language']").val()
        var starts_after = $("#id_start__gte")
        var ends_before = $("#id_end__lte")
        var projects = $('#id_projects')

        // Disable form fields autocomplete
        $('#id_employee').attr('autocomplete', 'off');
        projects.attr('autocomplete', 'off');
        starts_after.attr('autocomplete', 'off');
        ends_before.attr('autocomplete', 'off');
        $("#id_year_month").attr('autocomplete', 'off');

        // Add search option to form selects
        projects.select2({
            language: current_language,
            width: 'resolve'
        })

        // Add datepicker to form date fields
        starts_after.datepicker($.extend(
                $.datepicker.regional[current_language]
            ));
        ends_before.datepicker($.extend(
            $.datepicker.regional[current_language]
        ));

        // Auto submit form when fields changed
        projects.change(function() {
            $(this).parents("form").submit();
        });
        starts_after.change(function() {
            $(this).parents("form").submit();
        });
        ends_before.change(function() {
            $(this).parents("form").submit();
        });
    }
);
