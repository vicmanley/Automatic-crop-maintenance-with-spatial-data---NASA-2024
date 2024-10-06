import math
import requests
from urllib.parse import urlencode
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
import h5py
import os
import numpy as np
from geopy.distance import geodesic

# Función para generar los puntos del círculo basado en el radio
def generar_puntos_circulo(lat, lon, radio_km, num_puntos=100):
    puntos = []
    # La circunferencia de la Tierra en km
    circunferencia_tierra = 40075
    # Conversión de km a grados
    radio_grados = (radio_km / circunferencia_tierra) * 360
    for i in range(num_puntos):
        angulo = math.radians(float(i) / num_puntos * 360)
        punto_lat = lat + (radio_grados * math.cos(angulo))
        punto_lon = lon + (radio_grados * math.sin(angulo)) / math.cos(math.radians(lat))
        puntos.append(f"{punto_lat},{punto_lon}")
    return "|".join(puntos)

def bounding_box(latitude, longitude, radius_km):
    # Definir el punto de origen
    origin = (latitude, longitude)
    
    # Calcular el punto más al norte
    north = geodesic(kilometers=radius_km).destination(origin, 0)  # 0 grados es hacia el norte
    # Calcular el punto más al sur
    south = geodesic(kilometers=radius_km).destination(origin, 180)  # 180 grados es hacia el sur
    # Calcular el punto más al este
    east = geodesic(kilometers=radius_km).destination(origin, 90)  # 90 grados es hacia el este
    # Calcular el punto más al oeste
    west = geodesic(kilometers=radius_km).destination(origin, 270)  # 270 grados es hacia el oeste
    
    # Devolver la caja delimitadora
    Salida = [north.latitude,south.latitude,east.longitude,west.longitude]
    return Salida
#recuerda:
#Salida[0] norte
#Salida[1] sur
#Salida[2] este 
#Salida[3] oeste

# Credenciales de NASA Earthdata (asegúrate de tener una cuenta y usar tu usuario y contraseña)
# Tu Bearer Token
bearer_token = "eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6ImV4YW1lbmptdWYiLCJleHAiOjE3MzMxNjQ1NDYsImlhdCI6MTcyNzk4MDU0NiwiaXNzIjoiaHR0cHM6Ly91cnMuZWFydGhkYXRhLm5hc2EuZ292In0.bolB3Y6o-ydpR4MgnakyL0v0Hbluhrp_gRwyOH_b7aspQnv_DOK1jZgZSJEwqm_zCqnz1MXMg1FlLbgTUXtp7xEDl1OFLFpe3J9GArWPBYOPlRhatmB5ISrkyJv0KsWDvckn9ADAwbjvvJ2_2W-XffZUccoe_Rbo8JbOyDoI-oMH1qi8oK34Ye01nsjPHRpZLGjv8Yt8yw6ZJQPYJYWr0PNInRxEDOXg8SZLu2i05cbBwgi_HNWC0LOIJbDb-pyK8RAB41pGwgLNXEMFyCF9zFhB0IOWZEJG1Mv6CYDqec2Vx5XFBLrZ36-YTXm_NDIX_uN7aa75SvQdMnA1MMbfrg" 

# Configurar el encabezado de la solicitud
headers = {
    "Authorization": f"Bearer {bearer_token}"
}

#numero de lecturas para mostrar
lecturas = 50

# Coordenada de referencia 22.30439356518835, -98.73976381371145 Rancho Santa Margarita SLP
latitud = 19.60820584382566
longitud = -97.13460703391794
radio_km = 50  # Radio de 10 km de sistema de nasa
radio_google = radio_km + 10
num_puntos_circulo = 150  # Número de puntos para definir el círculo

# Generar los puntos del polígono circular
puntos_circulo = generar_puntos_circulo(latitud, longitud, radio_google, num_puntos_circulo)


#Area de coordigo

#delimitador de espacio
Referencia = bounding_box_result = bounding_box(latitud, longitud, radio_km)

# Obtener la fecha actual y el rango temporal (últimas 24 horas)
end_time = datetime.utcnow()
start_time = end_time - timedelta(days=1)
temporal_range = f"{start_time.isoformat()}Z,{end_time.isoformat()}Z"

