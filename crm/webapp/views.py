from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Record
from .forms import CreateUserForm, LoginForm, AddRecordForm, UpdateRecordForm


# Homepage
def home(request):
    return render(request, 'webapp/index.html')


# Register
def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = CreateUserForm()

    if (request.method == "POST"):
        form = CreateUserForm(request.POST)
        print(form)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')

            return redirect('/login')
        else:
            messages.error(request, 'Error creating account')

    context = {'form': form}
    return render(request, 'webapp/register.html', context)


# Login user
def login_user(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
        else:
            messages.error(request, 'Error logging in')
            return redirect('/login')

    context = {'form': form}
    return render(request, 'webapp/login.html', context)


# User Dashboard
@login_required(login_url='login')
def user_dashboard(request):
    my_records = Record.objects.all()
    return render(
        request,
        'webapp/dashboard.html',
        context={'records': my_records}
    )


# create record
@login_required(login_url='login')
def create_record(request):
    form = AddRecordForm()

    if request.method == "POST":
        form = AddRecordForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Record added successfully')
            return redirect('/dashboard')
        else:
            messages.error(request, 'Error adding record')

    return render(
        request,
        'webapp/create_record.html',
        context={'form': form}
    )


# View single record
@login_required(login_url='login')
def view_record(request, pk):
    record = Record.objects.get(id=pk)
    return render(
        request,
        'webapp/view_record.html',
        context={'record': record}
    )


# Update a record
@login_required(login_url='login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)

    if request.method == "POST":
        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully')
            return redirect('/view_record/' + str(pk))
        else:
            messages.error(request, 'Error updating record')

    return render(
        request,
        'webapp/update_record.html',
        context={'form': form}
    )


# Delete a record
@login_required(login_url='login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)

    record.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect('/dashboard')


# Logout user
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('/login')
