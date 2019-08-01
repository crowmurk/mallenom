$(document).ready(
    function() {
        var current_language = $("select[name='language']").val()

        // Disable form fields autocomplete
        $("#id_number").attr('autocomplete', 'off');

        // Add search option to form selects
        $("#id_employee").select2({language: current_language});
        $("#id_staffing").select2({language: current_language});
    }
);
