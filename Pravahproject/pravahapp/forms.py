from django import forms

from .models import EmployeeProfile
from .models import CandidateProfile

from .models import Education, SubmitCV

from django.core.exceptions import ValidationError
from .models import JobPostings

from .models import Contact
from .models import JobApplication

from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


import os

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



# class RegistrationForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password', 'role']  #
#         help_texts = {
#             'username': '',  # This removes the default help text
#         }# Add any fields you need

#     #If you need additional custom validation or fields:
#     password = forms.CharField(widget=forms.PasswordInput)
    
#     #Custom validation can also be added if needed
#     #forms.py

# class RegistrationForm(UserCreationForm):
#     role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

#     class Meta:
#         model = CustomUser
#         fields = ['username','email', 'password1', 'password2', 'role' ,'date_joined', 'registered_at']  
#         help_texts = {
#             'username': '',  # This removes the default help text
#         }# Add any fields you need
# class RegistrationForm(forms.ModelForm):
#     confirm_password = forms.CharField(widget=forms.PasswordInput)  # Add confirm_password field

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'role', 'password']

#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match.")
#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])  # Set the password
#         if commit:
#             user.save()
#         return user

 


# def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match.")
#         return cleaned_data

# def save(self):
#         # Create the user in the database
#         username = self.cleaned_data['username']
#         email = self.cleaned_data['email']
#         password = self.cleaned_data['password']

#         user = CustomUser.objects.create_user(username=username, email=email, password=password)
#         return user



# class CandidateRegistrationForm(forms.Form):
   
#     username = forms.CharField(max_length=100)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput())
#     confirm_password = forms.CharField(widget=forms.PasswordInput())

#     def clean(self):
#          cleaned_data = super().clean()
#          password = cleaned_data.get('password')
#          confirm_password = cleaned_data.get('confirm_password')

#          if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match.")
#          return cleaned_data

#     def save(self):
        
#          username = self.cleaned_data['username']
#          email = self.cleaned_data['email']
#          password = self.cleaned_data['password']

#          user = User.objects.create_user(username=username, email=email, password=password)
#          return user


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['name', 'email','phoneNo','company_name','designation' ,'location', 'sector', 'companywebsite']
        
    
class CandidateForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['name', 'email','contact','dob','age','gender','village', 'taluka', 'district', 'city', 'state', 'country', 'postal_code']  # Add fields you want to customize
          
        
        widgets = {
            'gender': forms.RadioSelect(attrs={'class':'gender-radio'}),  # Custom class for radio buttons
              # Radio buttons for gender
            'dob': forms.DateInput(attrs={'type': 'date'}),  # Date picker for date of birth

        }

# class EducationForm(forms.ModelForm):
#     class Meta:
#         model = Education
#         fields = ['degree', 'institution', 'year_of_passing', 'percentage', 'skills', 'experience', 'interestedsector', 'specialization', 'college']

#     # RadioButton choices for percentage
#     PERCENTAGE_CHOICES = [
#          ('Percentage', 'Percentage'),
#          ('CGPA', 'CGPA')
#     ]

#     percentage_type = forms.ChoiceField(choices=PERCENTAGE_CHOICES, widget=forms.Select(), label="Enter as", initial='Percentage')

#     def clean_percentage(self):
#         percentage_type = self.cleaned_data.get('percentage_type')
#         percentage_value = self.cleaned_data.get('percentage')

#         if percentage_type == 'Percentage':
#             if not (0 <= percentage_value <= 100):
#                 raise forms.ValidationError("Please enter a valid percentage between 0 and 100.")
#         elif percentage_type == 'CGPA':
#             if not (0 <= percentage_value <= 10):
#                 raise forms.ValidationError("Please enter a valid CGPA between 0 and 10.")
#         return percentage_value

#     # RadioButton choices for degree (with mandatory logic)
#     DEGREE_CHOICES = [
#         ('10th', '10th'),
#         ('12th', '12th'),
#         ('Degree', 'Degree')
#     ]

#     degree = forms.ChoiceField(choices=DEGREE_CHOICES, widget=forms.RadioSelect(), label="Degree Level")

