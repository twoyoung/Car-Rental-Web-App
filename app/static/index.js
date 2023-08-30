// client-side real-time validation username
$("input[id^='username']").each(function() {
    $(this).on("input", function(event) {
        const input = $(this);
        const value = input.val();
        if (value.length === 0){
            input.removeClass("is-valid").addClass("is-invalid");
            $(".username-invalid-format-feedback").hide();
            $(".username-empty-feedback").show();
        } else{
            const isValid = /^[a-zA-Z0-9]+$/.test(value);
            if (isValid){
                input.removeClass("is-invalid").addClass("is-valid");
                $(".username-valid-feedback").show();  
            }
            else {
                input.removeClass("is-valid").addClass("is-invalid");
                $(".username-empty-feedback").hide();
                $(".username-invalid-format-feedback").show();
            }
        }
    });
});

// client-side real-time validation password
$("input[id^='password']").each(function() {
    $(this).on("input", function(event) {
        const input = $(this);
        const value = input.val();
        if (value.length === 0){
            input.removeClass("is-valid").addClass("is-invalid");
            $(".password-invalid-format-feedback").hide();
            $(".password-empty-feedback").show();
        } else{
            const isValid = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/.test(value);
            if (isValid){
                input.removeClass("is-invalid").addClass("is-valid");
                $(".password-valid-feedback").show();  
            }
            else {
                input.removeClass("is-valid").addClass("is-invalid");
                $(".password-empty-feedback").hide();
                $(".password-invalid-format-feedback").show();
            }
        }
    });
});

// client-side real-time validation email
$("input[id^='email']").each(function() {
    $(this).on("input", function(event) {
        const input = $(this);
        const value = input.val();
        if (value.length === 0){
            input.removeClass("is-valid").addClass("is-invalid");
            $(".email-invalid-format-feedback").hide();
            $(".email-empty-feedback").show();
        } else{
            const isValid = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value);
            if (isValid){
                input.removeClass("is-invalid").addClass("is-valid");
                $(".email-valid-feedback").show();  
            }
            else {
                input.removeClass("is-valid").addClass("is-invalid");
                $(".email-empty-feedback").hide();
                $(".email-invalid-format-feedback").show();
            }
        }
    });
});

// client-side real-time validation car model
$("input[id^='model']").each(function() {
    $(this).on("input", function(event) {
        const input = $(this);
        const value = input.val();
        if (value.length === 0){
            input.removeClass("is-valid").addClass("is-invalid");
            $(".model-empty-feedback").show();
        } else{
            input.removeClass("is-invalid").addClass("is-valid");
            $(".model-valid-feedback").show();  
            }
        });
});

// client-side real-time validation year
$("input[id^='year']").each(function() {
    $(this).on("input", function(event) {
        const input = $(this);
        const value = input.val();
        const isValid = /^(188[6-9]|18[9-9]\d|19\d\d|20[0-1]\d|202[0-3])$/.test(value);
        if (isValid){
            input.removeClass("is-invalid").addClass("is-valid");
            $(".year-valid-feedback").show();
        } else{
            input.removeClass("is-valid").addClass("is-invalid");
            $(".year-invalid-feedback").show();  
            }
        });
});

// client-side real-time validation seatNumber
$("input[id^='seatNumber']").each(function() {
    $(this).on("input", function(event) {
        const input = $(this);
        const value = input.val();
        if (value.length === 0){
            input.removeClass("is-valid").addClass("is-invalid");
            $(".seat-number-format-feedback").hide();
            $(".seat-number-empty-feedback").show();
        } else{
            const isValid = /^(?:[1-9]|[1-4][0-9]|50)$/.test(value);
            if (isValid){
                input.removeClass("is-invalid").addClass("is-valid");
                $(".seat-number-valid-feedback").show();  
            }
            else {
                input.removeClass("is-valid").addClass("is-invalid");
                $(".seat-number-empty-feedback").hide();
                $(".seat-number-format-feedback").show();
            }
        }
    });
});

// client-side real-time validation registration number
$("input[id^='registration']").each(function() {
    $(this).on("input", function(event) {
        const input = $(this);
        const value = input.val();
        if (value.length === 0){
            input.removeClass("is-valid").addClass("is-invalid");
            $(".registration-format-feedback").hide();
            $(".registration-empty-feedback").show();
        } else{
            const isValid = /^[A-Z]{2,3}\d{2,3}$/.test(value);
            if (isValid){
                input.removeClass("is-invalid").addClass("is-valid");
                $(".registration-valid-feedback").show();  
            }
            else {
                input.removeClass("is-valid").addClass("is-invalid");
                $(".registration-empty-feedback").hide();
                $(".registration-format-feedback").show();
            }
        }
    });
});

