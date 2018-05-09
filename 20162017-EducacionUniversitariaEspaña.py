
# coding: utf-8

# # Educación Universitaria en España

# ## Datos del curso 2016/17 Ministerio de Educación, Cultura y Deporte

# Todos los datos que se tratan en este estudio están disponibles aquí: http://www.mecd.gob.es/servicios-al-ciudadano-mecd/estadisticas/educacion/universitaria/estadisticas/alumnado/2016-2017/Grado-y-Ciclo.html

# In[2]:


# Import
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import stats
from pylab import *
pd.options.display.max_columns = None
import scipy


# In[29]:


# Import all bokeh functions needed
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, output_file, show
from bokeh.models.annotations import BoxAnnotation
from bokeh.models import ColumnDataSource, LabelSet, Label, LinearAxis, Range1d, Toggle, BoxAnnotation, CustomJS
from bokeh.palettes import Spectral6
from bokeh.transform import jitter, dodge
from bokeh.models import HoverTool, Legend, LegendItem
from bokeh.layouts import gridplot, layout
from bokeh.core.properties import value
output_notebook()


# In[4]:


# Set path
DATASET_PATH = '/Users/lola/Documents/WooM/Data Analysis/20180426 - MUJER_STEM/'


# In[6]:


# Function to load .csv files as pandas DataFrame
def load_dataset(dataset_path=DATASET_PATH):
    csv_path = os.path.join(dataset_path, FileName)
    return pd.read_csv(csv_path)


# In[7]:


# Load data file 
FileName = '20162017-MatriculadosCarrerasSexoRamas.csv'
Datos = load_dataset()


# In[8]:


# Group data by study fields
EDUCACION = Datos[Datos['Ramas'] == 'EDUCACIÓN']
ARTES = Datos[Datos['Ramas'] == 'ARTES Y HUMANIDADES']
SOCIALES = Datos[Datos['Ramas'] == 'CIENCIAS SOCIALES, PERIODISMO Y DOCUMENTACIÓN']
NEGOCIOS = Datos[Datos['Ramas'] == 'NEGOCIOS, ADMINISTRACIÓN Y DERECHO']
CIENCIAS = Datos[Datos['Ramas'] == 'CIENCIAS']
INFORMATICA= Datos[Datos['Ramas'] == 'INFORMÁTICA']
INGENIERIA = Datos[Datos['Ramas'] == 'INGENIERÍA, INDUSTRIA Y CONSTRUCCIÓN']
AGRICULTURA = Datos[Datos['Ramas'] == 'AGRICULTURA, GANADERÍA, SILVICULTURA, PESCA Y VETERINARIA']
SALUD = Datos[Datos['Ramas'] == 'SALUD Y SERVICIOS SOCIALES']
SERVICIOS = Datos[Datos['Ramas'] == 'SERVICIOS']


# In[16]:


Teleco = Datos[Datos['Carreras'] == 'Ingeniería de telecomunicación']
Teleco


# En 2016, 1.3 millones de alumnos se matricularon en estudios de grado en universidades españolas (55% mujeres). 
# De ellos, sólo un 1% decidió estudiar Ingeniería de Telecomunicación. De ese 1%, sólo el 20% (2746) son mujeres. 

# In[78]:


genero = ['Mujeres', 'Hombres']
porcentaje = [Teleco['Mujer_por'].values, Teleco['Hombre_por'].values]
matriculados = [Teleco['Mujeres'].values, Teleco['Hombres'].values]

p = figure(x_range=genero, plot_height=600, y_range=(0, 100), title="Matriculados en Ingeniería de Telecomunicación",
           toolbar_location=None, tools="", y_axis_label = "Porcentaje")

l=p.vbar(x=genero, top=porcentaje, width=0.3, legend="Porcentaje de Matriculados")
p.xgrid.grid_line_color = None
p.y_range.start = 0

p.extra_y_ranges = {"foo": Range1d(start=0, end=20000)}
m=p.circle(x=genero, y=matriculados, color="black", y_range_name="foo", legend="Nº Matriculados")
p.line(x=genero, y=matriculados, color="yellow", line_width=2, y_range_name="foo")


#p.line(x=genero, top=matriculados, color="orange", width=0.2)
p.add_layout(LinearAxis(y_range_name="foo", axis_label="Matriculados"), 'right')
#p.add_layout(LinearAxis(axis_label="Porcentaje"), 'left')

