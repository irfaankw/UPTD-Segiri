from django.shortcuts import render

def market_unit(request):
    context = {
        'title' : 'Unit Pasar',
    }
    return render(request, 'market/market_unit.html', context)