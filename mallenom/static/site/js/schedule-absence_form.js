$(document).ready(
    function() {
        var current_language = $("select[name='language']").val()
        var start_date = $("#id_start")
        var end_date = $("#id_end")

        // Disable form fields autocomplete
        start_date.attr('autocomplete', 'off');
        end_date.attr('autocomplete', 'off');

        // Add datepicker to form date fields
        start_date.datepicker($.extend(
                $.datepicker.regional[current_language]
            ));
        end_date.datepicker($.extend(
            $.datepicker.regional[current_language]
        ));

        // Add search option to form selects
        $("#id_employee").select2({language: current_language})
    }
);