// client-side real-time validation rental per day 
$("input[id^='rentalPerDay']").each(function() {
    $(this).on("input", function(event) {
        const input = $(this);
        const value = input.val();
        if (value.length === 0){
            input.removeClass("is-valid").addClass("is-invalid");
            $(".rental-per-day-format-feedback").hide();
            $(".rental-per-day-empty-feedback").show();
        } else{
            const isValid = /^\d+(\.\d{1,2})?$/.test(value);
            if (isValid){
                input.removeClass("is-invalid").addClass("is-valid");
                $(".rental-per-day-valid-feedback").show();  
            }
            else {
                input.removeClass("is-valid").addClass("is-invalid");
                $(".rental-per-day-empty-feedback").hide();
                $(".rental-per-day-format-feedback").show();
            }
        }
    });
});

// client-side real-time validation customer ID
$("input[id^='customerId']").each(function() {
    $(this).on("input", function(event) {
        const input = $(this);
        const value = input.val();
        if (value.length === 0){
            input.removeClass("is-invalid");
            $(".custome-id-format-feedback").hide();
            $(".customer-id-empty-feedback").hide();
        } else{
            const isValid = /^(?:[1-9]\d*|)$/.test(value);
            if (isValid){
                input.removeClass("is-invalid").addClass("is-valid");
                $(".customer-id-valid-feedback").show();  
            }
            else {
                input.removeClass("is-valid").removeClass("is-invalid");
                $(".customer-id-empty-feedback").hide();
                $(".custome-id-format-feedback").show();
            }
        }
    });
});

// client-side real-time validation car image 
$("input[id^='carImage']").each(function() {
    $(this).on("input", function(event) {
        const input = $(this);
        const value = input.val();
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            const fileName = selectedFile.name;
            const fileExtension = fileName.split('.').pop().toLowerCase();
    
            if (['jpg', 'png', 'gif', 'jpeg'].includes(fileExtension)) {
                input.removeClass('is-invalid').addClass('is-valid');
                $(".car-image-valid-feedback").show();  
            } else {
                input.removeClass('is-valid').addClass('is-invalid');
                $(".car-image-invalid-feedback").show();
            }
        } else {
            input.removeClass('is-valid').removeClass('is-invalid');
            $(".car-image-invalid-feedback").hide();
            $(".car-image-valid-feedback").hide();  
        }
    });
});


// <!-- function to keep submit button disabled until all input valid-->
function enableSubmitButtonFunction(form, submitButtonId) {
    const submitButton = $("#"+ submitButtonId).get(0);
    function updateSubmitButtonState() {
        var isValid = true;
        $(form).find("input").each(function(){
            if ($(this).hasClass("is-invalid")){
                isValid = false;
            }
            if ($(this).filter('[required]:visible').val() === ""){
                isValid = false;
            }
        });

        if(isValid){
        $(submitButton).attr("disabled", false);
        $(submitButton).removeClass('btn-disabled').addClass('btn-enabled');
        } else {
        $(submitButton).attr("disabled", true);
        $(submitButton).removeClass('btn-enabled').addClass('btn-disabled');
        }
    }

    $(form).find("input").each(function(){
        $(this).on('input',updateSubmitButtonState);
    });
};

// <!-- Call enableSubmitButtonFunction for Form 'change-password' -->
document.addEventListener('DOMContentLoaded', function() {
    const form = $('#change-password').get(0);
    enableSubmitButtonFunction(form,'submitButton');
});
// <!-- Call enableSubmitButtonFunction for Form group 'add-user' -->
document.addEventListener('DOMContentLoaded', function() {
    const form = $('#add-user').get(0);
    enableSubmitButtonFunction(form,'submitButton');
});

// <!-- Call enableSubmitButtonFunction for Form group 'edit-user' -->
document.addEventListener('DOMContentLoaded', function() {
    $(".edit-user").each(function(){
        const form = this;
        submitButtonId = $(this).find("[id^='submitButton']").attr("id");
        enableSubmitButtonFunction(form,submitButtonId);
    });
});

// <!-- Call enableSubmitButtonFunction for Form group 'edit-profile' -->
document.addEventListener('DOMContentLoaded', function() {
    const form = $('#edit-profile').get(0);
    enableSubmitButtonFunction(form,'submitButton-edit');
});

// <!-- Call enableSubmitButtonFunction for Form 'add-car' -->
document.addEventListener('DOMContentLoaded', function() {
    const form = $('#add-car').get(0);
    enableSubmitButtonFunction(form,'submitButton');
});

// <!-- Call enableSubmitButtonFunction for Form group 'edit-car' -->
document.addEventListener('DOMContentLoaded', function() {
    $(".edit-car").each(function(){
        const form = this;
        submitButtonId = $(this).find("[id^='submitButton']").attr("id");
        enableSubmitButtonFunction(form,submitButtonId);
    });
});



