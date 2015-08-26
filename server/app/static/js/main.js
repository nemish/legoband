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
        var staffDesctiptionsHeights = [];
        $('.staff-description').each(function (index, element) {
            staffDesctiptionsHeights.push($(element).height());
        });
        $('.staff-description').height(_.max(staffDesctiptionsHeights));
    });

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a').click(function() {
        $('.navbar-toggle:visible').click();
    });

});