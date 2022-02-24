from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.decorators import login_required

def register(request):

    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            ## Writing form data to user database
            form.save()
            uname=form.cleaned_data.get('username')
            # print(uname)

            messages.success(request,f'Account created for {uname}. Kindly login.')

            return redirect('login')
    else:
        form=UserRegisterForm()

    return render(request,'users/register.html',{'form':form})

@login_required    
def profile(request):

    if request.method == 'POST':
        print(request.POST)

        print(request.content_params)
        print(request.GET)
        print("BODY")
        # print(request.data)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        # values = [value for name, value in request.POST.iteritems()]
        # print(values)


    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