#     # Custom validation for degree choice
#     def clean_degree(self):
#         degree = self.cleaned_data.get('degree')
#         if degree not in ['10th', '12th', 'Degree']:
#             raise forms.ValidationError("Please select a valid degree: 10th, 12th, or Degree.")
#         return degree
#     # RadioButton choices for skill type (Technical or Non-Technical)
#     SKILL_TYPE_CHOICES = [
#         ('technical', 'Technical'),
#         ('non_technical', 'Non-Technical')
#     ]

#     skill_type = forms.ChoiceField(choices=SKILL_TYPE_CHOICES, widget=forms.RadioSelect(), label="Choose Skill Category")

#     # Technical and Non-Technical Skills
#     technical_skills = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         choices=[
#             ('Python', 'Python'),
#             ('JavaScript', 'JavaScript'),
#             ('C++', 'C++'),
#             ('SQL', 'SQL'),
#             ('Java', 'Java'),
#             ('Django', 'Django'),
#             ('Ruby', 'Ruby'),
#             ('Go', 'Go'),
#             ('C#', 'C#'),
#             ('PHP', 'PHP'),
#             ('Swift', 'Swift'),
#             ('Kotlin', 'Kotlin'),
#             ('React', 'React'),
#             ('Angular', 'Angular'),
#             ('Node.js', 'Node.js'),
#             ('Vue.js', 'Vue.js'),
#             ('Docker', 'Docker'),
#             ('AWS', 'AWS'),
#             ('Azure', 'Azure'),
#             ('Git', 'Git'),
#             ('Linux', 'Linux'),
#             ('Machine Learning', 'Machine Learning'),
#             ('TensorFlow', 'TensorFlow'),
#             ('Deep Learning', 'Deep Learning'),
#             ('Data Science', 'Data Science'),
#             ('Others', 'Others')
#         ],
#         label="Technical Skills",
#         required=False
#     )

#     non_technical_skills = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         choices=[
#             ('Communication', 'Communication'),
#             ('Leadership', 'Leadership'),
#             ('Problem Solving', 'Problem Solving'),
#             ('Time Management', 'Time Management'),
#             ('Project Management', 'Project Management'),
#             ('Teamwork', 'Teamwork'),
#             ('Creativity', 'Creativity'),
#             ('Critical Thinking', 'Critical Thinking'),
#             ('Negotiation', 'Negotiation'),
#             ('Adaptability', 'Adaptability'),
#             ('Conflict Resolution', 'Conflict Resolution'),
#             ('Decision Making', 'Decision Making'),
#             ('Networking', 'Networking'),
#             ('Empathy', 'Empathy'),
#             ('Collaboration', 'Collaboration'),
#             ('Mentoring', 'Mentoring'),
#             ('Public Speaking', 'Public Speaking'),
#             ('Presentation Skills', 'Presentation Skills'),
#             ('Organizational Skills', 'Organizational Skills'),
#             ('Customer Service', 'Customer Service'),
#             ('Analytical Thinking', 'Analytical Thinking'),
#             ('Research', 'Research'),
#             ('Strategic Planning', 'Strategic Planning'),
#             ('Budgeting', 'Budgeting'),
#             ('Risk Management', 'Risk Management'),
#             ('Sales and Marketing', 'Sales and Marketing'),
#             ('Time Management', 'Time Management'),
#             ('Others', 'Others')
#         ],
#         label="Non-Technical Skills",
#         required=False
#     )

#     # Checkboxes for interested sectors
#     interestedsector = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         choices=[
#             ('Tech', 'Tech'),
#             ('Finance', 'Finance'),
#             ('Healthcare', 'Healthcare'),
#             ('Education', 'Education'),
#             ('Marketing', 'Marketing'),
#             ('Retail', 'Retail'),
#             ('Manufacturing', 'Manufacturing'),
#             ('Hospitality', 'Hospitality'),
#             ('Real Estate', 'Real Estate'),
#             ('Transportation', 'Transportation'),
#             ('Telecommunications', 'Telecommunications'),
#             ('Energy', 'Energy'),
#             ('Government', 'Government'),
#             ('Non-Profit', 'Non-Profit'),
#             ('Entertainment', 'Entertainment'),
#             ('Media', 'Media'),
#             ('Legal', 'Legal'),
#             ('Consulting', 'Consulting'),
#             ('Others', 'Others')
            
             
#         ],
#         label="Interested Sectors"
#     )


# class EducationForm(forms.ModelForm):
#     class Meta:
#         model = Education
#         fields = ['degree', 'institution', 'year_of_passing', 'percentage', 'skills', 'experience', 'interestedsector', 'specialization', 'college']

