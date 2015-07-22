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

            $.ajax({
                url: "/contact_me/",
                type: 'POST',
                data: $('#contactForm').serialize(),
                success: function(data, textStatus) {
                    showMessage(data);
                    var recaptchaObj = grecaptcha || recaptcha || Recaptcha;
                    if (recaptchaObj) {
                        recaptchaObj.reset();
                    }
                    $("#contactBtn").attr("disabled", false);
                    $('#contactForm').trigger("reset");
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

    function showMessage(data) {
        if (data.recaptcha) {
            $('.notify-alert.failure span#form-message').text('Неверно заполнено проверочное поле');
            $('.notify-alert.failure').show();
        } else {
            $('.notify-alert.success span#form-message').text(data.message);
            $('.notify-alert.success').show();
        }
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