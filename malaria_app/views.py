from django.shortcuts import render

# Create your views here.
# malaria_app/views.py

from django.shortcuts import render, redirect
from .forms import MalariaImageForm
from .utils import predict_malaria
import os


def index(request):
    return render(request, 'malaria_app/home.html')

from django.conf import settings
import os

def home(request):
    if request.method == 'POST':
        form = MalariaImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            
            # Chemin absolu pour le traitement
            image_path = instance.image.path
            prediction_result = predict_malaria(image_path)
            
            # URL relative pour l'affichage
            image_url = instance.image.url
            
            context = {
                'prediction': prediction_result['class'],
                'confidence': prediction_result['confidence'],
                'patient_name': request.POST.get('paatient_name', ''),
                'medical_notes': request.POST.get('noteMedical', ''),
                'image_url': image_url  # Ajout de l'URL de l'image
            }
            return render(request, 'malaria_app/result.html', context)
    else:
        form = MalariaImageForm()
    return render(request, 'malaria_app/index.html', {'form': form})


# malaria_app/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import predict_malaria
import os

@csrf_exempt  # Pour permettre les requêtes POST depuis d'autres domaines (à sécuriser en production)
def predict(request):
    if request.method == 'POST':
        try:
            # Récupérer le fichier image
            image_file = request.FILES['image']
            
            # Sauvegarder temporairement le fichier
            temp_path = os.path.join('media', 'temp', image_file.name)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            
            with open(temp_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            # Faire la prédiction
            prediction = predict_malaria(temp_path)
            
            # Nettoyer le fichier temporaire
            os.remove(temp_path)
            
            return JsonResponse({
                'status': 'success',
                'prediction': prediction,
                'confidence': 0.95  # Vous pouvez modifier ceci pour retourner la vraie confiance
            })
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée'
    }, status=405)