from django.shortcuts import render
from .models import company, watch, order

def index(request):
    companies = company.objects.all()
    context = {'companies': companies}
    return render(request, 'watches/index.html', context)

def company_watches(request, company_id):
    comp = company.objects.get(id=company_id)
    watches = watch.objects.filter(company_fk=comp)
    context = {'company': comp, 'watches': watches}
    return render(request, 'watches/company_watches.html', context)

def watch_orders(request, watch_id):
    watch_obj = watch.objects.get(id=watch_id)
    orders = order.objects.filter(watch_fk=watch_obj)
    context = {'watch': watch_obj, 'orders': orders}
    return render(request, 'watches/watch_orders.html', context)
