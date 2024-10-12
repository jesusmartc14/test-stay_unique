# test-stay_unique
El repositorio consta de dos ejercicios de prueba. Uno de web scraping y otro de un ETL.
## EJERCICIO 1 
Script de Web Scraping para Booking.com

## Descripción
Este proyecto es un script de web scraping que extrae información sobre hoteles de Booking.com utilizando Selenium. Captura datos como nombres de hoteles, direcciones, precios, puntuaciones y el número de habitaciones para ubicaciones y fechas seleccionadas.

## Configuración del Entorno
Para configurar el entorno para este proyecto, sigue estos pasos:

1. **Instalación de Python**: Asegúrate de tener Python instalado. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

2. **Instalar Bibliotecas Requeridas**: Usa `pip` para instalar las bibliotecas necesarias. Puedes hacerlo ejecutando el siguiente comando en tu terminal:
    pip install selenium webdriver-manager pandas
    
3. **Controlador Web**: El script gestiona automáticamente el Chrome WebDriver usando `webdriver-manager`, por lo que no necesitas descargarlo manualmente. Solo asegúrate de tener Google Chrome instalado.

4. **Estructura del Directorio**: Crea un directorio para el proyecto y navega dentro de él. Debería verse así:
 /dataset-output
    ├── final_scraping-ejercicio_1.csv

## Ejecutando el Script
Para ejecutar el script, sigue estos pasos:

1. Abre un terminal o símbolo del sistema.
2. Navega al directorio donde se encuentra tu script.
3. Ejecuta el script con el siguiente comando:
/dataset-output
    ├── final_scraping-ejercicio_1.csv

4. El script extraerá automáticamente datos de Booking.com y guardará los resultados como un archivo CSV en el directorio `dataset-output`.

## Decisiones de Limpieza de Datos
Durante el proceso de extracción, se tomaron las siguientes decisiones de limpieza de datos:

- **Puntuación**: La puntuación extraída se limpia dividiendo el texto por ":" para obtener solo el valor numérico y reemplazando la coma con un punto para poder convertirla en un número flotante.
- **Datos Faltantes**: Se establecieron valores predeterminados para ciertas columnas, como el número de habitaciones, para simplificar el análisis.

## Descripción del Pipeline ETL
El pipeline de ETL implementado en este proyecto se basa en las siguientes etapas:

1. **Extracción**: Utiliza Selenium para navegar por la página de Booking.com y obtener datos de los hoteles.
2. **Transformación**: Limpia y transforma los datos extraídos, como la puntuación y la estructura de los datos.
3. **Carga**: Guarda los datos limpios en un archivo CSV para su posterior análisis.

## Desafíos y Soluciones
Durante el desarrollo del script, se encontraron los siguientes desafíos:

- **Modales y Pop-ups**: Al iniciar la página, un modal puede interferir con la navegación. Esto se resolvió haciendo clic fuera del modal al inicio del script.
- **Elementos Dinámicos**: Algunos elementos cambian su ubicación después de la primera búsqueda. Para resolver esto, se utilizó `WebDriverWait` para esperar a que los elementos sean clicables antes de interactuar con ellos.

--------------------------------------------------------------------------------------------------------------------------------------------------------
## EJERCICIO 2 
Pipeline ETL y EDA para Conjuntos de Datos de Propiedades y Reservas

*Configuración del Entorno
1. Versión de Python: Asegúrate de tener instalada la versión 3.x de Python.
2. Dependencias: Instala las bibliotecas necesarias utilizando pip (pip install pandas matplotlib seaborn numpy)
3. Estructura del Directorio:
/dataset-input
    ├── properties.csv
    └── booking.csv
/dataset-output
    ├── final_dataset-ejercicio_2.csv
    └── analisis-missing_values_summary.csv
    └── analisis-numerode_propiedades_por_tipo.png
    └── analisis-distribucion_roomrate

*Ejecución del Script
python ejercicio-2.py

*Decisiones de Limpieza de Datos
- Columnas Eliminadas: Se eliminó la columna 'Capacity' del conjunto de datos de propiedades ya que no era necesaria para el análisis.
- Reemplazo de Valores: Se reemplazaron las instancias de 'Apa' por 'Apartment' en la columna 'PropertyType' para mantener la consistencia.
- Filtrado: Se filtró la columna 'PropertyType' para conservar solo 'Apartment' y 'House'.
- Eliminación de Duplicados: Se eliminaron filas duplicadas de ambos conjuntos de datos para asegurar la integridad de los datos.

*Descripción del Pipeline ETL
- Extracción:
Se cargaron los conjuntos de datos de propiedades y reservas desde archivos CSV.
- Transformación:
Se aplicó una función de formateo de fecha personalizada para estandarizar las columnas de fecha.
Se unieron los conjuntos de datos de propiedades y reservas utilizando un left join en 'PropertyId'.
Se reordenaron las columnas en el conjunto de datos combinado para que coincidan con la estructura deseada.
- Carga:
Se guardó el conjunto de datos final como un archivo CSV y se generaron visualizaciones de métricas clave.

* Desafíos y Soluciones
- Problemas de Formato de Fecha: Inicialmente, los formatos de fecha variaban entre los conjuntos de datos, lo que causaba inconsistencias. Creé una función personalizada para estandarizar el formato de fecha a 'yyyy-mm-dd 00:00:00'.
- Unión de Conjuntos de Datos: Durante la operación de left join, algunos IDs de propiedades en el conjunto de reservas no tenían entradas correspondientes en el conjunto de propiedades. Me aseguré de que el análisis tuviera en cuenta estos valores nulos sin afectar la integridad general de los datos.
- Visualización de Datos: Se hicieron ajustes necesarios para crear visualizaciones informativas que representaran con precisión las distribuciones de datos.
