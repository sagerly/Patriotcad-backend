from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .models import CurrentCall, Civilian, Citation, Arrest, Warrant, Vehicle
from .serializers import CurrentCallSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

class CurrentCallViewSet(viewsets.ModelViewSet):
    queryset = CurrentCall.objects.all().order_by('-time_of_call')
    serializer_class = CurrentCallSerializer

def search_civilian(request):
    if request.method == 'GET':
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        civilian = get_object_or_404(Civilian, first_name=first_name, last_name=last_name)
        citations = Citation.objects.filter(civilians=civilian)
        arrests = Arrest.objects.filter(civilians=civilian)
        warrants = Warrant.objects.filter(civilians=civilian)
        vehicles = Vehicle.objects.filter(civilians=civilian)

        civilian_data = {
            'id': civilian.id,
            'first_name': civilian.first_name,
            'last_name': civilian.last_name,
            'date_of_birth': civilian.date_of_birth,
            'citations': [c.description for c in citations],
            'arrests': [a.description for a in arrests],
            'warrants': [w.description for w in warrants],
            'vehicles': [{'make': v.make, 'model': v.model, 'license_plate': v.license_plate} for v in vehicles],
        }

        return JsonResponse({'civilian_data': civilian_data})

def delete_call(request, call_id):
    if request.method == 'DELETE':
        try:
            call = CurrentCall.objects.get(pk=call_id)
            call.delete()
            return JsonResponse({'message': 'Call deleted successfully'}, status=204)
        except CurrentCall.DoesNotExist:
            return JsonResponse({'message': 'Call not found'}, status=404)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

@api_view(['POST'])
def create_call(request):
    if request.method == 'POST':
        serializer = CurrentCallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({'error': 'Please provide all required fields'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)