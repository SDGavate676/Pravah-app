from django.shortcuts import render, redirect
from .decorators import role_required
from .decorators import superuser_required

from django.http import HttpResponse
from django.utils import timezone

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.contrib.auth import logout

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import CandidateProfile 

from django.contrib import messages
from .forms import CandidateForm, EducationForm, SubmitCVForm
from .forms import EmployeeForm  
from .models import EmployeeProfile 
from .models import JobPostings
from django.shortcuts import get_object_or_404
from .forms import JobApplicationForm
from .models import JobApplication
from .models import SubmitCV
from .models import Contact
from .models import CustomUser
from .models import Education



from .forms import *

from .forms import RegistrationForm

from .forms import LoginForm



from .forms import JobPostingForm

from .forms import ContactForm

from .forms import AdminRegisterForm

from django.contrib.admin.views.decorators import staff_member_required



def admin_register(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.role = 'admin'
            form.save()
            return redirect('admin_login')
        else:
            print(form.errors)  
    else:
        form = AdminRegisterForm()
    return render(request, 'admin_register.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
           if user.is_superuser and user.role=='admin':  # check for admin/staff user
               login(request, user)
               return redirect('admin_dashboard')
           else:
            
              messages.error(request, 'Invalid credentials or not authorized as admin.')
              return redirect('admin_login')
        else:
           messages.error(request, 'Invalid credentials.')
           return redirect('admin_login')


    return render(request, 'admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login') 

# @staff_member_required(login_url='admin_login')

# def admin_dashboard(request):
#     query = request.GET.get('q', '')  # Unified query

#     # Candidates
#     candidates = CandidateProfile.objects.all()
#     if query:
#         candidates = candidates.filter(
#             Q(name__icontains=query) |
#             Q(email__icontains=query) |
#             Q(city__icontains=query)
#         )

#     # Employees
#     employees = EmployeeProfile.objects.all()
#     if query:
#         employees = employees.filter(
#             Q(name__icontains=query) |
#             Q(email__icontains=query) |
#             Q(company_name__icontains=query)
#         )

#     # Job Posts
#     job_posts = JobPostings.objects.all()
#     if query:
#         job_posts = job_posts.filter(
#             Q(job_title__icontains=query) |
#             Q(company_name__icontains=query) |
#             Q(job_location__icontains=query)
#         )

#     context = {
#         'query': query,  # Pass query back to template
#         'candidates': candidates,
#         'employees': employees,
#         'job_posts': job_posts,
#     }
#     return render(request, 'admin_dashboard.html', context)
def is_admin(user):
    return user.is_authenticated and user.is_superuser and user.role == 'admin'

@user_passes_test(is_admin, login_url='admin_login')

@superuser_required
def admin_dashboard(request):
    search_query = request.GET.get('search', '')

    candidates = CandidateProfile.objects.all()
    employees = EmployeeProfile.objects.all()
    job_posts = JobPostings.objects.all()

    if search_query:
        candidates = candidates.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(city__icontains=search_query)
        )

        employees = employees.filter(
            Q(company_name__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )

        job_posts = job_posts.filter(
            Q(job_title__icontains=search_query) |
            Q(job_location__icontains=search_query)
        )

    context = {
        'users': CustomUser.objects.all(),
        'candidates': candidates,           # ← filtered result
        'employees': employees,             # ← filtered result
        'job_posts': job_posts,             # ← filtered result
        'applications': JobApplication.objects.all(),
        'contacts': Contact.objects.all(),
        'query': search_query,
    }

    return render(request, 'admin_dashboard.html', context)




def dashboard_search(request):
    query = request.GET.get('q', '')

    candidates = CandidateProfile.objects.filter(
        Q(name__icontains=query) |
        Q(email__icontains=query) |
        Q(contact__icontains=query) |
        Q(city__icontains=query)
    )

    employees = EmployeeProfile.objects.filter(
        Q(name__icontains=query) |
        Q(email__icontains=query) |
        Q(company__icontains=query)
    )

    jobs = JobPostings.objects.filter(
        Q(title__icontains=query) |
        Q(company__icontains=query) |
        Q(location__icontains=query)
    )

    return render(request, 'dashboard.html', {
        'candidates': candidates,
        'employees': employees,
        'jobs': jobs,
        'query': query
    })



from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            role = form.cleaned_data['role'] 
            user.role = role  

            if role in ['Candidate', 'Employee']:
                
                user.is_staff = False      
                user.is_superuser = False

            user.save()

            request.session['role'] = role  

            login(request, user)

            messages.success(request, f'{role.capitalize()} account created successfully!')
            return redirect('login')
        else:
            print("Form Errors:", form.errors)  
            messages.error(request, 'Error creating account.')
    else:
        form = RegistrationForm()

    role_from_session = request.session.get('role', None)
    return render(request, 'register.html', {'form': form, 'role_from_session': role_from_session})


# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()  # Save the user
#             role = form.cleaned_data['role']  # Get the role from the form
            
#             # Store the role in the session
#             request.session['role'] = role

#             # Optionally, you can update the user's role if it's not set through the form
#             user.role = role
#             user.save()

#             # Log the user in after registration
#             login(request, user)

#             # Show success message and redirect
#             messages.success(request, f'{role.capitalize()} account created successfully!')
#             return redirect('login')
#         else:
#             messages.error(request, 'Error creating account.')
#     else:
#         form = RegistrationForm()

#     # Optionally, retrieve the role from session if needed
#     role_from_session = request.session.get('role', None)

#     return render(request, 'register.html', {'form': form, 'role_from_session': role_from_session})

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()  # Save the user
#             role = form.cleaned_data['role']  # Get the role from the form
            
#             # Optionally, you can update the user's role if it's not set through the form
#             user.role = role
#             user.save()

#             # Log the user in after registration
#             login(request, user)

#             # Show success message and redirect
#             messages.success(request, f'{role.capitalize()} account created successfully!')
#             return redirect('login')
#         else:
#             messages.error(request, 'Error creating account.')
#     else:
#         form = RegistrationForm()

#     return render(request, 'register.html', {'form': form})



# def register(request):   //Just use for candidate registration
     
#        if request.method == "POST":
#         form = CandidateRegistrationForm(request.POST)
#         if form.is_valid():
#             # Save the new user
#             form.save()
#             return redirect('login')  # Correct
#   # Redirect to login page or wherever you want
#        else:
#         form = CandidateRegistrationForm()

#        return render(request, 'register.html', {'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('create_profile')  # Redirect to the home page
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
            
#             # Store the user's role in the session
#             request.session['username'] = user.username
#             request.session['role'] = user.role

#             # Check the role of the logged-in user
#             if user.role == 'Employee':
#                 return redirect('emp_profile')  # Redirect to employee dashboard
#             elif user.role == 'Candidate':
#                 return redirect('create_profile')  # Redirect to student dashboard
#         else:
#             messages.error(request, 'Invalid username or password.')
    
#     return render(request, 'login.html')

##JUST COOMENTED CODE
# def user_login(request):
#     form = LoginForm(request.POST or None)

#     if request.method == 'POST':
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
            
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)

#                 request.session['username'] = user.username
#                 request.session['role'] = user.role

#                 if user.role == 'Employee':
#                     return redirect('emp_profile')
#                 elif user.role == 'Candidate':
#                     return redirect('create_profile')
#             else:
#                 messages.error(request, 'Invalid username or password.')
                

#     return render(request, 'login.html', {'form': form})

def user_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                request.session['username'] = user.username
                request.session['role'] = user.role

                if user.role == 'Candidate':
                    try:
                        CandidateProfile.objects.get(user=user)
                        return redirect('candi_dashboard')
                    except CandidateProfile.DoesNotExist:
                        return redirect('create_profile')

                elif user.role == 'Employee':
                    try:
                        EmployeeProfile.objects.get(user=user)
                        return redirect('emp_dashboard')
                    except EmployeeProfile.DoesNotExist:
                        return redirect('emp_profile')

            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    # Clear session data
    request.session.flush()  # This will clear all session data, including the 'username' and 'role'
    return redirect('login')


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
            
#             # Check the role of the logged-in user
#             if user.role == 'employee':
#                 return redirect('employee_dashboard')  # Redirect to employee dashboard
#             elif user.role == 'student':
#                 return redirect('student_dashboard')  # Redirect to student dashboard
#         else:
#             messages.error(request, 'Invalid username or password.')
    
#     return render(request, 'login.html')


# @login_required 
# def user_logout(request):
#     logout(request)  # Logs the user out
#     return redirect('login') 

# def user_login(request):  //just use for candidate login
    
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)  
#             request.session['username'] = username  # Store in session
#             return redirect('create_profile')  # Or wherever you want to go after login
#         else:
#             messages.error(request, "Invalid credentials.")
    
