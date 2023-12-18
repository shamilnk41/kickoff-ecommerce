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


// ================================================================================================================================

// $(document).ready(function(){
//     $('.payWithRazorpay').click(function (e){
//         e.preventDefault();
//         var fname = $("[name='fname']").val();
//         var lname = $("[name='lname']").val();
//         var country = $("[name='country']").val();
//         var address = $("[name='address']").val();
//         var city = $("[name='city']").val();
//         var state = $("[name='state']").val();
//         var pincode = $("[name='pincode']").val();
//         var phone = $("[name='phone']").val();
//         var email = $("[name='email']").val();
//         var total_price = $("[name='total_price']").val();
//         var token = $("[name='csrfmiddlewaretoken']").val();

//         if (fname == "" || lname =="" || country =="" || address =="" || city == "" || state == "" || pincode == "" || phone == "" || email == "")
//         {   
//             alert("all fields are mandatory") 
//             return false;
//         } else {
//             var options = {
//                 key: "rzp_test_W8KgTDkjH3fB0r",
//                 amount: total_price * 100,
//                 currency: "INR",
//                 name: "Kickoff",
//                 description: "Thank you for buying from us",
//                 image: "/user/images/icons/logo.png",
//                 handler: function (response) {
//                     alert(response.razorpay_payment_id);

//                     // Add hidden input fields with Razorpay response data
//                     $("<input>").attr({
//                         type: "hidden",
//                         name: "payment_mode",
//                         value: "paid by razorpay"
//                     }).appendTo("#razorpay-form");

//                     $("<input>").attr({
//                         type: "hidden",
//                         name: "payment_id",
//                         value: response.razorpay_payment_id
//                     }).appendTo("#razorpay-form");

//                     // Submit the form
//                     $("#razorpay-form").submit();
//                 },
//                 prefill: {
//                     name: fname + " " + lname,
//                     email: email,
//                     contact: phone
//                 },
//                 theme: {
//                     color: "#c96",
//                 },
//             };

//             var rzp1 = new Razorpay(options);
//             rzp1.open();
//         }
//     });
// });

// ================================================================================================================================
// $(document).ready(function(){
//     $('.payWithRazorpay').click(function (e){
//         e.preventDefault();
//         var fname = $("[name='fname']").val();
//         var lname = $("[name='lname']").val();
//         var country = $("[name='country']").val();
//         var address = $("[name='address']").val();
//         var city = $("[name='city']").val();
//         var state = $("[name='state']").val();
//         var pincode = $("[name='pincode']").val();
//         var phone = $("[name='phone']").val();
//         var email = $("[name='email']").val();
//         var total_price = $("[name='total_price']").val();
//         var token = $("[name='csrfmiddlewaretoken']").val();

//         if (fname == "" || lname =="" || country =="" || address =="" || city == "" || state == "" || pincode == "" || phone == "" || email == "")
//         {   
//             alert("all fields are mandatory") 
//             return false;
//         }else 
//         {
//             var options = {
//                 key: "rzp_test_W8KgTDkjH3fB0r", // Enter the Key ID generated from the Dashboard
//                 amount: total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
//                 currency: "INR",
//                 name: "Kickoff", //your business name
//                 description: "Thank you for buying from us",
//                 image: "/user/images/icons/logo.png",
//                 // order_id: order.id, //This is a sample Order ID. Pass the id obtained in the response of Step 1
//                 "handler": function (response) {
//                     alert(response.razorpay_payment_id);
//                     data = {
//                         "fname": fname,
//                         "lname": lname,
//                         "email": email,
//                         "phone": phone,
//                         "address": address,
//                         "city": city,
//                         "state": state,
//                         "country": country,
//                         "pincode": pincode,
//                         "payment_mode": "paid by razorpay",
//                         "payment_id": response.razorpay_payment_id,
//                         // csrfmiddlewaretoken: token
//                         csrfmiddlewaretoken: token
//                     }
//                     $.ajax({
//                         methode: "POST",
//                         url: "/place_order",
//                         data: data,
//                         success: function(responsec){
//                             alert(responsec.status)
//                         }
//                     })
//                 },
//                 prefill: {
//                   //We recommend using the prefill parameter to auto-fill customer's contact information especially their phone number
//                   name: fname+" "+lname, //your customer's name
//                   email: email,
//                   contact: phone, //Provide the customer's phone number for better conversion rates
//                 },
//                 // notes: {
//                 //   address: "Razorpay Corporate Office",
//                 // },
//                 theme: {
//                   color: "#c96",
//              },
//         };
//             var rzp1 = new Razorpay(options) ;
//             rzp1.open();
//         }

        
//     })
// })

// $(document).ready(function () {
//     $('.payWithRazorpay').click(function (e) {
//         e.preventDefault();

//         // Collect form data
//         var formData = {
//             fname: $("[name='fname']").val(),
//             lname: $("[name='lname']").val(),
//             country: $("[name='country']").val(),
//             address: $("[name='address']").val(),
//             city: $("[name='city']").val(),
//             state: $("[name='state']").val(),
//             pincode: $("[name='pincode']").val(),
//             phone: $("[name='phone']").val(),
//             email: $("[name='email']").val()
//         };

//         // Validate form data
//         for (var key in formData) {
//             if (formData[key] === "") {
//                 alert("All fields are mandatory");
//                 return false;
//             }
//         }

