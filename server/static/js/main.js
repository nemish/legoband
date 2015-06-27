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

    $('.fancybox-img').fancybox({
        helpers : {
            title: {
                type: 'float'
            },
            overlay: {
                locked: false
            }
        }
    });

    $('.fancybox-gallery').fancybox({
        openEffect  : 'none',
        closeEffect : 'none',
        helpers : {
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

});