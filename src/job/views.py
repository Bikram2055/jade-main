import datetime

from django.db.models import Count, OuterRef, Subquery
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from src.common.permissions import IsEmployer
from src.job.models import Bid, Job, Project
from src.job.serializers import (
    BidperJobSerializer,
    BidSerializer,
    CategorywiseJobSerializer,
    JobSerializer,
    ProjectSerializer,
    ShortlistSerializer,
)

# Create your views here.


class JobUpdate(generics.RetrieveUpdateDestroyAPIView):
    """This is a Django REST Framework view for handling HTTP requests for updating and deleting
     a single job resource.

    The JobUpdate class is a subclass of generics.RetrieveUpdateDestroyAPIView, which is a generic
    view that provides the implementation for the HTTP GET, PUT, and DELETE methods.

    The queryset attribute specifies the set of Job objects that this view will handle. In this case,
    it's set to all jobs in the database.

    The serializer_class attribute specifies the serializer class that will be used to serialize and
    deserialize the job data. In this case, it's set to JobSerializer, which is presumably a custom
    serializer class defined elsewhere in the codebase.

    The permission_classes attribute specifies the set of permission classes that a user must satisfy
    in order to access the view. In this case, it requires that the user be authenticated and be an
    employer, as defined by the IsEmployer permission class. This means that only authenticated employers
    can update or delete job resources.
    """

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]


class Number_Of_JObs(APIView):
    """
    View to list all users in the system.
    """

    def get(self, request):
        """
        Return a list of all users.
        """
        no_of_jobs = Job.objects.all().count()
        return Response({"Jobs count": no_of_jobs})


class Job_Count_Category(APIView):
    """This is a Python class that implements an API endpoint for getting the count of job posts in each category.
    The class is a subclass of APIView from the Django REST framework and defines a single method, get,
     which implements the endpoint.
    """

    def get(self, request):
        """api get method

        Args:
            request (object): used to get data from endpoint

        Returns:
            data(json): category wise job count
        """
        data = Job.objects.values('category__category').annotate(count=Count('id'))
        serializer = CategorywiseJobSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer = serializer
        return Response(serializer.data)


class JobAge(APIView):
    """This is a Python class that implements an API endpoint for getting the age of a job post in days.
    The class is a subclass of APIView from the Django REST framework and defines a single method, get,
     which implements the endpoint.
    """

    def get(self, request, id):
        """api get method

        Args:
            request (object): used to get data from endpoint
            id (int): job id

        Returns:
            age(int): age of job
        """

        today = datetime.date.today()
        job_post_date = get_object_or_404(Job, id=id)
        if job_post_date is not None:
            age = -(datetime.datetime.date(job_post_date.created_at) - today).days
            return Response({'age': age})
        return Response(status=status.HTTP_404_NOT_FOUND)


class SearchJob(generics.ListAPIView):
    """This is a Django REST Framework view for handling HTTP requests for searching and retrieving
     a list of job resources based on a search query.

    The SearchJob class is a subclass of generics.ListAPIView, which is a generic view that provides the
    implementation for the HTTP GET method for listing resources.

    The search_fields attribute specifies the fields that can be searched using the search query. In this
    case, the name and description fields of the Job model can be searched.

    The filter_backends attribute specifies the filter backends that will be used to filter the results
    based on the search query. In this case, the SearchFilter backend is used.

    The queryset attribute specifies the set of Job objects that this view will handle. In this case,
    it's set to all jobs in the database.

    The serializer_class attribute specifies the serializer class that will be used to serialize and
    deserialize the job data. In this case, it's set to JobSerializer, which is presumably a custom
    serializer class defined elsewhere in the codebase.

    When an HTTP GET request is made to this view, the SearchFilter backend will filter the Job objects
    based on the search query specified in the query parameter. The filtered objects will be serialized
    using the JobSerializer and returned in the HTTP response.
    """

    search_fields = ['name', 'description']
    filter_backends = (filters.SearchFilter,)
    subquery = Project.objects.filter(job=OuterRef('pk')).values('job')
    queryset = Job.objects.annotate(is_in_project=Subquery(subquery)).filter(is_in_project=None, is_draft=False)
    serializer_class = JobSerializer


