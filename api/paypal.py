from re import A
from paypalcheckoutsdk.orders import OrdersCreateRequest,OrdersCaptureRequest
from paypalhttp import HttpError
# Construct a request object and set desired parameters
# Here, OrdersCreateRequest() creates a POST request to /v2/checkout/orders
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
import os
from dotenv import load_dotenv
load_dotenv()

# Creating Access Token for Sandbox
client_id = os.getenv("PAYPALCLIENT")
client_secret = os.getenv("PAYPALSECRET")
# Creating an environment
environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
client = PayPalHttpClient(environment)
import json
def create_order(amount):
    request = OrdersCreateRequest()

    request.prefer('return=representation')

    request.request_body (
        {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": amount
                    }
                }
            ]
        }
    )

    try:
        # Call API with your client and get a response for your call
        response = client.execute(request)
        # print ('Order With Complete Payload:')
        # print ('Status Code:', response.status_code)
        # print ('Status:', response.result.status)
        # print ('Order ID:', response.result.id)
        # print ('Intent:', response.result.intent)
        # print ('Links:')
        for link in response.result.links:
            # print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
            # print('Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
            # response.result.purchase_units[0].amount.value))
            # If call returns body in response, you can get the deserialized version from the result attribute of the response
            order = response.result
            return order
    except IOError as ioe:
        print (ioe)
        if isinstance(ioe, HttpError):
            # Something went wrong server-side
            print (ioe.status_code)

def capture_order(order_id):
    # Here, OrdersCaptureRequest() creates a POST request to /v2/checkout/orders
    # Replace APPROVED-ORDER-ID with the actual approved order id.
    request = OrdersCaptureRequest(order_id)

    try:
        # Call API with your client and get a response for your call
        response = client.execute(request)

        # If call returns body in response, you can get the deserialized version from the result attribute of the response        
        return response
    except IOError as ioe:
        if isinstance(ioe, HttpError):
            # Something went wrong server-side
            print (ioe.status_code)
            print (ioe.headers)
            print (ioe)
        else:
            # Something went wrong client side
            print (ioe)