from django.shortcuts import render

# Create your views here.

class HomeView(ListView):
    model = Item
    template_name = "planter/home.html"

class ProductView(DetailView):
    model = Item
    template_name = "planter/shop.html"

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'planters/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'order': order
        }
        return render(self.request, 'tabs/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                
                customer_name = form.cleaned_data.get('customer_name')
                contact_number = form.cleaned_data.get('contact_number')
                shipping_apartment_address = form.cleaned_data.get('shipping_apartment_address')
                shipping_street_address = form.cleaned_data.get('shipping_street_address')
                billing_street_address = form.cleaned_data.get('billing_street_address')
                billing_apartment_address = form.cleaned_data.get('billing_apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionality for these fields
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                shipping_option = form. cleaned_data.get('shipping_option')

                if shipping_option == 'MS':
                    order.delivery_fee = 45
                    shipping = "Mr. Speedy"
                elif shipping_option == 'NV':
                    order.delivery_fee = 45
                    shipping = "Ninja Van"
                elif shipping_option == 'L':
                    order.delivery_fee = 55
                    shipping = "LBC Padala"
                else:
                    messages.warning(self.request, "Invalid shipping option")
                
                if payment_option == 'C':
                    payment = "Card"
                elif payment_option == 'COD':
                    payment = "Cash on Delivery"
                elif payment_option == 'G':
                    payment = "Gcash"

                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    customer_name=customer_name,
                    contact_number=contact_number,
                    shipping_street_address=shipping_street_address,
                    shipping_apartment_address=shipping_apartment_address,
                    billing_street_address=billing_street_address,
                    billing_apartment_address=billing_apartment_address,
                    country=country,
                    zip=zip,
                    shipping_option=shipping,
                    payment_option=payment

                )
                
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()
                print(int(order.get_price_with_delivery()))

                if payment_option == 'C':
                    return redirect('payment', payment_option='card')
                elif payment_option == 'COD':
                    return redirect('payment', payment_option='cash_on_delivery')
                elif payment_option == 'G':
                    return redirect('payment', payment_option='gcash')
                else:
                    messages.warning(self.request, "Invalid Payment option")
                    return redirect('checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("order-summary")

class PaymentView(View):
    def get(self, *args, **kwargs):
        form = PaymentForm() 
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order,
            'form' : form
        }

        payment_option = self.kwargs.get('payment_option')
        if payment_option == 'card':
            #print(order.user)
            #print(order.checkout_address.customer_name)
            return render(self.request, "planters/payment_card.html", context)
        elif payment_option == 'cash_on_delivery':
            return render(self.request, "planters/payment_cod.html", context)
        elif payment_option == 'gcash':
            return render(self.request, "planters/payment_gcash.html", context)
        else:
            messages.warning(self.request, "Invalid Payment option")
            return redirect('payment')

    def post(self, *args, **kwargs):
        form = PaymentForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                
                account_name = form.cleaned_data.get('account_name')
                account_number = form.cleaned_data.get('contact_number')
                payment_checkout = PaymentCheckout(
                    account_name=account_name,
                    account_number=account_number
                )

                payment_checkout.save()
                order.payment_checkout = payment_checkout
                order.save()
                print(int(order.get_price_with_delivery()))

        except ObjectDoesNotExist:
                messages.error(self.request, "Invalid Payment Details")
        return redirect('payment')

def home(request):
    return render(request, "planter/home.html")

def shop(request):
    return render(request, "planter/shop.html")

def account(request):
    return render(request, "planter/account.html")