#     # RadioButton choices for percentage
#     PERCENTAGE_CHOICES = [
#          ('Percentage', 'Percentage'),
#          ('CGPA', 'CGPA')
#     ]

#     percentage_type = forms.ChoiceField(
#         choices=PERCENTAGE_CHOICES, 
#         widget=forms.Select(), 
#         label="Enter as", 
#         initial='Percentage'
#     )

#     def clean_percentage(self):
#         percentage_type = self.cleaned_data.get('percentage_type')
#         percentage_value = self.cleaned_data.get('percentage')

#         if percentage_value is None:
#             raise forms.ValidationError("This field is required.")

#         if percentage_type == 'Percentage':
#             if not (0 <= percentage_value <= 100):
#                 raise forms.ValidationError("Please enter a valid percentage between 0 and 100.")
#         elif percentage_type == 'CGPA':
#             if not (0 <= percentage_value <= 10):
#                 raise forms.ValidationError("Please enter a valid CGPA between 0 and 10.")
#         return percentage_value

#     # RadioButton choices for degree (with mandatory logic)
#     DEGREE_CHOICES = [
#         ('10th', '10th'),
#         ('12th', '12th'),
#         ('Degree', 'Degree')
#     ]

#     degree = forms.ChoiceField(
#         choices=DEGREE_CHOICES, 
#         widget=forms.RadioSelect(), 
#         label="Degree Level"
#     )

#     # Custom validation for degree choice
#     def clean_degree(self):
#         degree = self.cleaned_data.get('degree')
#         if degree not in ['10th', '12th', 'Degree']:
#             raise forms.ValidationError("Please select a valid degree: 10th, 12th, or Degree.")
#         return degree

#     # Skill Type: Technical or Non-Technical
#     SKILL_TYPE_CHOICES = [
#         ('technical', 'Technical'),
#         ('non_technical', 'Non-Technical')
#     ]

#     skill_type = forms.ChoiceField(
#         choices=SKILL_TYPE_CHOICES, 
#         widget=forms.RadioSelect(), 
#         label="Choose Skill Category"
#     )

#     # Dynamically show relevant skills based on skill type
#     technical_skills = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         choices=[
#             ('Python', 'Python'),
#             ('JavaScript', 'JavaScript'),
#             ('C++', 'C++'),
#             ('SQL', 'SQL'),
#             ('Java', 'Java'),
#             ('Django', 'Django'),
#             ('Ruby', 'Ruby'),
#             ('Go', 'Go'),
#             ('C#', 'C#'),
#             ('PHP', 'PHP'),
#             ('Swift', 'Swift'),
#             ('Kotlin', 'Kotlin'),
#             ('React', 'React'),
#             ('Angular', 'Angular'),
#             ('Node.js', 'Node.js'),
#             ('Vue.js', 'Vue.js'),
#             ('Docker', 'Docker'),
#             ('AWS', 'AWS'),
#             ('Azure', 'Azure'),
#             ('Git', 'Git'),
#             ('Linux', 'Linux'),
#             ('Machine Learning', 'Machine Learning'),
#             ('TensorFlow', 'TensorFlow'),
#             ('Deep Learning', 'Deep Learning'),
#             ('Data Science', 'Data Science'),
#             ('Others', 'Others')
#         ],
#         label="Technical Skills",
#         required=False
#     )

#     non_technical_skills = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         choices=[
#             ('Communication', 'Communication'),
#             ('Leadership', 'Leadership'),
#             ('Problem Solving', 'Problem Solving'),
#             ('Time Management', 'Time Management'),
#             ('Project Management', 'Project Management'),
#             ('Teamwork', 'Teamwork'),
#             ('Creativity', 'Creativity'),
#             ('Critical Thinking', 'Critical Thinking'),
#             ('Negotiation', 'Negotiation'),
#             ('Adaptability', 'Adaptability'),
#             ('Conflict Resolution', 'Conflict Resolution'),
#             ('Decision Making', 'Decision Making'),
#             ('Networking', 'Networking'),
#             ('Empathy', 'Empathy'),
#             ('Collaboration', 'Collaboration'),
#             ('Mentoring', 'Mentoring'),
#             ('Public Speaking', 'Public Speaking'),
#             ('Presentation Skills', 'Presentation Skills'),
#             ('Organizational Skills', 'Organizational Skills'),
#             ('Customer Service', 'Customer Service'),
#             ('Analytical Thinking', 'Analytical Thinking'),
#             ('Research', 'Research'),
#             ('Strategic Planning', 'Strategic Planning'),
#             ('Budgeting', 'Budgeting'),
#             ('Risk Management', 'Risk Management'),
#             ('Sales and Marketing', 'Sales and Marketing'),
#             ('Time Management', 'Time Management'),
#             ('Others', 'Others')
#         ],
#         label="Non-Technical Skills",
#         required=False
#     )

