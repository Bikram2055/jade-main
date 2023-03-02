from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from src.common.permissions import IsEmployer
from src.employer.models import Employer
from src.employer.serializers import EmployerSerializer
from src.job.models import Job, Rating
from src.job.serializers import JobSerializer, RateSerializer
from src.users.models import Address
from src.users.serializers import AddressSerializer

# Create your views here.


class EmployerApi(generics.ListCreateAPIView):
    """This is a Django class-based view for handling the creation and retrieval of
    "Employer" objects. The view is using Django Rest Framework's generics.ListCreateAPIView class,
     which provides the ability to list and create instances of a model.
    """

    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [permissions.AllowAny]


class EmployerUpdate(generics.RetrieveUpdateDestroyAPIView):
    """This is a Django class-based view for handling updates to an "Employer" model. The view is
    using Django Rest Framework's generics.RetrieveUpdateDestroyAPIView class, which provides the
     ability to retrieve, update, and delete a single instance of a model.
    """

    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class Number_Of_Employers(APIView):
    """
    View to list all users in the system.
    """

    def get(self, request):
        """
        Return a list of all users.
        """
        no_of_employers = Employer.objects.all().count()
        return Response({"employers count": no_of_employers})


class RateApi(generics.ListCreateAPIView):
    """This is an example of a Django REST Framework (DRF) view that inherits from generics.ListCreateAPIView.

    The ListCreateAPIView class is a generic view that provides both list and create functionalities for a model.
    In this case, the RateApi view is designed to work with the Rating model.

    The queryset attribute specifies the queryset of Rating objects to be used in the view. In this case,
    it's set to Rating.objects.all(), which will return all Rating objects.

    The serializer_class attribute specifies the serializer to be used to convert Rating objects to and from
    JSON format. In this case, it's set to RateSerializer, which is a custom serializer defined elsewhere in
    the codebase.

    The permission_classes attribute specifies the permission classes that will be used to check if a user has
    permission to access this view. In this case, it's set to IsEmployer, which is a custom permission class
    that checks if the user making the request is an employer.
    """

    queryset = Rating.objects.all()
    serializer_class = RateSerializer
    permission_classes = [
        IsEmployer,
    ]


class DraftJob(LoginRequiredMixin, generics.ListAPIView):

    queryset = Job.objects.filter(is_draft=True)
    serializer_class = JobSerializer
    permission_classes = [IsEmployer]


class EmployerAddress(APIView):
    def get(self, request, id):

        data = Employer.objects.get(id=id)
        data = Address.objects.filter(user=data.user)
        serializer = AddressSerializer(data=data, many=True)
        if serializer.is_valid():
            pass
        return Response(serializer.data)