#legend = Legend(items=[
#    ("sin(x)"   , [l]),
#    ("2*sin(x)" , [m])
#])
#legend = Legend(items=legend_it, location=(0, -60))
#legend.click_policy="mute"
#p.add_layout(legend, 'below')    
p.legend.location = (50,470)
show(p)


# In[11]:


# Group by 'Ramas'
RAMAS = Datos.groupby(['Ramas'], as_index=False).sum()
RAMAS = RAMAS.sort_values(by=['Diferencia'], ascending=False)


# #### Porcentaje de Mujeres matriculadas por ramas y diferencia en volumen con respecto a hombres

# In[79]:


ramas = RAMAS['Ramas'].unique()
porcentaje = RAMAS['Mujeres'].values * 100 / RAMAS['Matriculados']
diferencia = RAMAS['Mujeres'].values - RAMAS['Hombres'].values
matriculados = RAMAS['Matriculados'].values

p = figure(x_range=ramas, plot_height=600, y_range=(0, 100), title="Matriculados por Ramas",
           toolbar_location=None, tools="", y_axis_label = "Porcentaje de Mujeres")

p.vbar(x=ramas, top=porcentaje, width=0.3, legend="Porcentaje de Mujeres")
p.xgrid.grid_line_color = None
p.y_range.start = 0

p.extra_y_ranges = {"foo": Range1d(start=-100000, end=100000)}
p.line(x=ramas, y=diferencia, color="yellow", line_width=2, y_range_name="foo")
p.circle(x=ramas, y=diferencia, color="black", y_range_name="foo", legend="Nº Mujeres - Nº Hombres")

#p.line(x=carreras, top=diferencia, color="orange", width=0.2)
p.add_layout(LinearAxis(y_range_name="foo", axis_label="(Nº Mujeres - Nº Hombres)"), 'right')
#p.add_layout(LinearAxis(axis_label="Porcentaje de Mujeres"), 'left')


box = BoxAnnotation(bottom=0, top=25, fill_alpha=0.1, fill_color='red')
p.add_layout(box)
box = BoxAnnotation(bottom=75, top=100, fill_alpha=0.1, fill_color='red')
p.add_layout(box)


#p.xaxis.axis_label = "Profesiones"
#p.yaxis.axis_label = "Porcentaje de Mujeres"
p.xaxis.major_label_orientation = math.pi/3
p.xaxis.axis_label_text_font_style = "bold"
p.yaxis.axis_label_text_font_style = "italic"
p.legend.location = (250,150)


show(p)


# ### Top 20 de carreras universitarias donde el porcentaje de mujeres es mayor

# In[76]:


Datos = Datos.sort_values(by=['Mujer_por'], ascending=False)
Datos[:20]


# ### Top 20 de carreras universitarias donde el porcentaje de mujeres es menor

# In[77]:


Datos = Datos.sort_values(by=['Mujer_por'], ascending=True)
Datos[:20]


# Educación infantil cuenta con un 93% de mujeres y representa un porcentaje del 3.4% del total de matriculados: un volumen ligeramente inferior a la suma de los alumnos de las primeras 9 carreras con un menor porcentaje de mujeres matriculadas.

# ### Top 10 de carreras universitarias donde hay mayor volumen de mujeres que hombres matriculadas

# In[86]:


Datos = Datos.sort_values(by=['Diferencia'], ascending=False)
Datos[:10]


# ### Top 10 de carreras universitarias donde hay mayor volumen de hombres que mujeres matriculadas

# In[88]:


Datos = Datos.sort_values(by=['Diferencia'], ascending=True)
Datos[:10]


# In[80]:


# Call plots
# EDUCACION
EDUCACION = EDUCACION.sort_values(by=['Mujer_por'])
carreras = EDUCACION['Carreras'].unique()
porcentaje = EDUCACION['Mujer_por'].values
diferencia = EDUCACION['Diferencia'].values

s1 = figure(x_range=carreras, plot_height=600, y_range=(0, 100), title="Matriculados en EDUCACIÓN",
           toolbar_location=None, tools="", y_axis_label = "Porcentaje de Mujeres")
