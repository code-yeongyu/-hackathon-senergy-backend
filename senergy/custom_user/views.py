from rest_framework.decorators import api_view
from custom_user.serializers import ProfileSerializer
from custom_user.forms import RegisterForm
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from custom_user.models import Profile
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


class ProfileAPIView(APIView):
    @swagger_auto_schema(operation_description="Get user profile",
                         responses={
                             200: '''{
    "name": "foo",
    "weight": 65.0,
    "average_sleep_time": 6.0,
    "sleep_at": '16:27:58',
    "image": [url]
}''',
                             401: "Unauthorized"
                         })
    def get(self, request):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            return Response(ProfileSerializer(profile).data,
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(operation_description="""Patch User Profile
    ---
        # Parameters
            - weight: float
            - average_sleep_time : float
            - sleep_at: string | time format | nullable
            - image: string | image url | nullable
    """,
                         responses={
                             200: 'Updated',
                             401: 'Unauthorized',
                             406: 'Form error',
                         })
    def patch(self, request):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def register(request):  # fix here
    """
        registeration
        ---
        # Parameters
            - username: string
            - email: string | email-format
            - password1: string | password
            - password2: string | password confirmation
            - name: string | the user's name
            - weight: float
            - average_sleep_time : float
            - sleep_at: string | time format | nullable
            - image: string | image url | nullable
    """
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        try:  # fix it later
            user.save()
        except:
            pass
        profile = Profile.objects.create(
            user=user,
            name='default',
            weight=-1,
            average_sleep_time=-1,
        )
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        Profile.objects.get(user=user).delete()
        #import pdb; pdb.set_trace()
        print(serializer.errors)
        return Response(serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
    print(serializer.errors)
    return Response(form.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
