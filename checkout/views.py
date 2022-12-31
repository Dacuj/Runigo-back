from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from .models import *
from django.views.generic import ListView, CreateView, DetailView, TemplateView
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from web.models import Mentors
from rest_framework.views import APIView
from django.shortcuts import redirect

# Create your views here.


class ProductListView(ListView):
    model = Mentors
    template_name = "checkout/product_list.html"
    context_object_name = 'product_list'


class ProductDetailView(DetailView):
    model = Mentors
    template_name = "checkout/product_detail.html"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context  

@csrf_exempt
def create_checkout_session(request, id):
    request_data = json.loads(request.body)
    gig = get_object_or_404(Mentors, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    order = OrderDetail()
    checkout_session = stripe.checkout.Session.create(
        customer_email=request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': gig.mentor,
                    },
                    'unit_amount': int(gig.price * 100),
                },
                'quantity': 1,
            }
        ],

        mode='payment',
        success_url='http://127.0.0.1:8000/checkout/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/checkout/failed/',
        metadata={'order_id': order.uuid}
    )


    order.customer_email = request_data['email']
    order.gig = gig
    order.amount = int(gig.price * 100)
    order.save()
    
    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "checkout/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponse("failed")
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        
        order = get_object_or_404(OrderDetail, uuid=session.metadata.order_id)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)


class PaymentFailedView(TemplateView):
    template_name = "checkout/payment_failed.html"


class OrderHistoryListView(ListView):
    model = OrderDetail
    template_name = "checkout/order_history.html"


# questo è il mio tentativo di inserirlo

# class CreateCheckoutSession(APIView):
#   def post(self, request):
#     dataDict = dict(request.data)
#     price = dataDict['price'][0]
#     product_name = dataDict['product_name'][0]
#     try:
#       checkout_session = stripe.checkout.Session.create(
#         line_items =[{
#         'price_data' :{
#           'currency' : 'usd',  
#             'product_data': {
#               'name': product_name,
#             },
#           'unit_amount': price
#         },
#         'quantity' : 1
#       }],
#         mode= 'payment',
#         success_url= 'localhost:3000/app/checkout/success',
#         cancel_url= 'localhost:3000/app/checkout/failed',
#         )
#       return redirect(checkout_session.url , code=303)
#     except Exception as e:
#         print(e)
#         return e

# class WebHook(APIView):
#   def post(self , request):
#     event = None
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']

#     try:
#       event = stripe.Webhook.construct_event(
#         payload ,sig_header , webhook_secret
#         )
#     except ValueError as err:
#         # Invalid payload
#         raise err
#     except stripe.error.SignatureVerificationError as err:
#         # Invalid signature
#         raise err

#     # Handle the event
#     if event.type == 'payment_intent.succeeded':
#       payment_intent = event.data.object 
#       print("--------payment_intent ---------->" , payment_intent)
#     elif event.type == 'payment_method.attached':
#       payment_method = event.data.object 
#       print("--------payment_method ---------->" , payment_method)
#     # ... handle other event types
#     else:
#       print('Unhandled event type {}'.format(event.type))

#     return JsonResponse(success=True, safe=False)


class CreateCheckoutSession(APIView):
  def post(self, request):
    dataDict = dict(request.data)
    gig = get_object_or_404(Mentors, pk=dataDict["mentorId"])
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # order = OrderDetail()
    try:
      checkout_session = stripe.checkout.Session.create(
        customer_email="prova@gmail.com",
        payment_method_types=['card'],
        line_items =[{
        'price_data' :{
          'currency' : 'usd',  
            'product_data': {
              'name': gig.mentor,
            },
          'unit_amount': int(gig.price * 100),
        },
        'quantity' : 1
      }],
        mode= 'payment',
        success_url= 'localhost:3000/app/checkout/success',
        cancel_url= 'localhost:3000/app/checkout/failed',
        )
      return redirect(checkout_session.url , code=303)
    except Exception as e:
        print(e)
        return e