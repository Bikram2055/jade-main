from rest_framework import filters, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from src.job.models import Project
from src.job.serializers import ProjectSerializer
from src.job_seeker.models import Job_Seeker, Skill
from src.job_seeker.serializers import Job_SeekerSerializer, SeekerSkillSerializer
from src.users.models import Address
from src.users.serializers import AddressSerializer

# from src.users.models import User

# Create your views here.


class Seekers(generics.ListCreateAPIView):
    """This is a Django class-based view for handling the creation and retrieval of "Job Seeker" objects.
     The view is using Django Rest Framework's generics.ListCreateAPIView class, which provides the ability
      to list and create instances of a model.

    The queryset attribute specifies the set of objects that the view should operate on and it is set to
    Job_Seeker.objects.all(), meaning that it will operate on all objects of the Job_Seeker model.

    The serializer_class attribute specifies the serializer class that should be used to serialize the
    data for the view. It is set to Job_SeekerSerializer.

    The permission_classes attribute specifies the permission classes that should be applied to the view.
    It is set to [permissions.AllowAny], meaning that the view is accessible to anyone, including
    unauthenticated users."""

    queryset = Job_Seeker.objects.all()
    serializer_class = Job_SeekerSerializer
    permission_classes = [permissions.AllowAny]


class SeekerUpdate(generics.RetrieveUpdateDestroyAPIView):
    """This is a class-based view in Django Rest Framework (DRF) using the RetrieveUpdateDestroyAPIView
     class from the generics module. It defines a view for updating a Job_Seeker instance.

    The queryset attribute specifies the queryset that the view will use to retrieve the Job_Seeker instance
     to be updated. It is set to Job_Seeker.objects.all(), meaning that the view will retrieve all Job_Seeker
      instances.

    The serializer_class attribute specifies the serializer that will be used to serialize and deserialize
     the data. In this case, it is set to Job_SeekerSerializer.

    The permission_classes attribute specifies the permissions that must be satisfied in order to access
     this view. In this case, it is set to [permissions.IsAuthenticatedOrReadOnly], meaning that either the
      user must be authenticated, or the request method must be a safe method such as GET (read-only).
    """

    queryset = Job_Seeker.objects.all()
    serializer_class = Job_SeekerSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class SeekerSkillUpdate(generics.RetrieveUpdateDestroyAPIView):
    """This is a Django class-based view for handling updates to the "Skill" model for seekers.
     The view is using Django Rest Framework's generics.RetrieveUpdateDestroyAPIView class, which
      provides the ability to retrieve, update, and delete a single instance of a model.

    The queryset attribute specifies the set of objects that the view should operate on and it is
    set to Skill.objects.all(), meaning that it will operate on all objects of the Skill model.

    The serializer_class attribute specifies the serializer class that should be used to serialize
    the data for the view. It is set to SeekerSkillSerializer. This means that the view is using a
    custom serializer class for the Skill model specifically for seekers."""

    queryset = Skill.objects.all()
    serializer_class = SeekerSkillSerializer


class SeekerSkill(generics.ListCreateAPIView):
    """This is a Django class-based view for handling the creation and retrieval of "Skill" objects
     for seekers. The view is using Django Rest Framework's generics.ListCreateAPIView class, which
      provides the ability to list and create instances of a model.

    The queryset attribute specifies the set of objects that the view should operate on and it is set to
    Skill.objects.all(), meaning that it will operate on all objects of the Skill model.

    The serializer_class attribute specifies the serializer class that should be used to serialize the data
    for the view. It is set to SeekerSkillSerializer. This means that the view is using a custom serializer
    class for the Skill model specifically for seekers.
    """

    queryset = Skill.objects.all()
    serializer_class = SeekerSkillSerializer


class Number_Of_Job_seekers(APIView):
    """
    View to list all users in the system.
    """

    def get(self, request):
        """
        Return a list of all users.
        """
        no_of_job_seekers = Job_Seeker.objects.all().count()
        return Response({"Job_seekers count": no_of_job_seekers})


class ProjectsApi(APIView):
    def get(self, request, id):
        data = Project.objects.filter(job_seeker=id)
        serializer = ProjectSerializer(data=data, many=True)
        if serializer.is_valid():
            pass
        return Response(serializer.data)


class EmployeeAddress(APIView):
    def get(self, request, id):

        data = Job_Seeker.objects.get(id=id)
        data = Address.objects.filter(user=data.user)
        serializer = AddressSerializer(data=data, many=True)
        if serializer.is_valid():
            pass
        return Response(serializer.data)


class LocationSearch(generics.ListAPIView):

    search_fields = ['country', 'city']
    filter_backends = (filters.SearchFilter,)
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