s1.vbar(x=carreras, top=porcentaje, width=0.3, legend="Porcentaje de Mujeres")
s1.xgrid.grid_line_color = None
s1.y_range.start = 0
s1.extra_y_ranges = {"foo": Range1d(start=-40000, end=40000)}
s1.line(x=carreras, y=diferencia, color="yellow", line_width=2, y_range_name="foo")
s1.circle(x=carreras, y=diferencia, color="black", y_range_name="foo", legend="Nº Mujeres - Nº Hombres")
s1.add_layout(LinearAxis(y_range_name="foo", axis_label="(Nº Mujeres - Nº Hombres)"), 'right')
s1.xaxis.major_label_orientation = math.pi/3
s1.xaxis.axis_label_text_font_style = "bold"
s1.yaxis.axis_label_text_font_style = "italic"
#mid_box = BoxAnnotation(bottom=0, top=49.9, fill_alpha=0.1, fill_color='red')
#s1.add_layout(mid_box)
box = BoxAnnotation(bottom=0, top=25, fill_alpha=0.1, fill_color='red')
s1.add_layout(box)
box = BoxAnnotation(bottom=75, top=100, fill_alpha=0.1, fill_color='red')
s1.add_layout(box)

s1.legend.location = (10,330)


# ARTES Y HUMANIDADES
ARTES = ARTES.sort_values(by=['Mujer_por'])
#carreras = ARTES['Carreras2'].unique()
carreras = ARTES['Carreras'].unique()
porcentaje = ARTES['Mujer_por'].values
diferencia = ARTES['Diferencia'].values

s2 = figure(x_range=carreras, plot_height=600, y_range=(0, 100), title="Matriculados en ARTES Y HUMANIDADES",
           toolbar_location=None, tools="", y_axis_label = "Porcentaje de Mujeres")
s2.vbar(x=carreras, top=porcentaje, width=0.3)
s2.xgrid.grid_line_color = None
s2.y_range.start = 0
s2.extra_y_ranges = {"foo": Range1d(start=-40000, end=40000)}
s2.line(x=carreras, y=diferencia, color="yellow", line_width=2, y_range_name="foo")
s2.circle(x=carreras, y=diferencia, color="black", y_range_name="foo")
s2.add_layout(LinearAxis(y_range_name="foo", axis_label="(Nº Mujeres - Nº Hombres)"), 'right')
s2.xaxis.major_label_orientation = math.pi/3
s2.xaxis.axis_label_text_font_style = "bold"
s2.yaxis.axis_label_text_font_style = "italic"
#mid_box = BoxAnnotation(bottom=0, top=49.9, fill_alpha=0.1, fill_color='red')
#s2.add_layout(mid_box)
box = BoxAnnotation(bottom=0, top=25, fill_alpha=0.1, fill_color='red')
s2.add_layout(box)
box = BoxAnnotation(bottom=75, top=100, fill_alpha=0.1, fill_color='red')
s2.add_layout(box)

# CIENCIAS SOCIALES, PERIODISMO Y DOCUMENTACIÓN
SOCIALES = SOCIALES.sort_values(by=['Mujer_por'])
#carreras = SOCIALES['Carreras2'].unique()
carreras = SOCIALES['Carreras'].unique()
porcentaje = SOCIALES['Mujer_por'].values
diferencia = SOCIALES['Diferencia'].values

s3 = figure(x_range=carreras, plot_height=600, y_range=(0, 100), title="Matriculados en CIENCIAS SOCIALES, PERIODISMO Y DOCUMENTACIÓN",
           toolbar_location=None, tools="", y_axis_label = "Porcentaje de Mujeres")
s3.vbar(x=carreras, top=porcentaje, width=0.3)
s3.xgrid.grid_line_color = None
s3.y_range.start = 0
s3.extra_y_ranges = {"foo": Range1d(start=-40000, end=40000)}
s3.line(x=carreras, y=diferencia, color="yellow", line_width=2, y_range_name="foo")
s3.circle(x=carreras, y=diferencia, color="black", y_range_name="foo")
s3.add_layout(LinearAxis(y_range_name="foo", axis_label="(Nº Mujeres - Nº Hombres)"), 'right')
s3.xaxis.major_label_orientation = math.pi/3
s3.xaxis.axis_label_text_font_style = "bold"
s3.yaxis.axis_label_text_font_style = "italic"
#mid_box = BoxAnnotation(bottom=0, top=49.9, fill_alpha=0.1, fill_color='red')
#s3.add_layout(mid_box)
box = BoxAnnotation(bottom=0, top=25, fill_alpha=0.1, fill_color='red')
s3.add_layout(box)
box = BoxAnnotation(bottom=75, top=100, fill_alpha=0.1, fill_color='red')
s3.add_layout(box)

