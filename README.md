
## payment api
    1. POST > http://127.0.0.1:8000/api/payment  (with a JWT autheticaton token )

        body={
            "to_doctor": "ee267cf3-0510-4188-a8b0-7907c75d7216",  (doctors uuid)
            "email": "amans197555@gmail.com",
            "contact": "7372958746",
            "currency": "INR",
            "amount": "200",
            "payment_status": "PENDING",
            "payment_method": "razorpay"
        }
        response ={
            "uuid": "05bbdda6-cb49-4ffc-ab32-689fe6797996",
            "from_user": "ee267cf3-0510-4188-a8b0-7907c75d7216",
            "to_doctor": "934b9a2d-3a37-433b-9d83-2735e340ae60",
            "contact": "7372958746",
            "amount": 200.0,
            "currency": "INR",
            "payment_status": "PENDING",
            "payment_method": "razorpay",
            "gateway": null,
            "payment_data": {},
            "payment_id": "",
            "order_id": "order_Ighx5LBOs6Vv5V",
            "signature": "",
            "email": "amans197555@gmail.com",
            "payment_created_at": null
        }

    # details to be send to payment page and use them in razorpay's api
                #   order_id = 'get it from response'      
                #   RAZORPAY_KEY_ID = 'rzp_test_IBOH3OHRmzzGpi
                #   amount = 'get it from response'
                #   callback_url = 'http://127.0.0.1:8000/api/paymenthandler'
                #   currency = 'get it from response'

    # we will get this data from razorpay checkout api , send it to paymenthandler api
        "razorpay_payment_id": "pay_IdhnkVY8kfyBI7",
        "razorpay_order_id": "order_Idhmt8CwhCZ2QW",
        "razorpay_signature": "f9e0d0c0a38fcfdebd2a3313369bf45392e956e3cb99e9c7509484de6b88f947"

    2. Get > http://127.0.0.1:8000/api/paymenthandler  (with a JWT autheticaton token )
        body={
        "razorpay_payment_id": "pay_IdhnkVY8kfyBI7",
        "razorpay_order_id": "order_Idhmt8CwhCZ2QW",
        "razorpay_signature": "f9e0d0c0a38fcfdebd2a3313369bf45392e956e3cb99e9c7509484de6b88f947"
        }
        response= {
            "uuid": "05bbdda6-cb49-4ffc-ab32-689fe6797996",
            "from_user": "ee267cf3-0510-4188-a8b0-7907c75d7216",
            "to_doctor": "934b9a2d-3a37-433b-9d83-2735e340ae60",
            "contact": "7372958746",
            "amount": 200.0,
            "currency": "INR",
            "payment_status": "SUCCESS",
            "payment_method": "razorpay",
            "gateway": null,
            "payment_data": {},
            "payment_id": "pay_IdhnkVY8kfyBI7",
            "order_id": "order_Idhmt8CwhCZ2QW",
            "signature": "f9e0d0c0a38fcfdebd2a3313369bf45392e956e3cb99e9c7509484de6b88f947",
            "email": "amans197555@gmail.com",
            "payment_created_at": null
        }
        