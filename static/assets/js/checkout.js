$(document).ready(function () {
    $('.payWithRazorpay').click(function (e) {
        e.preventDefault();

        var addressId = $("input[name='address_id']:checked").val();
        var isExistingAddress = addressId !== undefined;

        var formData = {
            'fname': $("[name='fname']").val(),
            'lname': $("[name='lname']").val(),
            'country': $("[name='country']").val(),
            'address': $("[name='address']").val(),
            'city': $("[name='city']").val(),
            'state': $("[name='state']").val(),
            'pincode': $("[name='pincode']").val(),
            'phone': $("[name='phone']").val(),
            'email': $("[name='email']").val(),
            'total_price': $("[name='total_price']").val(),
            'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val(),
            'payment_mode': 'paid by razorpay',
        };

        // If an existing address is selected, no need to perform validation
        if (!isExistingAddress) {
            if (formData['fname'] == "" || formData['lname'] == "" || formData['country'] == "" || formData['address'] == "" || formData['city'] == "" || formData['state'] == "" || formData['pincode'] == "" || formData['phone'] == "" || formData['email'] == "") {
               
                alert("All fields are mandatory");
                // Swal.fire({
                //     icon: 'error',
                //     title: 'Oops...',
                //     text: 'fields are mandatory!',
                // });
                return false;
            }
            if (!/^[a-zA-Z]+$/.test(formData['fname'])) {
                alert('First name should only contain alphabetic characters.');
                return false;
            }
        }

        var options = {
            key: "rzp_test_W8KgTDkjH3fB0r",
            amount: formData['total_price'] * 100,
            currency: "INR",
            name: "Kickoff",
            description: "Thank you for buying from us",
            image: "/user/images/icons/logo.png",
            handler: function (response) {
                // alert(response.razorpay_payment_id);

                // Add hidden input fields with Razorpay response data
                $("<input>").attr({
                    type: "hidden",
                    name: "payment_mode",
                    value: "paid by razorpay"
                }).appendTo("#razorpay-form");

                $("<input>").attr({
                    type: "hidden",
                    name: "payment_id",
                    value: response.razorpay_payment_id
                }).appendTo("#razorpay-form");

                // Update form data based on the user's choice (existing or new address)
                for (var key in formData) {
                    if (formData.hasOwnProperty(key)) {
                        $("<input>").attr({
                            type: "hidden",
                            name: key,
                            value: formData[key]
                        }).appendTo("#razorpay-form");
                    }
                }

                // Submit the form
                $("#razorpay-form").submit();
            },
            prefill: {
                name: formData['fname'] + " " + formData['lname'],
                email: formData['email'],
                contact: formData['phone']
            },
            theme: {
                color: "#c96",
            },
        };

        var rzp1 = new Razorpay(options);
        rzp1.open();
        
    });
   
});


