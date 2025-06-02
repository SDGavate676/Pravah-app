from django.contrib import admin


# from  .models import Employee
# from  .models import Candidate


from  .models import EmployeeProfile
from .models import CandidateProfile

from .models import Education
from .models import SubmitCV

from .models import JobPostings
from .models import Contact

from .models import JobApplication

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active', 'registered_at']
    search_fields = ['username', 'email']
    list_filter = ['role', 'is_active', 'is_staff', 'registered_at']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)


# Register your models here.
def register(model):
    admin.site.register(model)

  


# from django.contrib.auth import get_user_model

# User = get_user_model()

# admin.site.register(User)

# class EmployeeAdmin(admin.ModelAdmin):
#     model = Employee

# admin.site.register(Employee)

# class CandidateAdmin(admin.ModelAdmin):
#     model = Candidate

# admin.site.register(Candidate)
 

class EmployeeAdmin(admin.ModelAdmin):
    model = EmployeeProfile

admin.site.register(EmployeeProfile)

class CandidateAdmin(admin.ModelAdmin):
   model =  CandidateProfile
 


admin.site.register(CandidateProfile)



class EducationAdmin(admin.ModelAdmin):
    model = Education

admin.site.register(Education)  

class SubmitCVAdmin(admin.ModelAdmin):
    model = SubmitCV

admin.site.register(SubmitCV)

class JobPostingsAdmin(admin.ModelAdmin):
    model = JobPostings

admin.site.register(JobPostings)

class ContactAdmin(admin.ModelAdmin):
    model = Contact
admin.site.register(Contact)

class jobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication
admin.site.register(JobApplication)