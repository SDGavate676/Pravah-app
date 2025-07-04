from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('admin_register/', views.admin_register, name='admin_register'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard_search/', views.dashboard_search, name='dashboard_search'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('user_logout/', views.user_logout, name='logout'),
    # path('empregistration/', views.empregistration, name='empregistration'),
    # path('emplogin/', views.emplogin, name='emplogin'),
    # path('emplogout/', views.emplogout, name='emplogout'),
    path('emp_profile/', views.emp_profile, name='emp_profile'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('profile_success/', views.profile_success, name='profile_success'), 
    path('profile_successcandidate/', views.profile_successcandidate, name='profile_successcandidate'), 
    path('educationdetail/', views.educationdetail, name='educationdetail'),
    path('submitcv/', views.submitcv, name='submitcv'),
    path('', views.index, name='index'),
   
    path('about/', views.about, name='about'),
    path('ourservices/', views.ourservices, name='ourservices'),
    path('service/', views.service, name='service'),
    path('features/', views.features, name='features'),
    path('jobpostings/', views.jobpostings, name='jobpostings'),
    path('unautorized/', views.unauthorized, name='unauthorized'),
    path('contact/', views.contact, name='contact'), 
    path("thank_you/", views.thank_you, name="thank_you"),

    path('joblist/', views.joblist, name='joblist'),
    path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('success_page/', views.success_page, name='success_page'),

    path('job-applications/', views.job_application_list, name='job_application_list'),

    path('submit_cv', views.candidate_resume_list, name='candidate_resume_list'),

    path('contact_detail', views.contact_detail_list, name='contact_detail_list'),
    path('user_detail', views.user_detail_list, name='user_detail_list'),
    path('candidate_detail',views.candidate_detail_list, name='candidate_detail_list'),
    path('employee_detail',views.employee_detail_list, name='employee_detail_list'),
    path('candidate_education', views.candidate_education_list, name='candidate_education_list'),
    path('jobposting_detail', views.jobposting_detail_list, name='jobposting_detail_list'),
    path('delete_candidate/<int:pk>/', views.delete_candidate, name='delete_candidate'),
    path('delete_employee/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('add_job/', views.add_job, name='add_job'),
    path('update_job/<int:id>/', views.update_job, name='update_job'),
    path('delete_job/<int:id>/', views.delete_job, name='delete_job'),
    path('delete_users/<int:id>/', views.delete_users, name='delete_users'),
    path('delete_apply_candidate/<int:pk>/', views.delete_apply_candidate, name='delete_apply_candidate'),
    path('delete_contact_detail/<int:pk>/', views.delete_contact_detail, name='delete_contact_detail'),
    path('candidate_dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('emp-dashboard/', views.emp_dashboard, name='emp_dashboard'),
    path('candi_dashboard/', views.candi_dashboard, name='candi_dashboard'),
    path('check/', views.check, name='check'),
    path('jobedit/<int:id>/', views.job_edit_view, name='jobedit'),
    path('jobdelete/<int:id>/', views.job_delete_view, name='jobdelete'),
    path('view-applicants/', views.view_applicants, name='view_applicants'),





 
]