# NEGOCIOS, ADMINISTRACIÓN Y DERECHO
NEGOCIOS = NEGOCIOS.sort_values(by=['Mujer_por'])
#carreras = NEGOCIOS['Carreras2'].unique()
carreras = NEGOCIOS['Carreras'].unique()
porcentaje = NEGOCIOS['Mujer_por'].values
diferencia = NEGOCIOS['Diferencia'].values

s4 = figure(x_range=carreras, plot_height=600, y_range=(0, 100), title="Matriculados en NEGOCIOS, ADMINISTRACIÓN Y DERECHO",
           toolbar_location=None, tools="", y_axis_label = "Porcentaje de Mujeres")
s4.vbar(x=carreras, top=porcentaje, width=0.3)
s4.xgrid.grid_line_color = None
s4.y_range.start = 0
s4.extra_y_ranges = {"foo": Range1d(start=-40000, end=40000)}
s4.line(x=carreras, y=diferencia, color="yellow", line_width=2, y_range_name="foo")
s4.circle(x=carreras, y=diferencia, color="black", y_range_name="foo")
s4.add_layout(LinearAxis(y_range_name="foo", axis_label="(Nº Mujeres - Nº Hombres)"), 'right')
s4.xaxis.major_label_orientation = math.pi/3
s4.xaxis.axis_label_text_font_style = "bold"
s4.yaxis.axis_label_text_font_style = "italic"
#mid_box = BoxAnnotation(bottom=0, top=49.9, fill_alpha=0.1, fill_color='red')
#s4.add_layout(mid_box)
box = BoxAnnotation(bottom=0, top=25, fill_alpha=0.1, fill_color='red')
s4.add_layout(box)
box = BoxAnnotation(bottom=75, top=100, fill_alpha=0.1, fill_color='red')
s4.add_layout(box)

# CIENCIAS
CIENCIAS = CIENCIAS.sort_values(by=['Mujer_por'])
#carreras = CIENCIAS['Carreras2'].unique()
carreras = CIENCIAS['Carreras'].unique()
porcentaje = CIENCIAS['Mujer_por'].values
diferencia = CIENCIAS['Diferencia'].values

s5 = figure(x_range=carreras, plot_height=600, y_range=(0, 100), title="Matriculados en CIENCIAS",
           toolbar_location=None, tools="", y_axis_label = "Porcentaje de Mujeres")
s5.vbar(x=carreras, top=porcentaje, width=0.3)
s5.xgrid.grid_line_color = None
s5.y_range.start = 0
s5.extra_y_ranges = {"foo": Range1d(start=-40000, end=40000)}
s5.line(x=carreras, y=diferencia, color="yellow", line_width=2, y_range_name="foo")
s5.circle(x=carreras, y=diferencia, color="black", y_range_name="foo")
s5.add_layout(LinearAxis(y_range_name="foo", axis_label="(Nº Mujeres - Nº Hombres)"), 'right')
s5.xaxis.major_label_orientation = math.pi/3
s5.xaxis.axis_label_text_font_style = "bold"
s5.yaxis.axis_label_text_font_style = "italic"
#mid_box = BoxAnnotation(bottom=0, top=49.9, fill_alpha=0.1, fill_color='red')
#s5.add_layout(mid_box)
box = BoxAnnotation(bottom=0, top=25, fill_alpha=0.1, fill_color='red')
s5.add_layout(box)
box = BoxAnnotation(bottom=75, top=100, fill_alpha=0.1, fill_color='red')
s5.add_layout(box)

# INFORMÁTICA
INFORMATICA = INFORMATICA.sort_values(by=['Mujer_por'])
#carreras = INFORMATICA['Carreras2'].unique()
carreras = INFORMATICA['Carreras'].unique()
porcentaje = INFORMATICA['Mujer_por'].values
diferencia = INFORMATICA['Diferencia'].values

s6 = figure(x_range=carreras, plot_height=600, y_range=(0, 100), title="Matriculados en INFORMÁTICA",
           toolbar_location=None, tools="", y_axis_label = "Porcentaje de Mujeres")
