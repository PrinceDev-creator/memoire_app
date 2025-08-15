from rest_framework.views import APIView    
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view 
from django.shortcuts import render
from django.template.loader import get_template
from datetime import date, datetime
from babel.dates import format_date
from pre_registration.models import PreRegistration
from .serializers import PreRegistrationSerializer
from .utils import send_preg_email_with_html_body_to_school,send_preg_email_with_html_body_to_app_team
from utils.helps import send_email_with_html_body
from school.models import School


class PreRegistrationView(APIView):
    
    def post(self,request, *args, **kwargs):
        """This view help to create and account for testing sending mails"""
        
        # template_email = get_template('emails/email.html')
        # print("Template trouvé à:", template_email.origin.name)

        ctx={}
        
        print('okay')
            
        data=request.data.copy()
        
        print(f"data: {data}")
        
        serializer=PreRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=400)
        
        
        email = data.get('email')
        director=data.get('director')
        school_name=data.get('school_name')
        phone_number=data.get('phone_number')
        address=data.get('address')
        
        template_preg_school='emails/preg_email_to_school.html'
        template_preg_app_team='emails/preg_email_to_app_team.html'
        
        context_preg_school={
            'date': format_date(date.today(), format='full', locale='fr'),
            'email': "princedev317@gmail.com" ,
            'director': director,
            'school_name': school_name
        }
        
        context_preg_app_team={
            'date': format_date(date.today(), format='full', locale='fr'),
            'email': email,
            'director': director,
            'school_name': school_name,
            "address": address,
            "phone_number": phone_number,
            "dev_url": "http://192.168.1.108:8000/schools-preg/"
        }
        
        receiver_school=[email]
        receiver_app_team=["princedev317@gmail.com"]
        subject="Email de pré-inscription"
        
        print(f"email : {email}")
        
        has_send_to_school = send_preg_email_with_html_body_to_school(subject=subject, receivers=receiver_school, template=template_preg_school, context=context_preg_school)
        has_send_to_app_team = send_preg_email_with_html_body_to_app_team(subject=subject, receivers=receiver_app_team, template=template_preg_app_team, context=context_preg_app_team)
        
        if has_send_to_school and has_send_to_app_team:
            ctx={"msg": "Mail envoyé avec succès"}
            status=200
        else:
            ctx={"msg": "L'envoi du mail a échoué"}
            status=500
        
        return Response(ctx, status=status)
    
def print_hello(request,*args, **kwargs):
    print("Hello")
    return Response({"message": "Hello, world!"})

def school_list_view(request):
    pre_schools = PreRegistration.objects.all()
    print(f'pre_schools : {pre_schools}')
    context = {
        'pre_schools': pre_schools,
        'page_title': "Liste des Écoles"
    }
    return render(request, 'schools_preg/schools_list.html', context)

@api_view(['POST'])
def reject_registration_view(request):
    # Vérification du format de la requête (POST)
    if request.method != 'POST':
        return Response(
            {"message": "Méthode non autorisée"}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    try:
        data = request.data.copy()
        email = data.get('email')
        preg_id=data.get('preg_id')
        
        has_refused=update_state_preg_school(preg_id=preg_id)
        if not has_refused:
            return Response(
                {"message": "École non trouvée"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not email:
            return Response(
                {"message": "Email manquant"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        print(f"email : {email}")

        # Formatage de la date en français
        current_date = format_date(date.today(), format='full', locale='fr'),

        # Envoi de l'email
        has_send = send_email_with_html_body(
            subject="Pré-inscription rejetée",
            receivers=[email],  # Liste attendue même pour un seul destinataire
            template='emails/preg_email_reject.html',
            context={'date': current_date}
        )

        if has_send:
            return Response(
                {"message": "Pré-inscription rejetée avec succès."},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Échec de l'envoi du message"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        print(f"Erreur : {str(e)}")
        return Response(
            {"message": "Erreur interne du serveur"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def update_state_preg_school(preg_id):
    preg_school=PreRegistration.objects.filter(id=preg_id).first()
    
    if preg_school==None:
        return False
    
    preg_school.state=False
    preg_school.save()
    
    return True
    