from django.shortcuts import render, redirect
from .models import Address
from .forms import AddressForm

def add_address(request):
    forms = AddressForm()
    if request.method == 'POST':
        forms = AddressForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('address')
    district = Address.objects.all()
    context = {'forms': forms, 'address': district}
    return render(request, 'address/address.html', context)

