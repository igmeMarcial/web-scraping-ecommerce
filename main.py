
import requests
import json
import time 

##https://www.plazavea.com.pe/api/catalog_system/pub/products/search?fq=C:/678/686/&_from=2499&_to=2519&O=OrderByScoreDESC&
# base_url = "https://www.plazavea.com.pe/api/catalog_system/pub/products/search?fq=C:/678/686/&_from=0&_to=1&O=OrderByScoreDESC&"
base_url = "https://www.plazavea.com.pe/api/catalog_system/pub/products/search?fq=C:/678/686/&O=OrderByScoreDESC&"


def get_all_products(base_url):
    all_products = []
    step = 50  # Tamaño de cada lote de productos, según lo permitido por la API
    start = 0  # Comenzamos desde el primer producto
    
    while True:
        # Ajustar los parámetros _from y _to en cada solicitud
        url = f"{base_url}_from={start}&_to={start + step - 1}"
        
        try:
            # Realizar la solicitud GET
            response = requests.get(url)
            response.raise_for_status()  # Lanzar excepción si ocurre un error HTTP
            
            # Convertir la respuesta a JSON
            products = response.json()
            
            # Si no hay más productos, salir del bucle
            if not products:
                break
            
            # Añadir los productos obtenidos a la lista total
            all_products.extend(products)
            print(f"Fetched products from {start} to {start + step - 1}")
            
            # Incrementar el inicio para la próxima solicitud
            start += step
            time.sleep(2)
        
        except requests.exceptions.HTTPError as http_err:
            print(f"Error en la solicitud HTTP: {http_err}")
            break
        except Exception as err:
            print(f"Error inesperado: {err}")
            break

    return all_products
            
            
        
    
    
# Llamada a la función y mostrar los resultados
products = get_all_products(base_url)
# print(products.l)

print(f"Total de productos obtenidos: {len(products)}")