class BidCreateApi(generics.ListCreateAPIView):
    """This is a Django REST Framework view for handling HTTP requests for creating and listing bid resources.

    The BidCreateApi class is a subclass of generics.ListCreateAPIView, which is a generic view that provides the
    implementation for the HTTP GET and POST methods for listing and creating resources.

    The queryset attribute specifies the set of Bid objects that this view will handle. In this case,
    it's set to all bids in the database.

    The serializer_class attribute specifies the serializer class that will be used to serialize and
    deserialize the bid data. In this case, it's set to BidSerializer, which is presumably a custom
    serializer class defined elsewhere in the codebase.

    The permission_classes attribute specifies the set of permission classes that a user must satisfy
    in order to access the view. In this case, it requires that the user be authenticated, meaning that
    only authenticated users can create or list bid resources.

    When an HTTP GET request is made to this view, all Bid objects in the queryset will be serialized
    using the BidSerializer and returned in the HTTP response.

    When an HTTP POST request is made to this view, the posted bid data will be deserialized using the
    BidSerializer, and a new Bid object will be created in the database with the deserialized data.
    The created bid object will be serialized using the BidSerializer and returned in the HTTP response."""

    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]


class BidUpdateApi(generics.RetrieveUpdateDestroyAPIView):

    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]


class ShortlistApi(generics.RetrieveUpdateAPIView):
    queryset = Bid.objects.all()
    serializer_class = ShortlistSerializer
    permission_classes = [IsEmployer]


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class JobApi(generics.ListCreateAPIView):

    subquery = Project.objects.filter(job=OuterRef('pk')).values('job')
    queryset = Job.objects.annotate(is_in_project=Subquery(subquery)).filter(is_in_project=None, is_draft=False)
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    pagination_class = LargeResultsSetPagination


class BidsPerJob(APIView):
    """This code defines a Django Rest Framework API view named BidsPerJob.
    The view handles GET requests and returns a serialized representation of the number of bids per job.
    """

    def get(self, request):
        data = Bid.objects.values('job__name').annotate(count=Count('id'))
        serializer = BidperJobSerializer(data=data, many=True)
        if serializer.is_valid():
            pass
        return Response(serializer.data)


class ProjectApi(APIView):  # (generics.ListCreateAPIView):
    """This code defines a Django Rest Framework API view named ProjectApi with two methods: get() and post().
    The view handles GET and POST requests for a Project model.
    """

    permission_classes = [permissions.IsAuthenticated]
    # queryset = Project.objects.all()
    # serializer_class = ProjectSerializer

    def get(self, request):
        """This code defines a GET method for a Django Rest Framework API view that retrieves all
        instances of the Project model from the database, serializes them using the ProjectSerializer,
        and returns the serialized data in a HTTP response.

        Args:
            request (object): used to get data from endpoint

        Returns:
            projects(json_object): all projects available in project table
        """
        data = Project.objects.all()
        serializer = ProjectSerializer(data=data, many=True)
        if serializer.is_valid():
            pass
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('job_id', openapi.IN_QUERY, "ID of job", type=openapi.TYPE_INTEGER),
            openapi.Parameter('employer_id', openapi.IN_QUERY, "ID of employer", type=openapi.TYPE_INTEGER),
            openapi.Parameter('job_seeker_id', openapi.IN_QUERY, "ID of job-seeker", type=openapi.TYPE_INTEGER),
        ],
        operation_id='this_is_the_view_to_assign_employer_for_job',
    )
    def post(self, request):
        """This code defines a POST method for a Django Rest Framework API view that retrieves all
        instances of the Project model from the database, serializes them using the ProjectSerializer,
        and returns the serialized data in a HTTP response.

        Args:
            request (_type_): used to get data from endpoint

        Returns:
            project(object): recently added project
        """

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
