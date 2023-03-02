from rest_framework import permissions

from src.employer.models import Employer
from src.job_seeker.models import Job_Seeker


class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):

        if Employer.objects.filter(user=request.user).exists():
            return True
        return False


class IsJobSeeker(permissions.BasePermission):
    def has_permission(self, request, view):

        if Job_Seeker.objects.filter(user=request.user).exists():
            return True
        return False
