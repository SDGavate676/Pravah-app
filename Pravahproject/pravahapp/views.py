from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import CandidateProfile 
from django.contrib import messages
from .forms import CandidateForm, EducationForm, SubmitCVForm
from .forms import EmployeeForm  # Import the form class (ensure it's in the correct path)
from .models import EmployeeProfile 
from .models import JobPostings
from django.shortcuts import get_object_or_404
from .forms import JobApplicationForm

from .forms import *

from .forms import RegistrationForm

from .forms import LoginForm

# from .forms import EmployerRegistrationForm
# from .forms import CandidateRegistrationForm

from .forms import JobPostingForm

from .forms import ContactForm

# Candidate Registration
# ---------------------------
# def candidate_register(request):
#     if request.method == 'POST':
#         form = CandidateRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user, backend='accounts.backends.CandidateBackend')
#             messages.success(request, "Candidate registered and logged in!")
#             return redirect('login')
#     else:
#         form = CandidateRegistrationForm()
#     return render(request, 'register.html', {'form': form})

# ---------------------------
# Employer Registration
# ---------------------------
# def employer_register(request):
#     if request.method == 'POST':
#         form = EmployerRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user, backend='accounts.backends.EmployerBackend')
#             messages.success(request, "Employer registered and logged in!")
#             return redirect('emp_login')
#     else:
#         form = EmployerRegistrationForm()
#     return render(request, 'empregistration.html', {'form': form})

# ---------------------------
# Candidate Login
# ---------------------------
# def candidate_login(request):
    # if request.method == 'POST':
    #     email = request.POST['email']
    #     password = request.POST['password']
    #     user = authenticate(request, email=email, password=password, backend='accounts.backends.CandidateBackend')
    #     if user:
    #         login(request, user, backend='accounts.backends.CandidateBackend')
    #         return redirect('create_profile')
    #     else:
    #         messages.error(request, 'Invalid credentials')
    # return render(request, 'login.html')

# ---------------------------
# Employer Login
# ---------------------------
# def employer_login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request, email=email, password=password, backend='accounts.backends.EmployerBackend')
#         if user:
#             login(request, user, backend='accounts.backends.EmployerBackend')
#             return redirect('emp_profile')
#         else:
#             messages.error(request, 'Invalid credentials')
#     return render(request, 'emplogin.html')

from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)  # Don't save to DB yet
#             role = form.cleaned_data['role']  # Get the role
#             user.role = role  # Set the role before saving
#             if role in ['Candidate', 'Employee']:
#                 user.is_staff = True  # Can access Django admin
#                 user.is_superuser = True
#             user.set_password(form.cleaned_data['password'])  # Set password securely
#             user.save()

#             request.session['role'] = role  # Save role in session

#             # Authenticate and log in the user after registration
#             user = authenticate(username=user.username, password=form.cleaned_data['password'])
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f'{role.capitalize()} account created and logged in successfully!')
#                 return redirect('dashboard')  # Redirect to a page after login
#             else:
#                 messages.error(request, 'Error logging in after registration.')
#         else:
#             print("Form Errors:", form.errors)  # Debug in console
#             messages.error(request, 'Error creating account.')
#     else:
#         form = RegistrationForm()

#     role_from_session = request.session.get('role', None)
#     return render(request, 'register.html', {'form': form, 'role_from_session': role_from_session})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to DB yet
            role = form.cleaned_data['role']  # Get the role
            user.role = role  # Set the role before saving

            if role in ['Candidate', 'Employee']:
                user.is_staff = True       # Can access Django admin
                user.is_superuser = True 

            user.save()

            request.session['role'] = role  # Save role in session

            login(request, user)

            messages.success(request, f'{role.capitalize()} account created successfully!')
            return redirect('login')
        else:
            print("Form Errors:", form.errors)  # Debug in console
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

                if user.role == 'Employee':
                    return redirect('emp_profile')
                elif user.role == 'Candidate':
                    return redirect('create_profile')
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
def jobpostings(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('index')  # Redirect to another view or the same view (like 'index')
        else:
            # Return the form with errors and print the errors in the template
            return render(request, 'jobpostings.html', {'form': form})

    else:
        form = JobPostingForm()  # If GET, just show an empty form

    return render(request, 'jobpostings.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save form data to the database
            return redirect('index')  
        else:
          
            return HttpResponse("Form is invalid")
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

@login_required
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
