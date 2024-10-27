from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, JsonResponse
import os
import google.generativeai as genai
from django.http import HttpResponse
import logging
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import logging  # Import logging for server-side logging
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import authenticate, login
from .models import HealthData
# Set up logging
logger = logging.getLogger(__name__)

from django.http import JsonResponse

from django.http import JsonResponse
import os
import google.generativeai as genai

@csrf_exempt
def chatbot(request):
    if request.method == "GET":
        return render(request, 'chatbot.html')

    elif request.method == "POST":
        try:
            user_input = request.POST.get("message", "").strip()  # Use .strip() to remove whitespace

            if not user_input:  # Check if the user input is empty
                return JsonResponse({'error': 'Input cannot be empty.'}, status=400)

            # Ensure the API key is set
            os.environ["gemAPI"] = "AIzaSyCpru-FWFISXO0hW6A_qosuoLu9RePUF2Q"
            api_key = os.getenv("gemAPI")
            
            if api_key is None:
                raise ValueError("gemAPI environment variable is not set.")
            
            # Configure genai
            genai.configure(api_key=api_key)

            # Set generation config
            generation_config = {
                "temperature": 2,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }

            # Initialize the model
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
            )

            # Start a chat session
            chat_session = model.start_chat(
                history=[
                    {"role": "user", "parts": ["hi\n"]},
                    {"role": "model", "parts": ["Hi there! How can I help you today?\n"]},
                ]
            )

            # Send message and capture response
            response = chat_session.send_message(user_input)
            
            # Extract response text
            response_text = getattr(response, 'content', None) or getattr(response, 'text', None)
            response_text = response_text if response_text else "The chatbot did not respond with text."
            
            return JsonResponse({'response': response_text})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

       
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        

        if password1 == password2:
            # Check for existing username and email
            if User.objects.filter(username=username).exists():
                error_message = "Username already exists"
            elif User.objects.filter(email=email).exists():
                error_message = "Email is already registered"
            else:
                try:
                    # Create the user
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    # Log the user in and redirect
                    auth.login(request, user)
                    return redirect('data')
                except IntegrityError:
                    error_message = "Error creating account. Please try again."
        else:
            error_message = "Passwords do not match"
        
        # Render with the error message
        return render(request, 'register.html', {'error_message': error_message})
    
    # Render the registration page for GET requests
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def data(request):
    if request.method == "POST":
        
        name = request.POST.get("name")
        age = request.POST.get("age")
        height= request.POST.get("height")
        weight=request.POST.get("weight")
        gender=request.POST.get("gender")

        # Basic example of analyzing input data
        output = analyze_heart_health(name, age, height, weight, gender)

        # Redirect to the dashboard after analysis
        return redirect('dashboard')  # Replace 'dashboard' with your actual URL name

    return render(request, 'form.html')

def analyze_heart_health(name, age, height, weight, gender):
    # Placeholder analysis function
    return f"Name: {name} Age: {age} Height: {height} Weight: {weight} Gender: {gender}"


@login_required
def dashboard(request):
    # Get the logged-in user's profile
    profile = Profile.objects.get(user=request.user)
    
    # Pass name and profile_picture to the template
    context = {
        'name': request.user.username,
        'profile_picture': profile.profile_picture.url if profile.profile_picture else None
    }
    return render(request, 'dashboard.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Automatically create the profile if it doesn’t exist
            Profile.objects.get_or_create(user=user)
            
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

# views.py
from django.shortcuts import render, redirect
from .models import HealthData

def health_data_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        height = request.POST['height']
        weight = request.POST['weight']
        gender = request.POST['gender']
        
        # Create a new instance of HealthData and save it to the database
        health_data = HealthData(
            name=name,
            age=age,
            height=height,
            weight=weight,
            gender=gender
        )
        health_data.save()

        # Redirect to the dashboard after saving data
        return redirect('dashboard')  # Replace 'dashboard' with the name of your dashboard view
    
    return render(request, 'form.html')

def ai(request):
    context = {
        'name': request.user.username,
    }
    return render(request,'ai.html',context)
