from django.conf.urls import url
from .views import solicitud, pedidos, login, register

urlpatterns = [
    url('', solicitud, name='solicitudHome'),
    url('solicitud/', solicitud, name='solicitud'),
    url('pedidos/', pedidos, name='pedidos'),
    url('login/', login, name='login'),
    url('register/', register, name='register'),
]