print("programa de exploracion v0.1")
print("Autor: Juan Ugalde")
print("Proposito: Consultar lo datos de GPM IMERG sobre precipitaciones")

print("Area delimitada para la exploracion de precipitacion")

print(f"Bounding box: Oeste={Referencia[3]}, Sur={Referencia[1]}, Este={Referencia[2]}, Norte={Referencia[0]}")

# Construir la URL de la consulta con parámetros espaciales y temporales
cmr_url = "https://cmr.earthdata.nasa.gov/search/granules.json"
params = {
    "provider": "GES_DISC",  # Proveedor de datos
    "short_name": "GPM_3IMERGHHE",  # Dataset de precipitación (GPM IMERG)
    "bounding_box": f"{Referencia[3]},{Referencia[1]},{Referencia[2]},{Referencia[0]}",  # Caja delimitadora
    "temporal": temporal_range,  # Rango temporal de las últimas 24 horas
    "page_size": 1,  # Número de resultados, era 5
    "sort_key[]": "-start_date"  # Ordenar por fecha, los más recientes primero
}

# Hacer la solicitud al CMR
response = requests.get(cmr_url, params=params,headers=headers)

#creamos variable para almacenar puntos de medida

puntos_adicionales = []

# Verificar la respuesta
if response.status_code == 200:
    granules = response.json()
    if granules['feed']['entry']:
        for granule in granules['feed']['entry']:
            print(f"Title: {granule['title']}")
            print(f"Start Time: {granule['time_start']}")
            print(f"End Time: {granule['time_end']}")
            # Obtener la URL de descarga de los datos
            data_link = next((link['href'] for link in granule['links'] if 'href' in link and 'data' in link['href']), None)
            if data_link:
                print(f"Download URL: {data_link}")
                
                # Descargar el archivo de datos con autenticación
                response_file = requests.get(data_link, headers=headers)

                # Verificar que la descarga fue exitosa
                if response_file.status_code == 200:
                    file_name = data_link.split('/')[-1]  # Nombre del archivo
                    with open(file_name, 'wb') as f:
                        f.write(response_file.content)
                    print(f"Archivo descargado: {file_name}")

                    with h5py.File(file_name, 'r') as hdf:
                        # Acceder a los datasets de precipitación, latitud, longitud y tiempo
                        precipitation = hdf['Grid/precipitation'][:]
                        latitudes = hdf['Grid/lat'][:]
                        longitudes = hdf['Grid/lon'][:]
                        times = hdf['Grid/time'][:]

                        # Valores Fill para precipitación (valores faltantes)
                        fill_value = hdf['Grid/precipitation'].attrs['_FillValue']
                        
                        # Iterar sobre las primeras 10 lecturas, saltando los valores Fill
                        count = 0
                        for time_idx in range(len(times)):
                            for lat_idx in range(len(latitudes)):
                                for lon_idx in range(len(longitudes)):
                                    precip_value = precipitation[time_idx, lon_idx, lat_idx]
                                    
                                    lat_value = latitudes[lat_idx]
                                    lon_value = longitudes[lon_idx]

                                    # Verificar si las coordenadas están dentro del rango especificado por bounding_box
                                    
                                    if ( lat_value <= Referencia[0] and Referencia[1] <= lat_value and Referencia[3] <= lon_value and lon_value <= Referencia[2] ):
                                        # Convertir el tiempo de "seconds since 1980-01-06" a una fecha legible
                                        time_value = times[time_idx]  # Dependiendo del formato, puedes hacer más conversiones
                                        time_readable = np.datetime64('1980-01-06') + np.timedelta64(int(time_value), 's')

                                        # Imprimir el valor en el formato deseado
                                        print(f"Tiempo: {time_readable}, Coordenadas: ({lat_value}, {lon_value}), Precipitación: {precip_value} mm/hr")
                                        # Almacenar las coordenadas en la lista
                                        puntos_adicionales.append((lat_value, lon_value))

                                        # Incrementar el contador de lecturas válidas
                                        count += 1

                                # Detener después de las primeras 10 lecturas válidas
                                    if count >= lecturas:
                                        break
                                if count >= lecturas:
                                    break
                            if count >= lecturas:
                                break
                    
                    # Eliminar el archivo descargado para limpieza
                    #os.remove(file_name)
                else:
                    print(f"Error al descargar el archivo: {response_file.status_code}")
            print("------")
    else:
        print("No se encontraron datos para los parámetros especificados.")