s6.vbar(x=carreras, top=porcentaje, width=0.3)
s6.xgrid.grid_line_color = None
s6.y_range.start = 0
s6.extra_y_ranges = {"foo": Range1d(start=-40000, end=40000)}
s6.line(x=carreras, y=diferencia, color="yellow", line_width=2, y_range_name="foo")
s6.circle(x=carreras, y=diferencia, color="black", y_range_name="foo")
s6.add_layout(LinearAxis(y_range_name="foo", axis_label="(Nº Mujeres - Nº Hombres)"), 'right')
s6.xaxis.major_label_orientation = math.pi/3
s6.xaxis.axis_label_text_font_style = "bold"
s6.yaxis.axis_label_text_font_style = "italic"
#mid_box = BoxAnnotation(bottom=0, top=49.9, fill_alpha=0.1, fill_color='red')
#s6.add_layout(mid_box)
box = BoxAnnotation(bottom=0, top=25, fill_alpha=0.1, fill_color='red')
s6.add_layout(box)
box = BoxAnnotation(bottom=75, top=100, fill_alpha=0.1, fill_color='red')
s6.add_layout(box)

# INGENIERÍA, INDUSTRIA Y CONSTRUCCIÓN
INGENIERIA = INGENIERIA.sort_values(by=['Mujer_por'])
#carreras = INGENIERIA['Carreras2'].unique()
carreras = INGENIERIA['Carreras'].unique()
porcentaje = INGENIERIA['Mujer_por'].values
diferencia = INGENIERIA['Diferencia'].values

s7 = figure(x_range=carreras, plot_height=600, y_range=(0, 100), title="Matriculados en INGENIERÍA, INDUSTRIA Y CONSTRUCCIÓN",
           toolbar_location=None, tools="", y_axis_label = "Porcentaje de Mujeres")
s7.vbar(x=carreras, top=porcentaje, width=0.3)
s7.xgrid.grid_line_color = None
s7.y_range.start = 0
s7.extra_y_ranges = {"foo": Range1d(start=-40000, end=40000)}
s7.line(x=carreras, y=diferencia, color="yellow", line_width=2, y_range_name="foo")
s7.circle(x=carreras, y=diferencia, color="black", y_range_name="foo")
s7.add_layout(LinearAxis(y_range_name="foo", axis_label="(Nº Mujeres - Nº Hombres)"), 'right')
s7.xaxis.major_label_orientation = math.pi/3
s7.xaxis.axis_label_text_font_style = "bold"
s7.yaxis.axis_label_text_font_style = "italic"
#mid_box = BoxAnnotation(bottom=0, top=49.9, fill_alpha=0.1, fill_color='red')
#s7.add_layout(mid_box)
box = BoxAnnotation(bottom=0, top=25, fill_alpha=0.1, fill_color='red')
s7.add_layout(box)
box = BoxAnnotation(bottom=75, top=100, fill_alpha=0.1, fill_color='red')
s7.add_layout(box)

# AGRICULTURA
AGRICULTURA = AGRICULTURA.sort_values(by=['Mujer_por'])
#carreras = AGRICULTURA['Carreras2'].unique()
carreras = AGRICULTURA['Carreras'].unique()
porcentaje = AGRICULTURA['Mujer_por'].values
diferencia = AGRICULTURA['Diferencia'].values

s8 = figure(x_range=carreras, plot_height=600, y_range=(0, 100), title="Matriculados en AGRICULTURA",
           toolbar_location=None, tools="", y_axis_label = "Porcentaje de Mujeres")
s8.vbar(x=carreras, top=porcentaje, width=0.3)
s8.xgrid.grid_line_color = None
s8.y_range.start = 0
s8.extra_y_ranges = {"foo": Range1d(start=-40000, end=40000)}
s8.line(x=carreras, y=diferencia, color="yellow", line_width=2, y_range_name="foo")
s8.circle(x=carreras, y=diferencia, color="black", y_range_name="foo")
s8.add_layout(LinearAxis(y_range_name="foo", axis_label="(Nº Mujeres - Nº Hombres)"), 'right')
s8.xaxis.major_label_orientation = math.pi/3
s8.xaxis.axis_label_text_font_style = "bold"
s8.yaxis.axis_label_text_font_style = "italic"
#mid_box = BoxAnnotation(bottom=0, top=49.9, fill_alpha=0.1, fill_color='red')
#s8.add_layout(mid_box)
box = BoxAnnotation(bottom=0, top=25, fill_alpha=0.1, fill_color='red')
s8.add_layout(box)
box = BoxAnnotation(bottom=75, top=100, fill_alpha=0.1, fill_color='red')
s8.add_layout(box)

