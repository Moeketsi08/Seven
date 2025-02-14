def admin_login(request):
    forms = CenterManagerLoginForm()

    if request.method == 'POST':
        forms = CenterManagerLoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_superuser:
                    login(request, user)

                    # Fetch the centers associated with the admin's center managers
                    centers = Center.objects.filter(center_managers=user.center_managers)

                    # Store centers in the session
                    request.session['centers'] = list(centers.values('name'))  

                    # Display a welcome message
                    messages.success(request, f'Welcome, Administrator {user.username}')

                    return redirect('home')
                else:
                    messages.error(request, "You do not have admin privileges.")
            else:
                messages.error(request, "Invalid username or password.")

    context = {'forms': forms}
    return render(request, 'center_manager/login.html', context)