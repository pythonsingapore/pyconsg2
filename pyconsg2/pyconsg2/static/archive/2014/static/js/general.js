$(document).ready(function() {
    $('.image-field').each(function() {
        link = $(this).parent().find('a');
        image = '<div><img src="/media/' + link.html() + '" style="width:200px;" /></div>';
        link.html(image);
    });
});
