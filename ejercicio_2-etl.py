import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import numpy as np
import time

# Funcion auxiliar
def custom_date_format(date_str):
    """
    Convierte fechas en formato 'dd/mm/yyyy' a 'yyyy-mm-dd 00:00:00'.
    """
    if pd.isna(date_str):
        return np.nan  # Devuelve NaN si el valor es nulo
    try:
        # Intenta convertir fechas con formato 'dd/mm/yyyy'
        return pd.to_datetime(date_str, format='%d/%m/%Y').strftime('%Y-%m-%d 00:00:00')
    except ValueError:
        # Si no es 'dd/mm/yyyy', devuelve el valor original convertido a datetime (si es posible)
        return pd.to_datetime(date_str, errors='coerce').strftime('%Y-%m-%d 00:00:00')


# Obtener la ruta absoluta de los archivos
properties_path = os.path.abspath('dataset-input/properties.csv')
bookings_path = os.path.abspath('dataset-input/booking.csv')

# Cargar datasets
properties_df = pd.read_csv(properties_path)
bookings_df = pd.read_csv(bookings_path)

# Paso 1: Eliminar la columna 'Capacity' de properties
properties_df.drop(columns=['Capacity'], inplace=True)
# Reemplazar 'Apa' por 'Apartment' en 'PropertyType'
properties_df['PropertyType'].replace('Apa', 'Apartment', inplace=True)
# Filtrar 'PropertyType' para que solo acepte 'Apartment' y 'House'
properties_df = properties_df[properties_df['PropertyType'].isin(['Apartment', 'House'])]

# Eliminar duplicados de ambos datasets
properties_df.drop_duplicates(inplace=True)
bookings_df.drop_duplicates(inplace=True)

print("DESARROLLO DEL ETL")
print("DATA SOURCE:")
print(properties_df)
print(bookings_df)

# Aplicar la función auxiliar a las columnas
properties_df['ReadyDate'] = properties_df['ReadyDate'].apply(custom_date_format)
bookings_df['BookingCreatedDate'] = bookings_df['BookingCreatedDate'].apply(custom_date_format)
bookings_df['ArrivalDate'] = bookings_df['ArrivalDate'].apply(custom_date_format)
bookings_df['DepartureDate'] = bookings_df['DepartureDate'].apply(custom_date_format)

# Paso 2: Realizar un left join entre properties y bookings usando 'PropertyId'
merged_df = pd.merge(bookings_df, properties_df, on='PropertyId', how='left')

# Paso 3: Reordenar las columnas en el dataset final
final_columns = [
    'PropertyId', 'RealProperty', 'Square', 'PropertyType', 'NumBedrooms', 'ReadyDate',
    'Property_BookingId', 'BookingCreatedDate', 'ArrivalDate', 'DepartureDate',
    'Adults', 'Children', 'Infants', 'Persons', 'NumNights', 'Channel',
    'RoomRate', 'CleaningFee', 'Revenue', 'ADR', 'TouristTax', 'TotalPaid'
]
final_df = merged_df[final_columns]

# Guardar el dataset final
final_df.to_csv('dataset-output/final_dataset-ejercicio_2.csv', index=False)

print("DATA SET FINAL:")
print(final_df)

# --- Parte de EDA ---
# Paso 4: Descripción general del dataset
print("ANALISIS EDA")
print("Primeras filas del dataset:")
print(final_df.head())

print("\nResumen estadístico:")
print(final_df.describe())

print("\nInformación del dataset:")
print(final_df.info())

# Paso 5: Verificar valores nulos
print("\nValores nulos por columna:")
print(final_df.isnull().sum())

# Eliminar o rellenar valores nulos si es necesario
# final_df.dropna(inplace=True)  # Eliminar filas con nulos
# final_df.fillna(0, inplace=True)  # Rellenar nulos con 0 (si es apropiado)

# Paso 6: Distribución de valores en columnas categóricas
print("\nDistribución de PropertyType:")
print(final_df['PropertyType'].value_counts())

print("\nDistribución de Channel:")
print(final_df['Channel'].value_counts())

# Paso 7: Análisis de fechas
# Convertir columnas de fechas al formato datetime
final_df['BookingCreatedDate'] = pd.to_datetime(final_df['BookingCreatedDate'])
final_df['ArrivalDate'] = pd.to_datetime(final_df['ArrivalDate'])
final_df['DepartureDate'] = pd.to_datetime(final_df['DepartureDate'])

print("\nRango de fechas de ArrivalDate:")
print(final_df['ArrivalDate'].min(), final_df['ArrivalDate'].max())

# Agregar columnas de año y mes
final_df['BookingYear'] = final_df['BookingCreatedDate'].dt.year
final_df['BookingMonth'] = final_df['BookingCreatedDate'].dt.month

print("\nNúmero de reservas por mes:")
print(final_df.groupby('BookingMonth').size())

# --- Visualizaciones básicas ---

# Histograma de la columna RoomRate
plt.figure(figsize=(10, 6))
sns.histplot(final_df['RoomRate'], kde=True)
plt.title('Distribución de RoomRate')
plt.savefig('dataset-output/analisis-distribucion_roomrate.png')  # Guardar imagen
plt.show()
plt.close()

# Gráfico de barras para ver el número de propiedades por tipo
plt.figure(figsize=(10, 6))
sns.countplot(data=final_df, x='PropertyType')
plt.title('Número de propiedades por tipo')
plt.savefig('dataset-output/analisis-numerode_propiedades_por_tipo.png')  # Guardar imagen
plt.show()
plt.close()

# Paso 8: Guardar insights del EDA en archivos CSV
final_df.isnull().sum().to_csv('dataset-output/analisis-missing_values_summary.csv')

