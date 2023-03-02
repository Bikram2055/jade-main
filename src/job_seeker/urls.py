from django.urls import path

from src.job_seeker import views

urlpatterns = [
    path("", views.Seekers.as_view()),
    path("update/<int:pk>", views.SeekerUpdate.as_view()),
    path("skills/", views.SeekerSkill.as_view(), name="add-skills"),
    path("skill-update/<int:pk>", views.SeekerSkillUpdate.as_view(), name="update-skills"),
    path("no-of-jobseekers/", views.Number_Of_Job_seekers.as_view()),
    path("projects/<int:id>", views.ProjectsApi.as_view()),
    path("address/<int:id>", views.EmployeeAddress.as_view()),
    path("search-emp-address/", views.LocationSearch.as_view()),
]