# SALUD Y SERVICIOS SOCIALES
SALUD = SALUD.sort_values(by=['Mujer_por'])
#carreras = SALUD['Carreras2'].unique()
carreras = SALUD['Carreras'].unique()
porcentaje = SALUD['Mujer_por'].values
diferencia = SALUD['Diferencia'].values

s9 = figure(x_range=carreras, plot_height=600, y_range=(0, 100), title="Matriculados en SALUD Y SERVICIOS SOCIALES",
           toolbar_location=None, tools="", y_axis_label = "Porcentaje de Mujeres")
s9.vbar(x=carreras, top=porcentaje, width=0.3)
s9.xgrid.grid_line_color = None
s9.y_range.start = 0
s9.extra_y_ranges = {"foo": Range1d(start=-40000, end=40000)}
s9.line(x=carreras, y=diferencia, color="yellow", line_width=2, y_range_name="foo")
s9.circle(x=carreras, y=diferencia, color="black", y_range_name="foo")
s9.add_layout(LinearAxis(y_range_name="foo", axis_label="(Nº Mujeres - Nº Hombres)"), 'right')
s9.xaxis.major_label_orientation = math.pi/3
s9.xaxis.axis_label_text_font_style = "bold"
s9.yaxis.axis_label_text_font_style = "italic"
#mid_box = BoxAnnotation(bottom=0, top=49.9, fill_alpha=0.1, fill_color='red')
#s9.add_layout(mid_box)
box = BoxAnnotation(bottom=0, top=25, fill_alpha=0.1, fill_color='red')
s9.add_layout(box)
box = BoxAnnotation(bottom=75, top=100, fill_alpha=0.1, fill_color='red')
s9.add_layout(box)

# SERVICIOS
SERVICIOS = SERVICIOS.sort_values(by=['Mujer_por'])
#carreras = SERVICIOS['Carreras2'].unique()
carreras = SERVICIOS['Carreras'].unique()
porcentaje = SERVICIOS['Mujer_por'].values
diferencia = SERVICIOS['Diferencia'].values

s10 = figure(x_range=carreras, plot_height=600, y_range=(0, 100), title="Matriculados en SERVICIOS",
           toolbar_location=None, tools="", y_axis_label = "Porcentaje de Mujeres")
s10.vbar(x=carreras, top=porcentaje, width=0.3)
s10.xgrid.grid_line_color = None
s10.y_range.start = 0
s10.extra_y_ranges = {"foo": Range1d(start=-40000, end=40000)}
s10.line(x=carreras, y=diferencia, color="yellow", line_width=2, y_range_name="foo")
s10.circle(x=carreras, y=diferencia, color="black", y_range_name="foo")
s10.add_layout(LinearAxis(y_range_name="foo", axis_label="(Nº Mujeres - Nº Hombres)"), 'right')
s10.xaxis.major_label_orientation = math.pi/3
s10.xaxis.axis_label_text_font_style = "bold"
s10.yaxis.axis_label_text_font_style = "italic"
#mid_box = BoxAnnotation(bottom=0, top=49.9, fill_alpha=0.1, fill_color='red')
#s10.add_layout(mid_box)
box = BoxAnnotation(bottom=0, top=25, fill_alpha=0.1, fill_color='red')
s10.add_layout(box)
box = BoxAnnotation(bottom=75, top=100, fill_alpha=0.1, fill_color='red')
s10.add_layout(box)


# ### Top de carreras universitarias donde hay paridad porcentual en alumnos matriculados

# In[129]:


Paridad = Datos[((Datos['Mujer_por'] > 48) & (Datos['Mujer_por'] < 52))]
Paridad = Paridad.sort_values(by=['Matriculados'], ascending=False)
Paridad.columns = ['Carrera', 'Matriculados', 'Mujeres', 'Hombres', 'Diferencia',
       '% del Total de Matriculados', '% Mujeres', '% Hombres', 'Rama']
Paridad.drop(columns=['Diferencia'])


# ### Porcentaje de Mujeres matriculadas por carrera y la diferencia en matrículas con respecto a hombres

# In[81]:


grid = gridplot([[s1, s2, s3, s4, s5], [s6, s7, s8, s9, s10]])
show(grid)

