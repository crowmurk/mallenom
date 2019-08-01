$(document).ready(
    function() {
        var current_language = $("select[name='language']").val()

        // Add search option to form selects
        $("#id_project").select2({language: current_language})
        $("#id_assignment").select2({language: current_language})
    }
);
