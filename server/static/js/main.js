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
});