#     # Checkboxes for interested sectors
#     interestedsector = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         choices=[
#             ('Tech', 'Tech'),
#             ('Finance', 'Finance'),
#             ('Healthcare', 'Healthcare'),
#             ('Education', 'Education'),
#             ('Marketing', 'Marketing'),
#             ('Retail', 'Retail'),
#             ('Manufacturing', 'Manufacturing'),
#             ('Hospitality', 'Hospitality'),
#             ('Real Estate', 'Real Estate'),
#             ('Transportation', 'Transportation'),
#             ('Telecommunications', 'Telecommunications'),
#             ('Energy', 'Energy'),
#             ('Government', 'Government'),
#             ('Non-Profit', 'Non-Profit'),
#             ('Entertainment', 'Entertainment'),
#             ('Media', 'Media'),
#             ('Legal', 'Legal'),
#             ('Consulting', 'Consulting'),
#             ('Others', 'Others')
#         ],
#         label="Interested Sectors"
#     )

#     def clean(self):
#         cleaned_data = super().clean()

#         # Dynamically validate skills based on selected category
#         skill_type = cleaned_data.get('skill_type')

#         if skill_type == 'technical':
#             cleaned_data['skills'] = cleaned_data.get('technical_skills', [])
#         elif skill_type == 'non_technical':
#             cleaned_data['skills'] = cleaned_data.get('non_technical_skills', [])
        
#         return cleaned_data

# from django import forms

# class EducationForm(forms.ModelForm):
#     class Meta:
#         model = Education
#         fields = ['degree', 'institution', 'year_of_passing', 'percentage', 'skills', 'experience', 'interestedsector', 'specialization', 'college']

#     # RadioButton choices for percentage
#     PERCENTAGE_CHOICES = [
#         ('Percentage', 'Percentage'),
#         ('CGPA', 'CGPA')
#     ]

#     percentage_type = forms.ChoiceField(
#         choices=PERCENTAGE_CHOICES, 
#         widget=forms.Select(), 
#         label="Enter Percentage as", 
#         initial='Percentage',
#         help_text="Choose whether your percentage is in Percentage or CGPA format."
#     )

#     def clean_percentage(self):
#         percentage_type = self.cleaned_data.get('percentage_type')
#         percentage_value = self.cleaned_data.get('percentage')

#         if percentage_value is None:
#             raise forms.ValidationError("This field is required.")

#         # Validate based on selected percentage type
#         if percentage_type == 'Percentage':
#             if not (0 <= percentage_value <= 100):
#                 raise forms.ValidationError("Please enter a valid percentage between 0 and 100.")
#         elif percentage_type == 'CGPA':
#             if not (0 <= percentage_value <= 10):
#                 raise forms.ValidationError("Please enter a valid CGPA between 0 and 10.")
#         return percentage_value

#     # RadioButton choices for degree (with mandatory logic)
#     DEGREE_CHOICES = [
#         ('10th', '10th Grade'),
#         ('12th', '12th Grade'),
#         ('Undergraduate', 'Undergraduate Degree'),
#         ('Postgraduate', 'Postgraduate Degree')
#     ]

#     degree = forms.ChoiceField(
#         choices=DEGREE_CHOICES, 
#         widget=forms.RadioSelect(), 
#         label="Highest Degree Level",
#         help_text="Please select your highest level of education."
#     )

#     def clean_degree(self):
#         degree = self.cleaned_data.get('degree')
#         if degree not in ['10th', '12th', 'Undergraduate', 'Postgraduate']:
#             raise forms.ValidationError("Please select a valid degree: 10th, 12th, Undergraduate, or Postgraduate.")
#         return degree

#     # Skill Category Choices: Technical or Non-Technical
#     SKILL_TYPE_CHOICES = [
#         ('technical', 'Technical'),
#         ('non_technical', 'Non-Technical')
#     ]

