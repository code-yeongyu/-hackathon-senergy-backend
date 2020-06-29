from sleep.serializers import SleepRecordSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from sleep.models import SleepRecord
from senergy.permissions import IsOwnerOrReadOnly
from drf_yasg.utils import swagger_auto_schema

import json


def convert_status_to_string(numbers):
    numbers_length = len(numbers)
    numbers_sum = sum(numbers)
    if numbers_sum == 0:
        return '데이터 에러'
    number = numbers_sum / numbers_length
    if 1 <= number and number >= 3:
        return '힘든 하루 힘내세요'
    if 4 <= number and number >= 7:
        return '오늘 하루는 무난한 하루가 되겠네요'
    return '오늘 하루는 활기찬 하루에요'


class SleepDetail(generics.RetrieveAPIView):
    queryset = SleepRecord.objects.all()
    serializer_class = SleepRecordSerializer
    permission_classes = (IsOwnerOrReadOnly, )


@swagger_auto_schema(method='post',
                     operation_description="""Add sleep record
                     ---
                     # Parameters
                        - data: json-like array, like [1, 2, 3, 4, 5]""",
                     responses={
                         201: 'Created',
                         401: 'Unauthorized'
                     })
@swagger_auto_schema(
    method='get',
    operation_description=
    "Get sleep record with pagination, per_page parameter to limit the record size, page record to specify page.",
    responses={
        200:
        '''"data": [
        {
            "datetime": "2020-06-29T16:27:58.169824Z",
            "status": "데이터 에러"
        },
        {
            "datetime": "2020-06-29T16:27:58.169824Z",
            "status": "힘든 하루 힘내세요"
        }
    ]'''
    })
@api_view(['POST', 'GET'])
def sleep_record(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        sleep_data = request.POST.get('data', [])
        SleepRecord.objects.create(owner=request.user, data=sleep_data)
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 5)
        records = SleepRecord.objects.filter(owner=request.user)
        page -= 1
        status = [{
            "datetime": record.datetime,
            "status": convert_status_to_string(json.loads(record.data))
        } for record in records[per_page * page:per_page * page + per_page]]
        return Response({'data': status})
    # test arrayfield
