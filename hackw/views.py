from xmlrpc.client import ResponseError
from django.http import JsonResponse
from .models import Event
from .serializers import EventSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import psycopg
import logging
from psycopg.errors import ProgrammingError
from .service import getEventDetails, createEvent, getAll



@api_view(['GET', 'POST'])
def event_list(request):
    if request.method == 'GET':
        #events = Event.objects.all()
        #serializer = EventSerializer(events, many = True)
        response = JsonResponse({"events": getAll()})
        response["Access-Control-Allow-Origin"] = "*"
        return response
    
    if request.method == 'POST':
        serializer = EventSerializer(data = request.data)
        if serializer.is_valid():
            #serializer.save()
            createEvent(serializer.data["name"], serializer.data["slide_url"])
            #print(serializer.data["name"], serializer.data["slide_url"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def get_detail(request, id):
    return Response(data = getEventDetails(id), status=status.HTTP_200_OK)

