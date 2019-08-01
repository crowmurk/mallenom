$(document).ready(
    function() {
        var current_language = $("select[name='language']").val()

        // Add search option to form selects
        $("#id_department").select2({language: current_language})
        $("#id_position").select2({language: current_language})
    }
);
