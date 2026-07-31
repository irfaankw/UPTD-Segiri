from django.shortcuts import render

def membership(request):
    context = {
        'title' : 'Keanggotaan',
    }
    return render(request, 'membership/membership.html', context)