#     return render(request, 'login.html')



    # if request.method == 'POST':
    #     form = AuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #         user = authenticate(username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             # You can also store custom session data here if needed:
    #             request.session['username'] = username  # Example of session storage

    #             return redirect('create_profile')  # Redirect to the create_profile view
    # else:
    #     form = AuthenticationForm()

    # return render(request, 'login.html', {'form': form})

# @login_required 
# def user_logout(request):
#     logout(request)  # Logs the user out
#     return redirect('login') 

# def logout_view(request):    // just use for candidate logout
#     logout(request)  # Django's built-in logout function
#     if 'username' in request.session:
#         del request.session['username']  # Session साफ करा
#     return redirect('login')  

# def candidate_logout(request):
#     try:
#         del request.session['username']  # Remove session value
#     except KeyError:
#         pass
#     return redirect('login') 

def create_profile(request):
     
    context = {
        'username': request.user.username  
    }
    return render(request, 'create_profile.html', context)  

# def empregistration(request):  //just use for employer registration
     
#        if request.method == "POST":
#         form = EmployerRegistrationForm(request.POST)
#         if form.is_valid():
#             # Save the new user
#             form.save()
#             return redirect('emplogin')  # Correct
#   # Redirect to login page or wherever you want
#        else:
#         form = EmployerRegistrationForm()

