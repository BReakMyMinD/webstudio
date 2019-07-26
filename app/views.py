from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError, HttpResponseBadRequest
from .models import About, Offer, Order, Message
from .forms import RegisterForm, OrderForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
import json


def index(request):
    info = About.objects.first()
    offers = Offer.objects.all()
    context = {
        'description': info.short_description,
        'offers': offers
    }
    return render(request, 'index.html', context)


def about(request):
    info = About.objects.first()
    context = {
        'short_description': info.short_description,
        'full_description': info.full_description
    }
    return render(request, 'about.html', context)


def offer(request, offer_id):
    offer_obj = get_object_or_404(Offer, link=offer_id)
    context = {
        'offer_info': offer_obj
    }
    return render(request, 'offer.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/login/')

    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def placeorder(request, offer_id):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create_order(offer_id, form.get_info(), request.user)
            order.save()
            return HttpResponseRedirect('/order/' + str(order.id))
    else:
        form = OrderForm()

    return render(request, 'order_confirm.html', {'form': form})


@login_required
def order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not order.client == request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    else:
        context = {
            'order': order,
            'messages': order.messages.order_by('date')
        }
        return render(request, 'order.html', context)


@login_required
def message(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not order.client == request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.is_ajax():
        if request.method == 'GET':
            data = serializers.serialize('json', order.messages.filter()[:5])
            return JsonResponse(data, safe=False)
        else:
            data = json.loads(request.body)
            try:
                text = data['text']
            except KeyError:
                return HttpResponseServerError('Wrong data')
            msg = Message.objects.create(text=text, is_client=not request.user.is_staff)
            order.messages.add(msg)
            data = serializers.serialize('json', msg)
            return JsonResponse(data, safe=False)
    else:
        return HttpResponseBadRequest()


