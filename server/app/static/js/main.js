$(document).ready(function() {
    $('.fancybox-media').fancybox({
        openEffect  : 'none',
        closeEffect : 'none',
        helpers : {
            media : {},
            overlay: {
                locked: false
            }
        }
    });

    $('.smooth-scroll').smoothScroll({
        offset: -50,
        speed: 1000
    });

    imagesLoaded('.staff-single-container', function () {
        alignHeights('.staff-description');
    });

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a').click(function() {
        $('.navbar-toggle:visible').click();
    });
});

function alignHeights (itemsCls) {
    var heights = [];
    $(itemsCls).each(function (index, element) {
        heights.push($(element).height());
    });
    $(itemsCls).height(_.max(heights));
}