#        return render(request, 'empregistration.html', {'form': form})


# def emplogin(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 emplogin(request, user)
#                 # You can also store custom session data here if needed:
#                 request.session['username'] = username  # Example of session storage

#                 return redirect('emp_profile')  # Redirect to the create_profile view
#     else:
#         form = AuthenticationForm()

#     return render(request, 'emplogin.html', {'form': form})

def emplogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # ✅ correct function here
                request.session['username'] = username
                return redirect('emp_profile')  # Redirect to the employer profile
    else:
        form = AuthenticationForm()

    return render(request, 'emplogin.html', {'form': form})


@login_required 
def emplogout(request):
    emplogout(request)  # Django's built-in logout function
    if 'username' in request.session:
        del request.session['username']  # Session साफ करा
    return redirect('login') 

def emp_profile(request):
    context = {
        'username': request.user.username  
    }
    return render(request, 'emp_profile.html', context)

def emp_profile(request):
      if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            # Automatically associate the form with the logged-in user
            profile = form.save(commit=False)
            profile.user = request.user  # Associate the current user with the profile
            profile.save()
            return redirect('profile_success')  # Redirect after successful form submission
      else:
        form = EmployeeForm()
    
      return render(request, 'emp_profile.html',  {'form': form})

# def emp_profile(request):
#     if request.method == 'POST':
#         form = EmployeeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/emp_profile/')  # Avoid form re-submission on refresh
#     else:
#         form = EmployeeForm()
    
#     return render(request, 'emp_profile.html', {
#         'form': form,
#         'username': request.session.get('username')
#     })





# def create_profile(request):
#     if request.method == 'POST':
#         form = CandidateForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             return redirect('index')  # Redirect to a success page after saving the profile
#     else:
#         form = CandidateForm()
    
#     return render(request, 'create_profile.html', {'form': form})
@login_required(login_url='login')
def create_profile(request):
   
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            # Automatically associate the form with the logged-in user
            profile = form.save(commit=False)
            profile.user = request.user  # Associate the current user with the profile
            profile.save()
            return redirect('educationdetail')  # Redirect after successful form submission
    else:
        form = CandidateForm()
    
    return render(request, 'create_profile.html',  {'form': form})

def profile_success(request):
    return render(request, 'profile_success.html')  

def profile_successcandidate(request):
    return render(request, 'profile_successcandidate.html')

# Render a success page after profile creation

# def educationdetail(request):
#     if request.method == 'POST':
#         form = EducationForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             return redirect('submitcv')  # Redirect to a success page after saving the profile
#     else:
#         form = EducationForm()
    
#     return render(request, 'educationdetail.html', {'form': form})

# def educationdetail(request):
#     if request.method == 'POST':
#         form = EducationForm(request.POST)
#         if form.is_valid():
#             education = form.save(commit=False)
#             education.candidate = request.user # Adjust as per your logic
#             education.save()
#             return redirect('submitcv')
#     else:
#         form = EducationForm()
#     return render(request, 'educationdetail.html', {'form': form})

