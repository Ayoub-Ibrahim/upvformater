from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import LoginForm, UserRegistrationForm, UserEditForm 
from . models import Conversion, Numeric
from . utils import convert_to_moodle_format, convert_input_to_gift

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'upvformat/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')



def home(request):
    return render(request,'upvformat/home.html',{'section': 'home'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'upvformat/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'upvformat/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated '\
                                      'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'upvformat/edit.html', {'user_form': user_form}) 

@login_required(login_url='/login/')
def multichoice(request):
    if request.method == 'POST':
        text_content = request.POST.get('text_content', '')
        input_file = request.FILES.get('file')
        if input_file:
            input_text = input_file.read().decode('utf-8')
        else:
            input_text = text_content        
        conversion = Conversion.objects.create(input_text=input_text)
        conversion.save()
        output_text = convert_to_moodle_format(input_text) 
        conversion.output_text = output_text
        conversion.save()
        response = HttpResponse(output_text, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="converted_output.txt"'        
        return response
    return render(request, 'upvformat/multichoice.html')

@login_required(login_url='/login/')
def numerical(request):
    if request.method == 'POST':
        question_text = request.POST.get('text_content', '')
        try:
            gift_format = convert_input_to_gift(question_text)
            question = Numeric.objects.create(question_text=question_text, gift_format=gift_format)
            response = HttpResponse(gift_format, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="question.txt"'
            return response
        except ValueError as e:
            return render(request, 'upvformat/numeric.html', {'error': str(e)})
    return render(request, 'upvformat/numeric.html')


def help(request):
    return render(request, 'upvformat/help.html')

def about(request):
    return render(request, 'upvformat/about.html')
