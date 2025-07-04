
from django.conf import settings
from django.utils import timezone

from django.db import models 



from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(r'^[A-Za-z\s]+$', 'Username must contain only letters and spaces.')
        ]
    )
      # Defining user roles as choices
    ROLE_CHOICES = [
        ('Candidate', 'Candidate'),
        
        ('Employee', 'Employee'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Candidate')
    registered_at = models.DateField(default=timezone.now) 

  

   

    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_set', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_permissions_set', blank=True
    )


    def __str__(self):
        return self.username

# class Employee(models.Model):
#        user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,  # Use the custom user model
#         on_delete=models.CASCADE,
#         null=False,
#         blank=True
#     )
#        username = models.CharField(max_length=100)
#        email = models.EmailField()
#        password = models.CharField(max_length=100)
#        confirm_password = models.CharField(max_length=100)
   
# def __str__(self):
#         return self.name

# class Candidate(models.Model):
#        user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,  # Use the custom user model
#         on_delete=models.CASCADE,
#         null=False,
#         blank=True
#     )
#        username = models.CharField(max_length=100)
#        email = models.EmailField()
#        password = models.CharField(max_length=100)
#        confirm_password = models.CharField(max_length=100)
   
# def __str__(self):
#         return self.name
# from  django.apps import apps




# users = User.objects.all()


# for user in users:
#     try:
#         candidate = CandidateProfile.objects.get(user=user)
#         print(f"{user.username} is a Candidate")
#     except CandidateProfile.DoesNotExist:
#         pass

#     try:
#         employee = EmployeeProfile.objects.get(user=user)
#         print(f"{user.username} is an Employee")
#     except EmployeeProfile.DoesNotExist:
#         pass


# users = User.objects.all()

# for user in users:
#     if hasattr(user, 'create_profile'):
#         print(f"{user.username} is a Candidate")
#     elif hasattr(user, 'emp_profile'):
#         print(f"{user.username} is an Employee")
#     else:
#         print(f"{user.username} has no profile")



# users = User.objects.all()

# for user in users:
#     try:
      
#         # Check if user has a CandidateProfile
#         candidate = CandidateProfile.objects.get(user=user)
#         print(f"{user.username} is a Candidate")
#     except CandidateProfile.DoesNotExist:
#         try:
#             # Check if user has an EmployeeProfile
#             employee = EmployeeProfile.objects.get(user=user)
#             print(f"{user.username} is an Employee")
#         except EmployeeProfile.DoesNotExist:
#             # If no profile is found
#             print(f"{user.username} has no profile")


# users = User.objects.all()

# for user in users:
#     try:
#         # Dynamically get CandidateProfile model
#         CandidateProfile = apps.get_model('pravahapp', 'CandidateProfile')
#         candidate = CandidateProfile.objects.get(user=user)
#         print(f"{user.username} is a Candidate")
#     except CandidateProfile.DoesNotExist:
#         try:
#             # Dynamically get EmployeeProfile model
#             EmployeeProfile = apps.get_model('pravahapp', 'EmployeeProfile')
#             employee = EmployeeProfile.objects.get(user=user)
#             print(f"{user.username} is an Employee")
#         except EmployeeProfile.DoesNotExist:
#             print(f"{user.username} has no profile")

class CandidateProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='candidate_profile',  null=False, default=1)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    dob = models.DateField()
    age = models.IntegerField()
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ]

    gender = models.CharField(
    max_length=10,
    choices=GENDER_CHOICES,
    default='F'
    )
    village = models.CharField(max_length=100, blank=True, null=True)
    taluka = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='India')
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class EmployeeProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile', null=False, blank=True, default=1)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phoneNo = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    company_website = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Education(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='education')

    degree = models.CharField(max_length=100)
    course_name= models.CharField(max_length=100, null=True, blank=True)
    college = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    year_of_passing = models.IntegerField()
    percentage = models.FloatField()
    skills = models.CharField(max_length=200)
    experience = models.CharField(max_length=100)
    interested_sector = models.CharField(max_length=100)
    

class SubmitCV(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='submitCV')
    cv_file = models.FileField(upload_to='cv_files/')
    date_submitted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('submitted', 'Submitted'), ('reviewed', 'Reviewed')], default='submitted')



    
   
def __str__(self):
     return self.name

class JobPostings(models.Model):
  
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    job_location = models.CharField(max_length=255)
    job_description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    employment_type = models.CharField(max_length=50, choices=[
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Internship', 'Internship'),
        ('Freelance', 'Freelance')
    ])
    application_deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    posted_by = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, null=True, blank=True)

   
    
    def __str__(self):
       return self.job_title



    
class Contact(models.Model):
     full_name = models.CharField(max_length=100)
     email = models.EmailField(max_length=100)
     subject = models.CharField(max_length=100)
     message = models.TextField()

     def __str__(self):
        return self.full_name

class JobApplication(models.Model):
    job = models.ForeignKey(JobPostings, on_delete=models.CASCADE, related_name='applications', null=True, blank=True)
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications', null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    cv_file = models.FileField(upload_to='cv_files/', null=True, blank=True)
    job_position = models.CharField(max_length=255)
    applied_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
    ('applied', 'Applied'),
    ('shortlisted', 'Shortlisted'),
    ('interview', 'Interview Scheduled'),
    ('rejected', 'Rejected'),
], default='applied')



    def __str__(self):
        return f"{self.full_name} - {self.job.job_title}"



