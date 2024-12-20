from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'employees/login.html', {'error': 'Invalid credentials'})
    return render(request, 'employees/login.html')


@login_required

def dashboard(request):
    total_employees = Employee.objects.count()
    return render(request, 'employees/dashboard.html', {'total_employees': total_employees})

def add_employee(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile_no = request.POST['mobile_no']
        designation = request.POST['designation']
        gender = request.POST['gender']
        course = request.POST['course']
        image = request.FILES.get('image')

        Employee.objects.create(
            name=name,
            email=email,
            mobile_no=mobile_no,
            designation=designation,
            gender=gender,
            course=course,
            image=image
        )
        return redirect('employee_list')

    return render(request, 'employees/add_employee.html')

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})
def user_logout(request):
    logout(request)
    return redirect('login')
def force_logout(request):
    logout(request)
    return redirect('login')  # Red

def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employee.name = request.POST['name']
        employee.email = request.POST['email']
        employee.mobile_no = request.POST['mobile_no']
        employee.designation = request.POST['designation']
        employee.gender = request.POST['gender']
        employee.course = request.POST['course']
        if 'image' in request.FILES:
            employee.image = request.FILES['image']
        employee.save()
        return redirect('employee_list')

    return render(request, 'employees/edit_employee.html', {'employee': employee})
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('employee_list')

