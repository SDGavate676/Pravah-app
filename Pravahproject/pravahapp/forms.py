from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import EmployeeProfile
from .models import CandidateProfile

from .models import Education, SubmitCV

from django.core.exceptions import ValidationError
from .models import JobPostings

from .models import Contact
from .models import JobApplication

from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils import timezone

import os

class AdminRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email','password', 'confirm_password');  

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and len(username) < 3:
            raise ValidationError('Username must be at least 3 characters long.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        if password and len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hashing manually
        user.is_staff = True
        user.is_superuser = True
        user.role = 'admin'  # Make sure 'admin' is a valid choice
        if commit:
            user.save()
        return user



    
class AdminLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES,  widget=forms.RadioSelect,required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'role']
        help_texts = {
            'username': '',
        }
         
      


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and len(username) < 3:
            raise ValidationError('Username must be at least 3 characters long.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # ✅ hashes the password
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class EmployeeForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}),
        validators=[RegexValidator(
            regex=r'^[\w\s-]+$',
            message='Name can only contain letters, spaces, and hyphens.',
            code='invalid_name'
        )]
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}), 
        validators=[RegexValidator(
            regex=r'^[\w\.-]+@[\w\.-]+\.\w+$',
            message='Enter a valid email address.',
            code='invalid_email'
        )]
    )
    company_name = forms.CharField( 
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your company name'}),       
        validators=[RegexValidator(
            regex=r'^[\w\s-]+$',
            message='Company name can only contain letters, digits, spaces, and hyphens.',
            code='invalid_company_name'
        )]  
    )
    designation = forms.CharField(
        max_length=100,     
        widget=forms.TextInput(attrs={'placeholder': 'Enter your designation'}),
        validators=[RegexValidator(
            regex=r'^[\w\s-]+$',
            message='Designation can only contain letters, spaces, and hyphens.',
            code='invalid_designation'
        )]  

    )

    location = forms.CharField(
        max_length=100,     
        widget=forms.TextInput(attrs={'placeholder': 'Enter your location'}),
        validators=[RegexValidator( 
            regex=r'^[\w\s-]+$',
            message='Location can only contain letters, spaces, and hyphens.',
            code='invalid_location'
        )]
    )

    sector = forms.CharField(
        max_length=100,     
        widget=forms.TextInput(attrs={'placeholder': 'Enter your sector'}),     
        validators=[RegexValidator(
            regex=r'^[\w\s-]+$',
            message='Sector can only contain letters, spaces, and hyphens.',
            code='invalid_sector'
        )]
    )
        

    phoneNo = forms.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\+?1?\d{10}$', 'Enter a valid phone number.')],
    )
     

    class Meta:
        model = EmployeeProfile
        fields = ['name', 'email','phoneNo','company_name','designation' ,'location', 'sector', 'company_website']
        
    
class CandidateForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=CandidateProfile.GENDER_CHOICES,  widget=forms.RadioSelect,required=True)
    class Meta:
        model = CandidateProfile
        fields = ['name', 'email','contact','dob','age','gender','village', 'taluka', 'district', 'city', 'state', 'country', 'postal_code']  # Add fields you want to customize
          
       
        widgets = {
            
              # Radio buttons for gender
            'dob': forms.DateInput(attrs={'type': 'date'}),  # Date picker for date of birth

        }