else:
    print(f"Error en la solicitud: {response.status_code}")

# Coordenadas de los puntos adicionales que deseas dibujar
# Añade aquí las coordenadas de los puntos que quieras destacar
print("puntos a colocar en la imagen: ")
print(puntos_adicionales)

# Crear la cadena de puntos adicionales en el formato adecuado para la API
marcadores = "|".join([f"{lat},{lon}" for lat, lon in puntos_adicionales])

# Parámetros para la solicitud a Google Static Maps API
api_key = "AIzaSyB5EyCxzzvpsWx9xUZ_2aUnvbNtXgEej6Q"  # Reemplaza con tu clave de API
base_url = "https://maps.googleapis.com/maps/api/staticmap?"

params = {
    "center": f"{latitud},{longitud}",  # Centro del mapa
    "zoom": 9,  # Nivel de zoom
    "size": "1000x1000",  # Tamaño de la imagen
    "maptype": "satellite",  # Vista satélite
    "path": f"color:0x0000ff80|weight:2|fillcolor:0x0000ff40|{puntos_circulo}",  # Polígono circular
    "markers": f"color:red|label:P|{marcadores}",  # Añadir puntos en las coordenadas adicionales
    "key": api_key  # Tu clave de API
}

params_comunes = {
    "center": f"{latitud},{longitud}",  # Centro del mapa
    "zoom": 9,  # Nivel de zoom
    "size": "1000x1000",  # Tamaño de la imagen (600x600 píxeles)
    "maptype": "satellite",  # Vista satélite
    "key": api_key  # Tu clave de API
}

params_comunes_circulo = {
    "center": f"{latitud},{longitud}",  # Centro del mapa
    "zoom": 9,  # Nivel de zoom
    "size": "1000x1000",  # Tamaño de la imagen (600x600 píxeles)
    "maptype": "satellite",  # Vista satélite
    "path": f"color:0x0000ff80|weight:2|fillcolor:0x0000ff40|{puntos_circulo}",  # Polígono circular
    "key": api_key  # Tu clave de API
}

# Construir la URL con los parámetros
url = base_url + urlencode(params)

# Hacer la solicitud para obtener la imagen
response = requests.get(url)



# Guardar la imagen en un archivo con Circulo y coordenadas
if response.status_code == 200:
    with open("mapa_circular_con_puntos.png", "wb") as f:
        f.write(response.content)
    print("Imagen descargada correctamente: mapa_circular_con_puntos.png")
else:
    print(f"Error al obtener la imagen: {response.status_code}")
    


# Hacer la solicitud para obtener la imagen sin el círculo
url_sin_circulo =  base_url + urlencode(params_comunes)
response_sin_circulo = requests.get(url_sin_circulo)




# Guardar la imagen sin el círculo
if response_sin_circulo.status_code == 200:
    with open("mapa_sin_circulo.png", "wb") as f:
        f.write(response_sin_circulo.content)
    print("Imagen sin círculo descargada correctamente: mapa_sin_circulo.png")
else:
    print(f"Error al obtener la imagen sin círculo: {response_sin_circulo.status_code}")
    
    
# Hacer la solicitud para obtener la imagen sin el círculo
url_con_circulo =  base_url + urlencode(params_comunes_circulo)
response_con_circulo = requests.get(url_con_circulo)


# Guardar la imagen sin el círculo
if response_con_circulo.status_code == 200:
    with open("mapa_con_circulo.png", "wb") as f:
        f.write(response_con_circulo.content)
    print("Imagen sin círculo descargada correctamente: mapa_con_circulo.png")
else:
    print(f"Error al obtener la imagen sin círculo: {response_con_circulo.status_code}")