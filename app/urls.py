from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('subir/', views.subir_archivo, name='subir_archivo'),
    path('archivos/', views.lista_archivos, name='lista_archivos'),
    path('analizar/<int:archivo_id>/', views.analizar_archivo, name='analizar_archivo'),
    path('exportar/<int:archivo_id>/', views.exportar_excel, name='exportar_excel'),
    path('exportar-pdf/<int:archivo_id>/', views.exportar_pdf, name='exportar_pdf'),
    path('eliminar/<int:archivo_id>/', views.eliminar_archivo, name='eliminar_archivo'),

]