class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'college','course_name','specialization' ,'institution', 'year_of_passing', 'percentage_type','percentage',  'skills', 'experience', 'interested_sector']

    # RadioButton choices for percentage type
    PERCENTAGE_CHOICES = [
        ('Percentage', 'Percentage'),
        ('CGPA', 'CGPA')
    ]

    percentage_type = forms.ChoiceField(
        choices=PERCENTAGE_CHOICES, 
        widget=forms.Select(), 
        label="Enter Score As", 
        initial='Percentage',
        # help_text="Choose whether your score is in Percentage or CGPA format."
    )

    percentage = forms.DecimalField(
        max_digits=5, 
        decimal_places=2,
        label="Percentage/CGPA",
        # help_text="Enter your percentage or CGPA (depending on the option selected above)."
    )

    def clean_percentage(self):
        percentage_type = self.cleaned_data.get('percentage_type')
        percentage_value = self.cleaned_data.get('percentage')

        # If percentage_type is 'Percentage', validate between 0 and 100
        if percentage_type == 'Percentage':
            if not (0 <= percentage_value <= 100):
                raise forms.ValidationError("Please enter a valid percentage between 0 and 100.")
        # If percentage_type is 'CGPA', validate between 0 and 10
        elif percentage_type == 'CGPA':
            if not (0 <= percentage_value <= 10):
                raise forms.ValidationError("Please enter a valid CGPA between 0 and 10.")
        return percentage_value

    # RadioButton choices for degree (with mandatory logic)
    DEGREE_CHOICES = [
        ('10th', '10th Grade'),
        ('12th', '12th Grade'),
        ('Undergraduate', 'Undergraduate Degree'),
        ('Postgraduate', 'Postgraduate Degree')
    ]

    degree = forms.ChoiceField(
        choices=DEGREE_CHOICES, 
        widget=forms.RadioSelect(), 
        label="Highest Degree Level",
        # help_text="Please select your highest level of education."
    )

    def clean_degree(self):
        degree = self.cleaned_data.get('degree')
        if degree not in ['10th', '12th', 'Undergraduate', 'Postgraduate']:
            raise forms.ValidationError("Please select a valid degree: 10th, 12th, Undergraduate, or Postgraduate.")
        return degree

    # Skill Category Choices: Technical or Non-Technical
    SKILL_TYPE_CHOICES = [
        ('technical', 'Technical'),
        ('non_technical', 'Non-Technical')
    ]

    skill_type = forms.ChoiceField(
        choices=SKILL_TYPE_CHOICES, 
        widget=forms.RadioSelect(), 
        label="Choose Skill Category",
        help_text="Choose between technical or non-technical skills."
    )

    # Technical Skills (if skill type is 'technical')
    technical_skills = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[
            ('Python', 'Python'),
            ('JavaScript', 'JavaScript'),
            ('C++', 'C++'),
            ('SQL', 'SQL'),
            ('Java', 'Java'),
            ('Django', 'Django'),
            ('Ruby', 'Ruby'),
            ('Go', 'Go'),
            ('C#', 'C#'),
            ('PHP', 'PHP'),
            ('Swift', 'Swift'),
            ('Kotlin', 'Kotlin'),
            ('React', 'React'),
            ('Angular', 'Angular'),
            ('Node.js', 'Node.js'),
            ('Vue.js', 'Vue.js'),
            ('Docker', 'Docker'),
            ('AWS', 'AWS'),
            ('Azure', 'Azure'),
            ('Git', 'Git'),
            ('Linux', 'Linux'),
            ('Machine Learning', 'Machine Learning'),
            ('TensorFlow', 'TensorFlow'),
            ('Deep Learning', 'Deep Learning'),
            ('Data Science', 'Data Science'),
            ('Others', 'Others')
        ],
        label="Technical Skills",
        required=False,
        # help_text="Select any technical skills you possess."
    )

    # Non-Technical Skills (if skill type is 'non_technical')
    non_technical_skills = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[
            ('Communication', 'Communication'),
            ('Leadership', 'Leadership'),
            ('Problem Solving', 'Problem Solving'),
            ('Time Management', 'Time Management'),
            ('Project Management', 'Project Management'),
            ('Teamwork', 'Teamwork'),
            ('Creativity', 'Creativity'),
            ('Critical Thinking', 'Critical Thinking'),
            ('Negotiation', 'Negotiation'),
            ('Adaptability', 'Adaptability'),
            ('Conflict Resolution', 'Conflict Resolution'),
            ('Decision Making', 'Decision Making'),
            ('Networking', 'Networking'),
            ('Empathy', 'Empathy'),
            ('Collaboration', 'Collaboration'),
            ('Mentoring', 'Mentoring'),
            ('Public Speaking', 'Public Speaking'),
            ('Presentation Skills', 'Presentation Skills'),
            ('Organizational Skills', 'Organizational Skills'),
            ('Customer Service', 'Customer Service'),
            ('Analytical Thinking', 'Analytical Thinking'),
            ('Research', 'Research'),
            ('Strategic Planning', 'Strategic Planning'),
            ('Budgeting', 'Budgeting'),
            ('Risk Management', 'Risk Management'),
            ('Sales and Marketing', 'Sales and Marketing'),
            ('Others', 'Others')
        ],
        label="Non-Technical Skills",
        required=False,
        # help_text="Select any non-technical skills you possess."
    )

    # Interested Sectors (checkboxes for multiple selections)
    interestedsector = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[
            ('Tech', 'Tech'),
            ('Finance', 'Finance'),
            ('Healthcare', 'Healthcare'),
            ('Education', 'Education'),
            ('Marketing', 'Marketing'),
            ('Retail', 'Retail'),
            ('Manufacturing', 'Manufacturing'),
            ('Hospitality', 'Hospitality'),
            ('Real Estate', 'Real Estate'),
            ('Transportation', 'Transportation'),
            ('Telecommunications', 'Telecommunications'),
            ('Energy', 'Energy'),
            ('Government', 'Government'),
            ('Non-Profit', 'Non-Profit'),
            ('Entertainment', 'Entertainment'),
            ('Media', 'Media'),
            ('Legal', 'Legal'),
            ('Consulting', 'Consulting'),
            ('Others', 'Others')
        ],
        label="Interested Sectors",
        # help_text="Select the sectors you are interested in working with."
    )


    # Specialization / College Details (Optional)
    specialization = forms.CharField(
        max_length=100,
        required=False,
        label="Specialization (if any)",
        widget=forms.TextInput(attrs={'placeholder': 'E.g., Computer Science, Finance, etc.'}),
        validators=[RegexValidator(
            regex=r'^[\w\s-]+$',
            message='Specialization can only contain letters, spaces, and hyphens.',
            code='invalid_specialization'
        )],
        
    )

    college = forms.CharField(
        max_length=100,
        required=False,
        label="College/University",
        widget=forms.TextInput(attrs={'placeholder': 'Name of your College/University'}),
        help_text="Enter the name of the college or university you attended."
    )

    # Custom form clean method to handle dynamic skills based on skill type selection
    def clean(self):
        cleaned_data = super().clean()

        # Dynamically select the skills based on the selected skill category
        skill_type = cleaned_data.get('skill_type')

        if skill_type == 'technical':
            cleaned_data['skills'] = cleaned_data.get('technical_skills', [])
        elif skill_type == 'non_technical':
            cleaned_data['skills'] = cleaned_data.get('non_technical_skills', [])
        
        return cleaned_data