#     skill_type = forms.ChoiceField(
#         choices=SKILL_TYPE_CHOICES, 
#         widget=forms.RadioSelect(), 
#         label="Choose Skill Category",
#         help_text="Choose between technical or non-technical skills."
#     )

#     # Technical Skills (if skill type is 'technical')
#     technical_skills = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         choices=[
#             ('Python', 'Python'),
#             ('JavaScript', 'JavaScript'),
#             ('C++', 'C++'),
#             ('SQL', 'SQL'),
#             ('Java', 'Java'),
#             ('Django', 'Django'),
#             ('Ruby', 'Ruby'),
#             ('Go', 'Go'),
#             ('C#', 'C#'),
#             ('PHP', 'PHP'),
#             ('Swift', 'Swift'),
#             ('Kotlin', 'Kotlin'),
#             ('React', 'React'),
#             ('Angular', 'Angular'),
#             ('Node.js', 'Node.js'),
#             ('Vue.js', 'Vue.js'),
#             ('Docker', 'Docker'),
#             ('AWS', 'AWS'),
#             ('Azure', 'Azure'),
#             ('Git', 'Git'),
#             ('Linux', 'Linux'),
#             ('Machine Learning', 'Machine Learning'),
#             ('TensorFlow', 'TensorFlow'),
#             ('Deep Learning', 'Deep Learning'),
#             ('Data Science', 'Data Science'),
#             ('Others', 'Others')
#         ],
#         label="Technical Skills",
#         required=False,
#         help_text="Select any technical skills you possess."
#     )

#     # Non-Technical Skills (if skill type is 'non_technical')
#     non_technical_skills = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         choices=[
#             ('Communication', 'Communication'),
#             ('Leadership', 'Leadership'),
#             ('Problem Solving', 'Problem Solving'),
#             ('Time Management', 'Time Management'),
#             ('Project Management', 'Project Management'),
#             ('Teamwork', 'Teamwork'),
#             ('Creativity', 'Creativity'),
#             ('Critical Thinking', 'Critical Thinking'),
#             ('Negotiation', 'Negotiation'),
#             ('Adaptability', 'Adaptability'),
#             ('Conflict Resolution', 'Conflict Resolution'),
#             ('Decision Making', 'Decision Making'),
#             ('Networking', 'Networking'),
#             ('Empathy', 'Empathy'),
#             ('Collaboration', 'Collaboration'),
#             ('Mentoring', 'Mentoring'),
#             ('Public Speaking', 'Public Speaking'),
#             ('Presentation Skills', 'Presentation Skills'),
#             ('Organizational Skills', 'Organizational Skills'),
#             ('Customer Service', 'Customer Service'),
#             ('Analytical Thinking', 'Analytical Thinking'),
#             ('Research', 'Research'),
#             ('Strategic Planning', 'Strategic Planning'),
#             ('Budgeting', 'Budgeting'),
#             ('Risk Management', 'Risk Management'),
#             ('Sales and Marketing', 'Sales and Marketing'),
#             ('Others', 'Others')
#         ],
#         label="Non-Technical Skills",
#         required=False,
#         help_text="Select any non-technical skills you possess."
#     )

#     # Interested Sectors (checkboxes for multiple selections)
#     interestedsector = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         choices=[
#             ('Tech', 'Tech'),
#             ('Finance', 'Finance'),
#             ('Healthcare', 'Healthcare'),
#             ('Education', 'Education'),
#             ('Marketing', 'Marketing'),
#             ('Retail', 'Retail'),
#             ('Manufacturing', 'Manufacturing'),
#             ('Hospitality', 'Hospitality'),
#             ('Real Estate', 'Real Estate'),
#             ('Transportation', 'Transportation'),
#             ('Telecommunications', 'Telecommunications'),
#             ('Energy', 'Energy'),
#             ('Government', 'Government'),
#             ('Non-Profit', 'Non-Profit'),
#             ('Entertainment', 'Entertainment'),
#             ('Media', 'Media'),
#             ('Legal', 'Legal'),
#             ('Consulting', 'Consulting'),
#             ('Others', 'Others')
#         ],
#         label="Interested Sectors",
#         help_text="Select the sectors you are interested in working with."
#     )

