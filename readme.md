## descripcion
este es un ambiente que simula un entorno laboral donde debemos resolver las consignas planteadas en un espacio de tiempo determinado<br>
## contexto
se debe crear un modelo de recomendacion para una start up que provee servicios de agregacon para plataformas de estreaming<br>
los datos estan originalmente en 2 archivos CSV, algunas columnas tienen datos anidados, nulos y sin transformar<br>
## tabla de contenido
1. [Instalación y Requisitos](#instalación-y-requisitos)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Datos y Fuentes](#datos-y-fuentes)
4. [Metodología](#metodología)
5. [Contribución y Colaboración](#contribución-y-colaboración)
6. [Licencia](#autores)




## Instalación y Requisitos
Requisitos:

- Python 3.7 o superior
- pandas
- ydata_profiling
- matplotlib
- scikit-learn

Pasos de instalación:

- Clonar el repositorio: git clone https://github.com/Miguel-David-Llanos-Lopez/PI-1-Henry
- Crear un entorno virtual: python -m venv venv
- Activar el entorno virtual:
- Windows: venv\Scripts\activate
- macOS/Linux: source venv/bin/activate
- Instalar las dependencias: pip install -r requirements.txt
nota: en el requirements.txt no esta ydata_profiling y debe ser instalado con pip install ydata_profiling

## Estructura del Proyecto
data/: Contiene los archivos de datos generados en el proyecto.
notebooks/: Incluye los notebooks de Jupyter con el ETL, EDA y modelos.
main.py: es el codigo fuente de la API
requeriments.txt: contiene los requisitos para el despliegue de la API
README.md: Archivo de documentación del proyecto.

## Datos y Fuentes

los datos originales no se encuentran en este repositorio debido a su gran tamaño pero estan disponibles en: <br>
https://drive.google.com/drive/folders/1X_LdCoGTHJDbD28_dJTxaD4fVuQC9Wt5<br>
https://drive.google.com/drive/u/0/folders/1aSiFQ304eiuEY5YwNl0bZMZVt7qZTkot<br>
nota: ambos enlaces contienen los mismos archivos

## Metodología
se aplicaron metodos de aprendizaje automatico como vectorizacion de palabras y similitud del coseno para crear un minimo producto viable de un algoritmo de recomendacion de peliculas utilizando informacion como el director, la sinopsis "overview", el genero "gender", el titulo "title" entre otros

## autores

este proyecto fue realizado por: Miguel Llanos <br>
Gmail: llanoslopezmigueldavid@gmail.com