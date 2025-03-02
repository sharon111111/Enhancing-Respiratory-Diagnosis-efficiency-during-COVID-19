from django.http import HttpResponse  
from django.shortcuts import render  
from django.shortcuts import render, redirect  
from django.core.files.storage import FileSystemStorage  
from joblib import load  
from subprocess import run  
from PIL import Image  
import matplotlib.pyplot as plt  
import os  
import torch  
from torchvision import transforms  
import cv2  
import torch  
from torchvision import models  
from django.conf import settings  
from django.contrib.auth.decorators import login_required  

@login_required(login_url='/login')  
def index(request):  
    return render(request, 'index.html')  

import os  
import cv2  
import torch  
from torchvision import transforms, models  
from django.core.files.storage import FileSystemStorage  
from django.conf import settings  
from django.shortcuts import render
from django.contrib.auth.models import User  
from django.contrib.auth import authenticate, login, logout  
from django.contrib.auth.hashers import import make_password  

def home(request):  
    return render(request, 'home.html')  

def register(request):  
    if request.method == "POST":  
        first_name = request.POST.get('first_name')  
        last_name = request.POST.get('last_name')  
        username = request.POST.get('username')  
        email = request.POST.get('email')  
        password = request.POST.get('password')  
        password1 = request.POST.get('password1')  
        if password == password1:  
            passwd = make_password(password)  
            obj = User.objects.create(first_name=first_name,  
                                      last_name=last_name,  
                                      username=username,  
                                      email=email,  
                                      password=passwd,  
                                      is_staff=True)  
            return redirect('/login')  
        else:  
            error_message = "Passwords do not match"  
            return render(request, 'registration.html', {'error_message': error_message})  
    return render(request, 'registration.html')  

def patient_registration(request):  
    if request.method == "POST":  
        first_name = request.POST.get('first_name')  
        last_name = request.POST.get('last_name')  
        username = request.POST.get('username')  
        email = request.POST.get('email')  
        password = request.POST.get('password')  
        password1 = request.POST.get('password1')
        if password == password1:  
    passwd = make_password(password)  
    obj = User.objects.create(first_name=first_name,  
                              last_name=last_name,  
                              username=username,  
                              email=email,  
                              password=passwd)  
    return redirect('/patient_login')  
else:  
    error_message = "Passwords do not match"  
    return render(request, 'patient_registration.html', {'error_message': error_message})  

return render(request, 'patient_registration.html')  

def patient_login(request):  
    if request.method == 'POST':  
        username = request.POST.get('username')  
        password = request.POST.get('password')  
        user = authenticate(request, username=username, password=password)  
        print("user")  
        if user is not None and user.is_staff == False:  
            login(request, user)  
            print("loginnnnnnnnnnnnnnnn")  
            return redirect('/')  # Redirect to a home page or another page after login  
        else:  
            error_message = "Invalid username or password"  
            return render(request, 'patient_login.html', {'error_message': error_message})  

    return render(request, 'patient_login.html')  

def login_view(request):  
    if request.method == 'POST':  
        print()  
        username = request.POST.get('username')  
        password = request.POST.get('password')  
        user = authenticate(request, username=username, password=password)  
        print("user", user)
        if user is not None:  
    login(request, user)  
    print("loginnnnnnnnnnnnnnnn")  
    return redirect('/doctor_db')  # Redirect to a home page or another page after login  
else:  
    error_message = "Invalid username or password"  
    return render(request, 'login.html', {'error_message': error_message})  

return render(request, 'login.html')  

def doctor_db(request):  
    user_name = request.user.first_name  
    data = User.objects.filter(is_staff=False).all()  

    context = {  
        'user_name': user_name,  
        'data': data  
    }  

    return render(request, 'doctor_db.html', context)  

def doctor_logout(request):  
    logout(request)  
    return redirect('/home')  

@login_required(login_url='/login')  
def analyze(request):  
    if request.method == 'POST':  
        uploaded_image = request.FILES['image_input']  
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)  
static_image_path = 'static/' + uploaded_image.name  
fs.save(static_image_path, uploaded_image)  

model = models.resnet152(pretrained=False, num_classes=2)  
model_path = '../Trainedmodels/best.pth'  
model.load_state_dict(torch.load(model_path))  
model.eval()  

test_transform = transforms.Compose([  
    transforms.Resize((224, 224)),  
    transforms.ToTensor(),  
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  
])  

class_mapping = {  
    0: 'Normal',  
    1: 'Pneumonic'  
}  

with torch.no_grad():  
    image = cv2.imread(uploaded_image.name)  
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
    image = cv2.resize(image, (224, 224))  
    image = transforms.ToPILImage()(image)  
    input_tensor = test_transform(image).unsqueeze(0)  
    output = model(input_tensor)  
    _, predicted = torch.max(output, 1)  
    predicted_label = class_mapping[predicted.item()]  

    if predicted_label.strip() == 'Normal':  
        confidence = 0  
    else:  
        softmax_probs = torch.softmax(output, dim=1)  
        confidence = softmax_probs[0][predicted.item()].item() * 100  
        predicted_label = 'affected by respiratory disorder'