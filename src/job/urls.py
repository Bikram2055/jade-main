from django.urls import path

from src.job import views

urlpatterns = [
    path("update/<int:pk>", views.JobUpdate.as_view()),
    path("", views.JobApi.as_view()),
    path("no-of-jobs/", views.Number_Of_JObs.as_view()),
    path("categorywise-jobcount/", views.Job_Count_Category.as_view()),
    path("job-age/<int:id>", views.JobAge.as_view()),
    path("search/", views.SearchJob.as_view()),
    path("bid/", views.BidCreateApi.as_view()),
    path("bid-update/", views.BidUpdateApi.as_view()),
    path("shotlist/<int:pk>", views.ShortlistApi.as_view()),
    path("bids-per-job/", views.BidsPerJob.as_view()),
    path("project/", views.ProjectApi.as_view()),
]
