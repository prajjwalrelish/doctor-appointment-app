from .models import Transactions
from usermgmt.models import User
import razorpay
from livLife.settings import RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import TransactionSerializer
from rest_framework.response import Response
# Create your views here.

client = razorpay.Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET))

class payment(GenericAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def post(self,request):
        try:
            user = request.user #get the user to extract it's uuid and add it in request.data
            userUUID = user.uuid

            amount = request.data['amount'] 
            currency = request.data['currency'] 
            razorpay_amount = int(amount)*100 # 200rs = 20000 for razorpay api
            order_reciept = request.data['order_receipt']
            razorpay_order = client.order.create(dict(currency= currency,
                                                amount=razorpay_amount,
                                                receipt = order_reciept,
                                                payment_capture = '0'))
                                            
            order_id = razorpay_order['id'] #get order id from created order
           
            request.data['from_user'] = userUUID  #add user uuid to the data
            request.data['order_id'] = order_id  #add order id to the data

            order_status = razorpay_order['status']
            
            transaction = Transactions.objects.filter(from_user=userUUID, order_id=order_id)
            if transaction.exists():
                transaction = self.serializer_class(transaction[0])
                return Response(transaction.data, status=status.HTTP_202_ACCEPTED)
                
            if order_status == 'created' :        
                # save the details to Transaction Model 
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            print(e)
            return Response({'error' : 'payment failed'},status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
class paymentHandler(GenericAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Transactions.objects.all()

    def get(self,request):
        try:
       
            # receive dta from GET request
            payment_id = request.data['razorpay_payment_id']
            razorpay_order_id = request.data['razorpay_order_id']
            signature  = request.data['razorpay_signature']
        

            params_dict = {
                'razorpay_payment_id' : payment_id,
                'razorpay_order_id' : razorpay_order_id,
                'razorpay_signature' : signature
            }
            # verify the payment
          
            result = client.utility.verify_payment_signature(params_dict)
          
            if result is None:#If the payment was successful then it would return None, else it would throw an error.
                # amount = 20000  # Rs. 200 
                try :
                        # capture the payemt
                    # client.payment.capture(payment_id, amount)
           
                    # get the object by order id and update payment status and other details
                    transaction = Transactions.objects.get(order_id = razorpay_order_id)
                    transaction.payment_status = 'SUCCESS'
                    transaction.payment_id = payment_id
                    transaction.signature = signature
                    transaction.save()

                    serializer = self.serializer_class(transaction) #convert python data to serialized data
                 
                    # render success page on successful caputre of payment
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                except:
    
                    # if there is an error while capturing payment.
                    return Response({'msg':'payment failed'},status=status.HTTP_400_BAD_REQUEST)
            else :
                # if signature verification fails.
                return  Response({'msg':'payment failed'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            print(e)
            return  Response({'msg':'payment failed'},status=status.HTTP_400_BAD_REQUEST)



    # "context": {
    #     "order_id": "order_IgTENp21xFqRzh",
    #     "api_key_id": "rzp_test_IBOH3OHRmzzGpi",
    #     "amount": "200",
    #     "callback_url": "paymenthandler",
    #     "currency": "INR"
    # }