//         // Make AJAX request to get cart total price
//         $.ajax({
//             url: '/proceed-to-pay/',  // Updated URL to match your Django view URL
//             method: 'GET',
//             success: function (data) {
//                 console.log('Cart Total Price:', data.total_price);
//                 // Now you can proceed to open the Razorpay Checkout form or perform other actions
//             },
//             error: function (xhr, textStatus, errorThrown) {
//                 console.error('Error fetching cart total price:', textStatus, errorThrown);
//                 console.log('XHR object:', xhr);
//             }
//         });
//     });
// });

// $(document).ready(function () {
//     $('.payWithRazorpay').click(function (e) {
//         e.preventDefault();

//         // Collect form data
//         var formData = {
//             fname: $("[name='fname']").val(),
//             lname: $("[name='lname']").val(),
//             country: $("[name='country']").val(),
//             address: $("[name='address']").val(),
//             city: $("[name='city']").val(),
//             state: $("[name='state']").val(),
//             pincode: $("[name='pincode']").val(),
//             phone: $("[name='phone']").val(),
//             email: $("[name='email']").val()
//         };

//         // Validate form data
//         for (var key in formData) {
//             if (formData[key] === "") {
//                 alert("All fields are mandatory");
//                 return false;
//             }
//         }

//         // Define the URL without using Django template tags
//         // var razorpayCheckURL = "/proceed-to-pay/";  // Update this URL based on your actual URL

//         // Make an AJAX request
//         // $.ajax({
//         //     method: "GET",
//         //     url: razorpayCheckURL,
//         //     data: formData,
//         //     success: function(response) {
//         //         console.log(response);
//         //         // Now you can use the response to proceed with Razorpay payment
//         //     },
//         //     error: function(error) {
//         //         console.error('Error:', error);
//         //     }
//         // });
//     });
// });


// $(document).ready(function () {
//     $('.payWithRazorpay').click(function (e) {
//         e.preventDefault();

//         // Collect form data
//         var formData = {
//             fname: $("[name='fname']").val(),
//             lname: $("[name='lname']").val(),
//             country: $("[name='country']").val(),
//             address: $("[name='address']").val(),
//             city: $("[name='city']").val(),
//             state: $("[name='state']").val(),
//             pincode: $("[name='pincode']").val(),
//             phone: $("[name='phone']").val(),
//             email: $("[name='email']").val()
//         };

//         // Validate form data
//         for (var key in formData) {
//             if (formData[key] === "") {
//                 alert("All fields are mandatory");
//                 return false;
//             }
//         }

//         // Make an AJAX request
//         $.ajax({
//             method: "GET",
//             url: "{% url 'razorpaycheck' %}",  // Update the URL if needed
//             data: formData,  // Pass form data to the server
//             success: function(response) {
//                 console.log(response);
//                 // Now you can use the response to proceed with Razorpay payment
//             },
//             error: function(error) {
//                 console.error('Error:', error);
//             }
//         });
//     });
// });

// $(document).ready(function () {
//     $('.payWithRazorpay').click(function (e) {
//         e.preventDefault();

//         // Collect form data
//         var formData = {
//             fname: $("[name='fname']").val(),
//             lname: $("[name='lname']").val(),
//             country: $("[name='country']").val(),
//             address: $("[name='address']").val(),
//             city: $("[name='city']").val(),
//             state: $("[name='state']").val(),
//             pincode: $("[name='pincode']").val(),
//             phone: $("[name='phone']").val(),
//             email: $("[name='email']").val()
//         };

//         // Validate form data
//         for (var key in formData) {
//             if (formData[key] === "") {
//                 alert("All fields are mandatory");
//                 return false;
//             }
//         }
//         $.ajax({
//             url: '/proceed-to-pay/',  // Replace with the actual URL for your razorpaycheck view
//             type: 'GET',
//             dataType: 'json',
//             success: function (data) {
//                 // Access the total price from the response
//                 var cartTotal = data.total_price;
//                 console.log('Cart Total:', cartTotal);

//                 // Rest of your Razorpay code...
//             },
//             error: function (error) {
//                 console.error('Error fetching total price:', error);
//             }
//         });
            
            
        // Prepare Razorpay options
        // var options = {
        //     key: "YOUR_RAZORPAY_API_KEY", // Replace with your actual API key
        //     amount: 50000, // Replace with the actual amount in paise
        //     currency: "INR",
        //     name: "FurniCube Pvt.Ltd",
        //     description: "Test Transaction",
        //     image: "/user/images/icons/logo.png",
        //     order_id: "your_order_id", // Replace with the actual order ID
        //     handler: function (response) {
        //         // Handle the response from Razorpay
        //         verifyPayment(response); // You need to implement this function
        //     },
        //     prefill: {
        //         name: "FurniCube Pvt.Ltd",
        //         email: "furnicube007store@example.com",
        //         contact: "910000000369"
        //     },
        //     notes: {
        //         address: "Razorpay Corporate Office"
        //     },
        //     theme: {
        //         color: "#c96"
        //     }
        // };

        // // Open the Razorpay Checkout form
        // var rzp = new Razorpay(options);
        // rzp.open();
//     });
// });


// ==================================
// $.ajax({
            //     method: "GET",
            //     url: "proceed-to-pay",
            //     // data: "data",
            //     // dataType: "dataType",
            //     success: function(response) {
            //         console.log(response);
            //     }
            // });
            // $.ajax({
            //     method: "GET",
            //     url: "{% url 'proceed-to-pay' %}",  // Make sure this matches the URL in your Django urls.py
            //     success: function(response) {
            //         console.log(response);
            //     },
            //     error: function(error) {
            //         console.error('Error:', error);
            //     }
            // });