class SubmitCVForm(forms.ModelForm):
    class Meta:
        model = SubmitCV
        fields = ['cv_file']  # Include the file field for CV submission

    def clean_cv_file(self):
        cv_file = self.cleaned_data.get('cv_file')
        if not cv_file.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")
        return cv_file


class JobPostingForm(forms.ModelForm):
    job_title = forms.CharField(
        max_length=200,     
        widget=forms.TextInput(attrs={  
            'class': 'form-control',
            'placeholder': 'Enter job title',
        }), 
        validators=[RegexValidator(
            regex=r'^[\w\s-]+$',
            message='Job title can only contain letters, spaces, and hyphens.',
            code='invalid_job_title'
        )]

    )   

    company_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter company name',
        }),     
        validators=[RegexValidator( 
            regex=r'^[\w\s-]+$',
            message='Company name can only contain letters, digits, spaces, and hyphens.',
            code='invalid_company_name'
        )] 
    )


    class Meta:
      model = JobPostings 
      exclude = ['posted_by']  

      fields = ['job_title', 'company_name', 'job_location', 'job_description', 'salary', 'employment_type', 'application_deadline']

      widgets = {
            'job_description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width:100%; min-height:150px; resize:vertical;',
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter salary in INR',
            }),

            'job_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job location',
            }),

            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title',
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name',
            }),

            'employment_type': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select employment type',
            }),
            
             


        }

    


  


    application_deadline = forms.DateField(
       widget=forms.DateInput(attrs={
        'type': 'date',
        'placeholder': 'YYYY-MM-DD'  # or 'Select deadline'
    }, format='%Y-%m-%d'),
    required=False,
    input_formats=['%Y-%m-%d']
)
    
    def clean_application_deadline(self):
        date = self.cleaned_data.get('application_deadline')
        if date:
            if date < timezone.now().date():
                raise forms.ValidationError("Application deadline cannot be in the past.")
        return date
       
           


class ContactForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Your Full Name'}),
        label="Full Name",
        validators=[
        RegexValidator(
            regex=r'^[A-Za-z ]+$',
            message='Only alphabets and spaces are allowed.',
            code='invalid_fullname'
            )
        ]
    )
 

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Your Email Address'})
    )

    subject = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Subject of your message'})
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'maxlength': 800,
            'placeholder': 'Your message',
            'style': 'height: 150px',
            'class': 'form-control'
        }),
        label="Message"
    )

    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'subject', 'message']


class JobApplicationForm(forms.ModelForm):
   

    phone_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Phone Number',
            'pattern': r'\d{10}',
            'title': 'Enter a 10-digit phone number'
        }),
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number.')]
    )
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone_number', 'cv_file', 'job_position']
    widgets = {
        'full_name': forms.TextInput(attrs={'placeholder': 'Your Full Name'}),
        'email': forms.EmailInput(attrs={'placeholder': 'Your Email Address'}),
        'phone_number': forms.TextInput(attrs={'placeholder': 'Your Phone Number','pattern': r'\d{10}'}),
        'job_position': forms.Select(attrs={'class': 'form-control'}),
        'cv_file': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'})
    }

    
def clean_cv_file(self):
    cv_file = self.cleaned_data.get('cv_file')
    if not cv_file.name.endswith('.pdf'):
        raise forms.ValidationError("Only PDF files are allowed.")
    return cv_file


