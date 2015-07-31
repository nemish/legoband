$(function() {

    $("input,textarea").jqBootstrapValidation({
        preventSubmit: true,
        submitError: function($form, event, errors) {
            // additional error messages or events
        },
        submitSuccess: function($form, event) {
            // Prevent spam click and default submit behaviour
            $("#contactBtn").attr("disabled", true);
            event.preventDefault();
            hideMessage();

            $.ajax({
                url: "/contact_me/",
                type: 'POST',
                data: $('#contactForm').serialize(),
                success: function(data, textStatus) {
                    var recaptchaObj = grecaptcha || recaptcha || Recaptcha;
                    if (recaptchaObj) {
                        recaptchaObj.reset();
                    }
                    if (data.recaptcha) {
                        showMessage(data.status, 'Неверно заполнено проверочное поле.');
                    } else {
                        showMessage(data.status, data.message);
                        $('#contactForm').trigger("reset");
                    }

                    $("#contactBtn").attr("disabled", false);
                }
            });
        },
        filter: function() {
            return $(this).is(":visible");
        }
    });

    $("a[data-toggle=\"tab\"]").click(function(e) {
        e.preventDefault();
        $(this).tab("show");
    });

    function showMessage(status, message) {
        var selectorTpl = _.template('.notify-alert.<%= status %>');
        var selector = selectorTpl({status: status});
        $(selector + ' span#form-message').text(message);
        $(selector).show();
    }

    function hideMessage() {
        $('.notify-alert').hide();
    }

    $('.notify-alert').click(function (event) {
        $(event.currentTarget).hide();
    });
});

// When clicking on Full hide fail/success boxes
$('#name').focus(function() {
    $('#success').html('');
});

// Floating label headings for the contact form
$(function() {
    $("body").on("input propertychange", ".floating-label-form-group", function(e) {
        $(this).toggleClass("floating-label-form-group-with-value", !! $(e.target).val());
    }).on("focus", ".floating-label-form-group", function() {
        $(this).addClass("floating-label-form-group-with-focus");
    }).on("blur", ".floating-label-form-group", function() {
        $(this).removeClass("floating-label-form-group-with-focus");
    });
});