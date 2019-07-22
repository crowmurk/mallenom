$(window).on('load', function() {
    // Show page content after loading
    $('.loading-progress').remove();
    $('.main-container').css('visibility', 'visible');
});

$(document).ready(function() {
    // Hide notification messages
    $("ul.messages").delay(3000). animate(
        {height:"toggle", opacity:"toggle"},
        1000
    );
});