#     # Specialization / College Details (Optional)
#     specialization = forms.CharField(
#         max_length=100,
#         required=False,
#         label="Specialization (if any)",
#         widget=forms.TextInput(attrs={'placeholder': 'E.g., Computer Science, Finance, etc.'}),
#         help_text="Mention your specialization or area of focus (if applicable)."
#     )

#     college = forms.CharField(
#         max_length=100,
#         required=False,
#         label="College/University",
#         widget=forms.TextInput(attrs={'placeholder': 'Name of your College/University'}),
#         help_text="Enter the name of the college or university you attended."
#     )

#     # Custom form clean method to handle dynamic skills based on skill type selection
#     def clean(self):
#         cleaned_data = super().clean()

#         # Dynamically select the skills based on the selected skill category
#         skill_type = cleaned_data.get('skill_type')

#         if skill_type == 'technical':
#             cleaned_data['skills'] = cleaned_data.get('technical_skills', [])
#         elif skill_type == 'non_technical':
#             cleaned_data['skills'] = cleaned_data.get('non_technical_skills', [])
        
#         return cleaned_data





class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'college','coursename','specialization' ,'institution', 'year_of_passing', 'percentage_type','percentage',  'skills', 'experience', 'interestedsector']

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

#    # Skill Category Choices: Technical or Non-Technical
#     SKILL_TYPE_CHOICES = [
#         ('technical', 'Technical'),
#         ('non_technical', 'Non-Technical')
#     ]

#     skill_type = forms.ChoiceField(
#         choices=SKILL_TYPE_CHOICES, 
#         widget=forms.Select(),  # Dropdown for skill category
#         label="Choose Skill Category",
#         help_text="Choose between technical or non-technical skills."
#     )

#     # Interested Sectors (Dropdown with Checkboxes)
#     INTERESTED_SECTORS_CHOICES = [
#         ('Tech', 'Tech'),
#         ('Finance', 'Finance'),
#         ('Healthcare', 'Healthcare'),
#         ('Education', 'Education'),
#         ('Marketing', 'Marketing'),
#         ('Retail', 'Retail'),
#         ('Manufacturing', 'Manufacturing'),
#         ('Hospitality', 'Hospitality'),
#         ('Real Estate', 'Real Estate'),
#         ('Transportation', 'Transportation'),
#         ('Telecommunications', 'Telecommunications'),
#         ('Energy', 'Energy'),
#         ('Government', 'Government'),
#         ('Non-Profit', 'Non-Profit'),
#         ('Entertainment', 'Entertainment'),
#         ('Media', 'Media'),
#         ('Legal', 'Legal'),
#         ('Consulting', 'Consulting'),
#         ('Others', 'Others')
#     ]

#     interestedsector = forms.MultipleChoiceField(
#         choices=INTERESTED_SECTORS_CHOICES,
#         widget=forms.SelectMultiple(attrs={
#             'class': 'dropdown-checkboxes',
#         }),
#         label="Interested Sectors",
#         help_text="Select the sectors you are interested in working with."
#     )

#     # Technical Skills (Dropdown with Checkboxes)
#     TECHNICAL_SKILLS_CHOICES = [
#         ('Python', 'Python'),
#         ('JavaScript', 'JavaScript'),
#         ('C++', 'C++'),
#         ('SQL', 'SQL'),
#         ('Java', 'Java'),
#         ('Django', 'Django'),
#         ('Ruby', 'Ruby'),
#         ('Go', 'Go'),
#         ('C#', 'C#'),
#         ('PHP', 'PHP'),
#         ('Swift', 'Swift'),
#         ('Kotlin', 'Kotlin'),
#         ('React', 'React'),
#         ('Angular', 'Angular'),
#         ('Node.js', 'Node.js'),
#         ('Vue.js', 'Vue.js'),
#         ('Docker', 'Docker'),
#         ('AWS', 'AWS'),
#         ('Azure', 'Azure'),
#         ('Git', 'Git'),
#         ('Linux', 'Linux'),
#         ('Machine Learning', 'Machine Learning'),
#         ('TensorFlow', 'TensorFlow'),
#         ('Deep Learning', 'Deep Learning'),
#         ('Data Science', 'Data Science'),
#         ('Others', 'Others')
#     ]

