# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Academy,UserApp

# @receiver(post_save,sender=Academy)
# def create_academy_user(sender, instance,created,**kwargs):
#     if created:
#         user=UserApp.objects.create(
#             username=instance.academy.lower().replace(" ","_"),
#             password=instance.password,
#             email=instance.email,
#             is_academy=True
#         )
#         instance.user=user
#         instance.save()