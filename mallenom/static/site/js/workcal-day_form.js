$(document).ready(
    function() {
        var current_language = $("select[name='language']").val()
        var date = $("#id_date")

        // Disable form fields autocomplete
        date.attr('autocomplete', 'off');

        // Add datepicker to form date fields
        date.datepicker($.extend(
                $.datepicker.regional[current_language]
            ));

        // Add search option to form selects
        $("#id_day_type").select2({language: current_language})
    }
);