#     technical_skills = forms.MultipleChoiceField(
#         choices=TECHNICAL_SKILLS_CHOICES,
#         widget=forms.SelectMultiple(attrs={
#             'class': 'dropdown-checkboxes',
#         }),
#         label="Technical Skills",
#         required=False,
#         help_text="Select any technical skills you possess."
#     )

#     # Non-Technical Skills (Dropdown with Checkboxes)
#     NON_TECHNICAL_SKILLS_CHOICES = [
#         ('Communication', 'Communication'),
#         ('Leadership', 'Leadership'),
#         ('Problem Solving', 'Problem Solving'),
#         ('Time Management', 'Time Management'),
#         ('Project Management', 'Project Management'),
#         ('Teamwork', 'Teamwork'),
#         ('Creativity', 'Creativity'),
#         ('Critical Thinking', 'Critical Thinking'),
#         ('Negotiation', 'Negotiation'),
#         ('Adaptability', 'Adaptability'),
#         ('Conflict Resolution', 'Conflict Resolution'),
#         ('Decision Making', 'Decision Making'),
#         ('Networking', 'Networking'),
#         ('Empathy', 'Empathy'),
#         ('Collaboration', 'Collaboration'),
#         ('Mentoring', 'Mentoring'),
#         ('Public Speaking', 'Public Speaking'),
#         ('Presentation Skills', 'Presentation Skills'),
#         ('Organizational Skills', 'Organizational Skills'),
#         ('Customer Service', 'Customer Service'),
#         ('Analytical Thinking', 'Analytical Thinking'),
#         ('Research', 'Research'),
#         ('Strategic Planning', 'Strategic Planning'),
#         ('Budgeting', 'Budgeting'),
#         ('Risk Management', 'Risk Management'),
#         ('Sales and Marketing', 'Sales and Marketing'),
#         ('Others', 'Others')
#     ]

#     non_technical_skills = forms.MultipleChoiceField(
#         choices=NON_TECHNICAL_SKILLS_CHOICES,
#         widget=forms.SelectMultiple(attrs={
#             'class': 'dropdown-checkboxes',
#         }),
#         label="Non-Technical Skills",
#         required=False,
#         # help_text="Select any non-technical skills you possess."
#     )

    # Specialization / College Details (Optional)
    specialization = forms.CharField(
        max_length=100,
        required=False,
        label="Specialization (if any)",
        widget=forms.TextInput(attrs={'placeholder': 'E.g., Computer Science, Finance, etc.'}),
        # help_text="Mention your specialization or area of focus (if applicable)."
    )

    college = forms.CharField(
        max_length=100,
        required=False,
        label="College/University",
        widget=forms.TextInput(attrs={'placeholder': 'Name of your College/University'}),
        # help_text="Enter the name of the college or university you attended."
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
    class Meta:
      model = JobPostings  

      fields = ['job_title', 'company_name', 'job_location', 'job_description', 'salary', 'employment_type', 'application_deadline']

      application_deadline=forms.DateField(
           
        widget=forms.DateInput(attrs={
              
            'type':'date'
              
              
        }, 
        format='%Y-%m-%d'),
        required=False
    )

       
           
# class JobInquiryForm(forms.ModelForm):
#     class Meta:
#       model = JobInquiry
#       fields = ['full_name', 'email', 'phone_number', 'role', 'message', 'resume']
#       widgets = {
#             'phone_number': forms.TextInput(attrs={'placeholder': 'Your phone number', 'pattern': r'\d{10}'}),
#             'message': forms.Textarea(attrs={'placeholder': 'Type your message here...'}),
#             'resume': forms.ClearableFileInput(attrs={'accept': 'application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document'})
#         }
# def clean_phone_number(self):
#         phone_number = self.cleaned_data.get('phone_number')
#         if len(phone_number) != 10:  # Check for exactly 10 digits
#             raise ValidationError("Phone number must be 10 digits.")
#         return phone_number

# def clean_resume(self):
#         resume = self.cleaned_data.get('resume')
#         if resume:
#             # File size validation (e.g., 5 MB max)
#             max_size = 5 * 1024 * 1024  # 5 MB
#             if resume.size > max_size:
#                 raise ValidationError("Resume file size must be less than 5MB.")
#         return resume


class ContactForm(forms.ModelForm):
    class Meta:
      model = Contact
      fields =['full_name', 'email','subject','message']

      message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your message',
            'style': 'height: 150px'
        }),
        label="Message"
      )



class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone_number', 'resume', 'job_position']