def educationdetail(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            # Fetch the CandidateProfile instance associated with the logged-in user
            candidate_profile = CandidateProfile.objects.get(user=request.user)  # Adjust based on your model setup
            education.candidate = candidate_profile  # Set the candidate as the CandidateProfile instance
            education.save()
            return redirect('submitcv')  # Redirect to the submitcv page or another page after saving
    else:
        form = EducationForm()
    return render(request, 'educationdetail.html', {'form': form})


# def submitcv(request):
#     if request.method == 'POST':
#         form = SubmitCVForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             return redirect('create_profile')  # Redirect to a success page after saving the profile
#     else:
#         form = SubmitCVForm()
    
#     return render(request, 'submitcv.html', {'form': form})


def submitcv(request):
    if request.method == 'POST':
        form = SubmitCVForm(request.POST, request.FILES)
        if form.is_valid():
            # Before saving, set the candidate to the current user's CandidateProfile
            submit_cv = form.save(commit=False)
            submit_cv.candidate = CandidateProfile.objects.get(user=request.user)  # Adjust as necessary
            submit_cv.save()
            return redirect('profile_successcandidate')  # Redirect to a success page after saving the profile
    else:
        form = SubmitCVForm()
    
    return render(request, 'submitcv.html', {'form': form})


def index(request):
    

    # query = request.GET.get('q', '')
    # if query:
    #     jobs = JobPostings.objects.filter(
    #         job_title__icontains=query
    #     )
    # else:
    #     jobs = JobPostings.objects.all()

    # return render(request, 'joblist.html', {
    #     'jobs': jobs,
    #     'query': query
    # })
    return render(request, 'index.html')



def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def features(request):
    return render(request, 'features.html')

def jobpostings(request):
    return render(request, 'jobpostings.html')

def contact(request):
    return render(request, 'contact.html')

def ourservices(request):
    return render(request, 'ourservices.html' )





# def main(request):
#     return render(request, 'main.html')





# def jobpostings(request):
#     if request.method == 'POST':
      
#         form = JobPostingForm(request.POST)
#         if form.is_valid():
          
#             form.save()
#             return redirect('index') 
#         else:
           
            # return HttpResponse("Form is invalid")
    #         return HttpResponse(f"Form errors: {form.errors}")

    # else:
       
    #     form = JobPostingForm()

   
    # return render(request, 'jobpostings.html', {'form': form})
# def is_employee_or_admin(user):
#     return user.is_authenticated and user.role in ['employee', 'admin']

# # View restricted to employee and admin
# @user_passes_test(is_employee_or_admin, login_url='unauthorized')

@login_required
@role_required(['Employee', 'admin'])

# Ensure only employees can access this view

# 
@login_required
# 

# def jobpostings(request):
#     if request.method == 'POST':
#         form = JobPostingForm(request.POST)
#         if form.is_valid():
#             job = form.save(commit=False)
#             job.posted_by = request.user.employee_profile  # ✅ important!
#             job.save()
#             return redirect('emp_dashboard')
#         else:
#             jobs = JobPostings.objects.filter(posted_by=personal)
#             today = timezone.now().date()
#             return render(request, 'jobpostings.html', {'form': form})
#     else:
#         form = JobPostingForm()
#     return render(request, 'jobpostings.html', {
#         'form': form,
#         'jobs':jobs,
#         'today': today
# })

def jobpostings(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user.employee_profile  # ✅ important!
            job.save()
            return redirect('emp_dashboard')
        else:
            jobs = JobPostings.objects.filter(posted_by=request.user.employee_profile)
            today = timezone.now().date()
            return render(request, 'jobpostings.html', {'form': form, 'jobs': jobs, 'today': today})
    
    else:
        form = JobPostingForm()
        jobs = JobPostings.objects.filter(posted_by=request.user.employee_profile)
        today = timezone.now().date()
        return render(request, 'jobpostings.html', {
            'form': form,
            'jobs': jobs,
            'today': today
        })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save form data to the database
            return redirect('thank_you')  
        else:
          
            return HttpResponse("Form is invalid")
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def thank_you(request):
    return render(request, 'thank_you.html')  
# Create this template to show thank you message
@login_required
@role_required(['Candidate', 'admin'])


def joblist(request):
    
    query = request.GET.get('q', '')
    if query:
        jobs = JobPostings.objects.filter(job_title__icontains=query)
       
    else:
        jobs = JobPostings.objects.all()
    
    return render(request, 'joblist.html', {'jobs': jobs, 'query': query})
   



# def apply_job(request):
    
#     if request.method == 'POST':
       
#         form = JobApplicationForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Process the form (e.g., save to the database, send email)
#             form.save()  # Assuming you're saving to a model
#             return redirect('success_page')  # Redirect to a success page after submission
#     else:
#         form = JobApplicationForm()
    
#     return render(request, 'apply_job.html', {'form': form})

@login_required
@role_required('Candidate')

def apply_job(request, job_id):
    job = get_object_or_404(JobPostings, id=job_id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job  # Link the job to the application
            application.applicant = request.user  # Optional: Save user info
            application.save()
            return redirect('success_page')
    else:
        form = JobApplicationForm()
    
    return render(request, 'apply_job.html', {'form': form, 'job': job})

def success_page(request):
    
    return render(request, 'success_page.html')  # Create this template to show success message


def job_application_list(request):
    # Fetch all job applications
    job_applications = JobApplication.objects.all()

    search_query = request.GET.get('search', '')
    job_position = request.GET.get('job_position', '')

    if search_query:
        job_applications = job_applications.filter(
            Q(full_name__icontains=search_query) 
        )

    
    if job_position:
        job_applications = job_applications.filter(job_position=job_position)


    job_positions = JobApplication.objects.values_list('job_position', flat=True).distinct()
    
    context = {
        'job_applications': job_applications,
        'job_positions': job_positions,
    }
    return render(request, 'job_application_list.html', context)

def candidate_resume_list(request):
    # Fetch all job applications
    submit_cv = SubmitCV.objects.select_related('candidate').all()
    return render(request, 'candidate_resume_list.html', {'submit_cv': submit_cv})


def contact_detail_list(request):

    contact_detail = Contact.objects.all()

    search_query = request.GET.get('search', '')
    subject = request.GET.get('subject', '')
    if search_query:
        contact_detail = contact_detail.filter(
            Q(full_name__icontains=search_query) 
        )

    if subject:
        contact_detail = contact_detail.filter(subject=subject)

    subject_list = Contact.objects.values_list('subject', flat=True).distinct()
    context = {
        'contact_detail': contact_detail,
        'subject_list': subject_list,
    }

    return render(request, 'contact_detail_list.html',context)


def user_detail_list(request):
   
   user_detail = CustomUser.objects.all()

   search_query = request.GET.get('search', '')
   if search_query:
       user_detail = user_detail.filter(
           Q(username__icontains=search_query) |
           Q(email__icontains=search_query)
       )

   role_filter = request.GET.get('role', '')
   if role_filter:
       user_detail = user_detail.filter(role=role_filter)

  

   return render(request, 'user_detail_list.html', {'user_detail': user_detail} )


def candidate_detail_list(request):
   
   candidate_detail = CandidateProfile.objects.all()
   return render(request, 'candidate_detail_list.html', {'candidate_detail':  candidate_detail} )


def candidate_detail_list(request):
    candidates = CandidateProfile.objects.all()
    
    search_query = request.GET.get('search', '')
    gender_filter = request.GET.get('gender', '')
    village = request.GET.get('village','')
    state = request.GET.get('state', '')
    district = request.GET.get('district', '')

    if search_query:
        candidates = candidates.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if gender_filter:
        candidates = candidates.filter(gender=gender_filter)

    if village:
        candidates = candidates.filter(village=village)
    
    if state:
        candidates = candidates.filter(state=state)

    if district:
        candidates = candidates.filter(district=district)

    village = CandidateProfile.objects.values_list('village', flat=True).distinct()
    states = CandidateProfile.objects.values_list('state', flat=True).distinct()
    districts = CandidateProfile.objects.values_list('district', flat=True).distinct()

    
    context = {
        'candidate_detail': candidates,
        'village': village,
        'states': states,
        'districts': districts,
    }

    return render(request, 'candidate_detail_list.html', context) 
       




def candidate_education_list(request):
    candidate_education = Education.objects.select_related('candidate').all()

    search_query = request.GET.get('search', '')
    degree = request.GET.get('degree', '')
    course_name = request.GET.get('course_name', '')
    college = request.GET.get('college', '')
    year_of_passing = request.GET.get('year_of_passing', '')
    experience = request.GET.get('experience', '')
    interested_sector = request.GET.get('interested_sector', '')

    if search_query:
        candidate_education = candidate_education.filter(
            Q(candidate__name__icontains=search_query) 
    )

    if degree:
        candidate_education = candidate_education.filter(degree=degree)
    if course_name:
        candidate_education = candidate_education.filter(course_name=course_name)
    if college:
        candidate_education = candidate_education.filter(college=college)
    if year_of_passing:
        candidate_education = candidate_education.filter(year_of_passing=year_of_passing)
    if experience:
        candidate_education = candidate_education.filter(experience=experience)
    if interested_sector:
        candidate_education = candidate_education.filter(interested_sector=interested_sector)

    context = {
        'candidate_education': candidate_education,
        'degree_list': Education.objects.values_list('degree', flat=True).distinct(),
        'course_name_list': Education.objects.values_list('course_name', flat=True).distinct(),
        'college_list': Education.objects.values_list('college', flat=True).distinct(),
        'year_of_passing_list': Education.objects.values_list('year_of_passing', flat=True).distinct(),
        'experience_list': Education.objects.values_list('experience', flat=True).distinct(),
        'interested_sector_list': Education.objects.values_list('interested_sector', flat=True).distinct(),
    }

    return render(request, 'candidate_education_list.html', context)


def employee_detail_list(request):
   
   employee_detail = EmployeeProfile.objects.all()

   search_query = request.GET.get('search', '')
   designation = request.GET.get('designation', '')
   sector = request.GET.get('sector', '')
   location = request.GET.get('location', '')

   if search_query:
         employee_detail = employee_detail.filter(
              Q(name__icontains=search_query) |
              Q(email__icontains=search_query) |
              Q(company_name__icontains=search_query)
         )

   
   if designation:
        employee_detail = employee_detail.filter(designation=designation)

  
   if sector:
        employee_detail = employee_detail.filter(sector=sector) 

   
   if location:
        employee_detail = employee_detail.filter(location=location)

   context = {
        'employee_detail': employee_detail,
        'designation_list': EmployeeProfile.objects.values_list('designation', flat=True).distinct(),
        'sector_list': EmployeeProfile.objects.values_list('sector', flat=True).distinct(),
        'location_list': EmployeeProfile.objects.values_list('location', flat=True).distinct()
    }
        
   return render(request, 'employee_detail_list.html', context)

def jobposting_detail_list(request):
   
   jobposting_detail = JobPostings.objects.all()

   search_query = request.GET.get('search', '')
   if search_query:
        jobposting_detail = jobposting_detail.filter(
            Q(job_title__icontains=search_query) 
          
        )

   
   job_title = request.GET.get('job_title', '')
   company_name = request.GET.get('company_name', '')
   job_location = request.GET.get('job_location', '')
   employment_type = request.GET.get('employement_type', '')

   if job_title:
        jobposting_detail = jobposting_detail.filter(job_title=job_title)
   if company_name:
        jobposting_detail = jobposting_detail.filter(company_name=company_name)
   if job_location:
        jobposting_detail = jobposting_detail.filter(job_location=job_location)

   if employment_type:
        jobposting_detail = jobposting_detail.filter(employment_type=employment_type)
    
   context = {
        'jobposting_detail': jobposting_detail,
        'job_title_list': JobPostings.objects.values_list('job_title', flat=True).distinct(),
        'company_name_list': JobPostings.objects.values_list('company_name', flat=True).distinct(),
        'job_location_list': JobPostings.objects.values_list('job_location', flat=True).distinct(),
        'employment_type_list': JobPostings.objects.values_list('employment_type', flat=True).distinct()
    }


   return render(request, 'jobposting_detail_list.html', context) 

def unauthorized(request):
    return render(request, 'unauthorized.html')


def delete_candidate(request, pk):
    candidate = get_object_or_404(CandidateProfile, pk=pk)
    if request.method == 'POST':
        candidate.delete()
        return redirect('admin_dashboard')
    return render(request, 'delete_candidate.html', {'candidate': candidate})

def delete_employee(request, pk):
    employee = get_object_or_404(EmployeeProfile, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('admin_dashboard')
    return render(request, 'delete_employee.html', {'employee': employee})

def add_job(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('joblist')  # Change to your listing view name
    else:
        form = JobPostingForm()
    return render(request, 'add_job.html', {'form': form})

def update_job(request, id):
    job = get_object_or_404(JobPostings, id=id)
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('joblist')
    else:
        form = JobPostingForm(instance=job)
    return render(request, 'update_job.html', {'form': form})

def delete_job(request, id):
    job = get_object_or_404(JobPostings, id=id)
    if request.method == 'POST':
        job.delete()
        return redirect('joblist')
    return render(request, 'delete_job.html', {'job': job})

def delete_users(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_detail_list')
    return render(request, 'delete_users.html', {'user': user})

def delete_apply_candidate(request, pk):
    applied = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        applied.delete()
        return redirect('job_application_list')
    return render(request, 'delete_apply_candidate.html', {'applied': applied})

def delete_contact_detail(request, pk):
    delete_contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        delete_contact.delete()
        return redirect('contact_detail_list')
    return render(request, 'delete_contact_detail.html', {' delete_contact':  delete_contact})

# views.py
def candidate_dashboard(request):
    user = request.user

    # Step 1: Get existing data
    personal = CandidateProfile.objects.filter(user=user).first()
    education = Education.objects.filter(candidate=personal).first()
    resume = SubmitCV.objects.filter(candidate=personal).first()

    if request.method == 'POST':
        # Step 2: Bind existing instance for update
        personal_form = CandidateForm(request.POST, instance=personal)
        education_form = EducationForm(request.POST, instance=education)
        resume_form = SubmitCVForm(request.POST, request.FILES, instance=resume)

        if personal_form.is_valid() and education_form.is_valid() and resume_form.is_valid():
            # Step 3: Save updates
            pf = personal_form.save(commit=False)
            pf.user = user
            pf.save()

            ef = education_form.save(commit=False)
            ef.user = user
            ef.save()

            rf = resume_form.save(commit=False)
            rf.user = user
            rf.save()

            return redirect('candidate_dashboard')  # Same page reload
    else:
        # Show current values
        personal_form = CandidateForm(instance=personal)
        education_form = EducationForm(instance=education)
        resume_form = SubmitCVForm(instance=resume)

    return render(request, 'candidate_dashboard.html', {
        'personal_form': personal_form,
        'education_form': education_form,
        'resume_form': resume_form,
    })

# def employee_dashboard(request):
#     user = request.user

#     # Step 1: Get existing data
#     personal = EmployeeProfile.objects.filter(user=user).first()

#     if request.method == 'POST':
#         # Step 2: Bind existing instance for update
#         personal_form = EmployeeForm(request.POST, instance=personal)

#         if personal_form.is_valid():
#             # Step 3: Save updates
#             pf = personal_form.save(commit=False)
#             pf.user = user
#             pf.save()

#             return redirect('employee_dashboard')  # Same page reload
#     else:
#         # Show current values
#         personal_form = EmployeeForm(instance=personal)

#     return render(request, 'employee_dashboard.html', {
#         'personal_form': personal_form,
#     })

def employee_dashboard(request):
    user = request.user

    personal = EmployeeProfile.objects.filter(user=user).first()
    
    # Get jobs posted by this employee
    jobs = JobPostings.objects.filter(posted_by=personal)

    if request.method == 'POST':
        personal_form = EmployeeForm(request.POST, instance=personal)
        if personal_form.is_valid():
            pf = personal_form.save(commit=False)
            pf.user = user
            pf.save()
            return redirect('employee_dashboard')
    else:
        personal_form = EmployeeForm(instance=personal)
       
       
        today = timezone.now().date()

    return render(request, 'employee_dashboard.html', {
        'personal_form': personal_form,
        'jobs': jobs, 
        'today':today,
    })

# def emp_dashboard(request):
#     # total_jobs = JobPostings.objects.filter(employer=request.user).count()
#     # total_applications =JobApplication.objects.filter(job__posted_by=request.user).count()
#     # active_jobs = JobPostings.objects.filter(employer=request.user, status='active').count()
    
#     user = request.user
#     personal = EmployeeProfile.objects.filter(user=user).first()
#     jobs = JobPostings.objects.filter(posted_by=personal)
#     today = timezone.now().date()

#     return render(request, 'emp-dashboard.html', {
#         # 'total_jobs': total_jobs,
#         # 'total_applications': total_applications,
#         # 'active_jobs': active_jobs,
       
#         'jobs': jobs,
#         'today': timezone.now().date(),
#     })

from django.utils import timezone
from .models import JobPostings, JobApplication, EmployeeProfile

def emp_dashboard(request):
    user = request.user
    personal = EmployeeProfile.objects.filter(user=user).first()

    if personal:
        jobs = JobPostings.objects.filter(posted_by=personal)
        total_jobs = jobs.count()
        total_applications = JobApplication.objects.filter(job__posted_by=personal).count()
        today = timezone.now().date()
        active_jobs = JobPostings.objects.filter(posted_by=personal, application_deadline__gte=today).count()

      
    else:
        jobs = []
        total_jobs = 0
        total_applications = 0
        active_jobs = 0

    today = timezone.now().date()

    return render(request, 'emp-dashboard.html', {
        'jobs': jobs,
        'today': today,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'active_jobs': active_jobs,
    })


# def candi_dashboard(request):
#     # user = request.user
#     # total_applied = Application.objects.filter(candidate=user).count()
#     # shortlisted = Application.objects.filter(candidate=user, status='shortlisted').count()
#     # interviews = Interview.objects.filter(candidate=user).count()

#     return render(request, 'candi_dashboard.html', {
#         # 'total_applied': total_applied,
#         # 'shortlisted': shortlisted,
#         # 'interviews': interviews,
#     })

def candi_dashboard(request):
    # 1. Get the candidate profile for the logged‑in user
    candidate = get_object_or_404(CandidateProfile, user=request.user)

    # 2. Total jobs applied
    total_applied = JobApplication.objects.filter(candidate=candidate).count()

    # 3. Shortlisted applications
    shortlisted = JobApplication.objects.filter(candidate=candidate, status='shortlisted').count()

   
   

    return render(request, 'candi_dashboard.html', {
        'total_applied': total_applied,
        'shortlisted': shortlisted,
        
    })

def check(request):
    return render(request, 'check.html')

# def jobedit(request, id):
#     job = get_object_or_404(JobPostings, id=id, user=request.user)  
    

#     if request.method == 'POST':
#         form = JobPostingForm(request.POST, request.FILES, instance=job)
#         if form.is_valid():
#             form.save()
#             return redirect('joblist')  # replace with your job list view name
#     else:
#         form = JobPostingForm(instance=job)

#     return render(request, 'jobedit.html', {'form': form, 'job': job})

# @login_required
# def job_edit_view(request, id):
#     job = get_object_or_404(JobPostings, id=id, posted_by=request.user.EmployeeProfile)  # Ensure the job belongs to the logged-in user

#     if request.method == 'POST':
#         form = JobPostingForm(request.POST, instance=job)
#         if form.is_valid():
#             form.save()
#             return redirect('joblist')  # or your job list page
#     else:
#         form = JobPostingForm(instance=job)

#     return render(request, 'jobedit.html', {'form': form, 'job': job})


from django.core.exceptions import ObjectDoesNotExist

@login_required
def job_edit_view(request, id):
    try:
        employee_profile = request.user.employee_profile
    except ObjectDoesNotExist:
        messages.error(request, "You do not have an employee profile.")
        return redirect('employee_dashboard')  # or another fallback

    job = get_object_or_404(JobPostings, id=id, posted_by=employee_profile)

    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect('joblist')  # update if needed
    else:
        form = JobPostingForm(instance=job)

    return render(request, 'jobedit.html', {'form': form, 'job': job})

# def job_delete_view(request, id):
#     job = get_object_or_404(JobPostings, id=id, posted_by=request.user.employee_profile)

#     if job.application_deadline < timezone.now().date():
#         job.delete()
#         return redirect('employee_dashboard')  # or wherever you want to redirect
#     else:
#         # Optional: show error message if trying to delete before deadline
#         return redirect('employee_dashboard')

def job_delete_view(request, id):
    job = get_object_or_404(JobPostings, id=id, posted_by=request.user.employee_profile)

    if job.application_deadline <= timezone.now().date():
        job.delete()
        messages.success(request, f"Job '{job.job_title}' deleted successfully.")
    else:
        messages.warning(request, "Cannot delete the job before its application deadline.")

    return redirect('employee_dashboard')

def view_applicants(request):
    personal = EmployeeProfile.objects.get(user=request.user)
    applications = JobApplication.objects.filter(job__posted_by=personal)

    return render(request, 'view_applicants.html', {
        'applications': applications
    })

