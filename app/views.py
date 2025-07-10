from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from app.models import ArchivoExcel
from .forms import RegistroForm
from .forms import ArchivoExcelForm
import pandas as pd
import plotly.express as px
import os
from .forms import AnalisisForm

def home(request):
    return render(request, 'home.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def subir_archivo(request):
    if request.method == 'POST':
        form = ArchivoExcelForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_archivo = form.save(commit=False)
            nuevo_archivo.usuario = request.user
            nuevo_archivo.save()
            return redirect('lista_archivos')
    else:
        form = ArchivoExcelForm()
    return render(request, 'subir_archivo.html', {'form': form})

def lista_archivos(request):
    archivos = ArchivoExcel.objects.filter(usuario=request.user).order_by('-fecha_subida')
    return render(request, 'lista_archivos.html', {'archivos': archivos})

def analizar_archivo(request, archivo_id):
    archivo = get_object_or_404(ArchivoExcel, id=archivo_id, usuario=request.user)
    ruta_archivo = archivo.archivo.path
    df = pd.read_excel(ruta_archivo)

    resumen = {
        'filas': df.shape[0],
        'columnas': df.shape[1],
        'columnas_nombres': list(df.columns),
        'primeros_datos': df.head(10).to_html(classes='table table-bordered', index=False),
    }

    # ✅ CONVERTIMOS A LISTA NORMAL para evitar errores
    columnas_num = list(df.select_dtypes(include='number').columns)
    columnas_cat = list(df.select_dtypes(include='object').columns)

    estadisticas_html = None
    grafico_html = None
    agrupado_html = None

    if request.method == 'POST':
        form = AnalisisForm(request.POST, columnas_num=columnas_num, columnas_cat=columnas_cat)
        if form.is_valid():
            col_num = form.cleaned_data['columna_numerica']
            col_cat = form.cleaned_data['columna_categorica']

            # Estadísticas
            estadisticas = df[[col_num]].agg(['sum', 'mean', 'max', 'min']).transpose()
            estadisticas_html = estadisticas.to_html(classes='table table-striped table-sm')

            # Agrupado
            agrupado = df.groupby(col_cat)[col_num].sum().reset_index()
            agrupado_html = agrupado.to_html(classes='table table-bordered table-sm', index=False)

            # Gráfico
            fig = px.bar(agrupado, x=col_cat, y=col_num, title=f'{col_num} por {col_cat}')
            grafico_html = fig.to_html(full_html=False)
    else:
        if len(columnas_num) > 0 and len(columnas_cat) > 0:
            form = AnalisisForm(columnas_num=columnas_num, columnas_cat=columnas_cat)
        else:
            form = None  # No hay columnas suficientes para análisis

    return render(request, 'analizar_archivo.html', {
        'archivo': archivo,
        'resumen': resumen,
        'form': form,
        'estadisticas_html': estadisticas_html,
        'agrupado_html': agrupado_html,
        'grafico_html': grafico_html,
    })