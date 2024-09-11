import requests
import json
import base64
from urllib.parse import urlparse, parse_qs
import urllib.parse
import time


def obtener_precio_y_calcular_porcentaje(product):
    # Obtener precios de venta y lista
    selling_price_low = (
        product.get("priceRange", {}).get("sellingPrice", {}).get("lowPrice")
    )
    list_price_low = product.get("priceRange", {}).get("listPrice", {}).get("lowPrice")

    selling_price_low = selling_price_low if selling_price_low is not None else 0
    list_price_low = list_price_low if list_price_low is not None else 0

    if list_price_low > 0:
        descuento_low = ((list_price_low - selling_price_low) / list_price_low) * 100
    else:
        descuento_low = (
            0  # Si el precio de lista es 0 o no es válido, el descuento es 0
        )

    return {
        "selling_price_low": selling_price_low,
        "list_price_low": list_price_low,
        "descuento_low": descuento_low,
    }


def separate_url_params(url):
    # Parsear la URL y obtener sus componentes
    parsed_url = urlparse(url)

    # Retornar el esquema, red y ruta, ignorando los parámetros de consulta
    return parsed_url.scheme, parsed_url.netloc, parsed_url.path


def decode_graphql_variables(url):
    # Extraer el parámetro 'variables' de la URL
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    extensions_value = query_params.get("extensions", [])[0]

    # Decodificar el JSON
    extensions_json = urllib.parse.unquote(extensions_value)
    extensions_dict = json.loads(extensions_json)

    # Obtener el valor de 'variables'
    variables_base64 = extensions_dict.get("variables", "")
    if not variables_base64:
        raise ValueError('El parámetro "variables" no se encuentra en la URL.')
    # print(f"Valor base64 de 'variables': {variables_base64}")  # Mensaje de depuración
    # Decodificar la cadena Base64
    try:
        variables_json = base64.b64decode(variables_base64).decode("utf-8")
        # print("Cadena decodificada:", variables_json)  # Imprimir el JSON decodificado
    except Exception as e:
        raise ValueError("Error al decodificar la cadena Base64: " + str(e))

    # Analizar el JSON decodificado
    try:
        variables = json.loads(variables_json)
        return variables
    except json.JSONDecodeError as e:
        raise ValueError("Error al analizar el JSON decodificado: " + str(e))


# https://www.electrolux.com.pe/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=es-PE&operationName=productSearchV3&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%228e3fd5f65d7d83516bfea23051b11e7aa469d85f26906f27e18afbee52c56ce4%22%2C%22sender%22%3A%22vtex.store-resources%400.x%22%2C%22provider%22%3A%22vtex.search-graphql%400.x%22%7D%2C%22variables%22%3A%22eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6ZmFsc2UsInNrdXNGaWx0ZXIiOiJGSVJTVF9BVkFJTEFCTEUiLCJzaW11bGF0aW9uQmVoYXZpb3IiOiJkZWZhdWx0IiwiaW5zdGFsbG1lbnRDcml0ZXJpYSI6Ik1BWF9XSVRIT1VUX0lOVEVSRVNUIiwicHJvZHVjdE9yaWdpblZ0ZXgiOnRydWUsIm1hcCI6ImMiLCJxdWVyeSI6InJlZnJpZ2VyYWNpb24iLCJvcmRlckJ5IjoiT3JkZXJCeVRvcFNhbGVERVNDIiwiZnJvbSI6MTIsInRvIjoyMywic2VsZWN0ZWRGYWNldHMiOlt7ImtleSI6ImMiLCJ2YWx1ZSI6InJlZnJpZ2VyYWNpb24ifV0sIm9wZXJhdG9yIjoiYW5kIiwiZnV6enkiOiIwIiwic2VhcmNoU3RhdGUiOm51bGwsImZhY2V0c0JlaGF2aW9yIjoiU3RhdGljIiwiY2F0ZWdvcnlUcmVlQmVoYXZpb3IiOiJkZWZhdWx0Iiwid2l0aEZhY2V0cyI6ZmFsc2UsImFkdmVydGlzZW1lbnRPcHRpb25zIjp7InNob3dTcG9uc29yZWQiOnRydWUsInNwb25zb3JlZENvdW50IjozLCJhZHZlcnRpc2VtZW50UGxhY2VtZW50IjoidG9wX3NlYXJjaCIsInJlcGVhdFNwb25zb3JlZFByb2R1Y3RzIjp0cnVlfX0%3D%22%7D


# Headers si son necesarios
headers = {"Content-Type": "application/json"}
# Parámetros comunes
paramsComunes = {
    "workspace": "master",
    "maxAge": "short",
    "appsEtag": "remove",
    "domain": "store",
    "locale": "es-PE",
    "operationName": "productSearchV3",
    # Falta agregar 'extensions' y 'variables' si se quieren incluir como parte de los parámetros
}


def fetch_products(base_url, urlVariables, params):
    all_products = []
    from_index = 0
    batch_size = 24

    while True:
        try:
            urlVariables["from"] = from_index
            urlVariables["to"] = from_index + batch_size - 1
            # Hacer la solicitud

            variables_base64 = base64.b64encode(
                json.dumps(urlVariables).encode()
            ).decode()
            # Ajusta las extensiones con variables_base64
            params["extensions"] = json.dumps(
                {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "8e3fd5f65d7d83516bfea23051b11e7aa469d85f26906f27e18afbee52c56ce4",
                        "sender": "vtex.store-resources@0.x",
                        "provider": "vtex.search-graphql@0.x",
                    },
                    "variables": variables_base64,
                }
            )

            response = requests.get(base_url, params=params, headers=headers)
            data = response.json()

            # Debug: imprimir la respuesta completa para verificar la estructura
            # print("Respuesta completa:", json.dumps(data, indent=2))

            # Obtener productos
            products = data.get("data", {}).get("productSearch", {}).get("products", [])
            for product in products:
                precios_y_descuentos = obtener_precio_y_calcular_porcentaje(product)
                if precios_y_descuentos["descuento_low"] > 70:
                    print("==========================")
                    name = product.get("productName")
                    urlProduct = product.get("linkText")

                    print(
                        f"{name}: {precios_y_descuentos['descuento_low']}% de descuento"
                    )
                    print(f"https://www.electrolux.com.pe/{urlProduct}/p")

            all_products.extend(products)

            # Si no hay más productos, detener
            if not products:
                break

            # Incrementar el índice para la siguiente página
            from_index += batch_size
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud: {e}")
            break
        except ValueError as e:
            print(f"Error al procesar la respuesta JSON: {e}")
            break
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            break

    return all_products

    # Iterar sobre las URLs y hacer fetch de productos


all_products_total = []


# lavadoras
# refrigeradoras
# cosina
# Aspiradoras
urls = [
    "https://www.electrolux.com.pe/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=es-PE&__bindingId=0b440534-f784-49bb-8863-fddb6a3c9ea9&operationName=productSearchV3&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%228e3fd5f65d7d83516bfea23051b11e7aa469d85f26906f27e18afbee52c56ce4%22%2C%22sender%22%3A%22vtex.store-resources%400.x%22%2C%22provider%22%3A%22vtex.search-graphql%400.x%22%7D%2C%22variables%22%3A%22eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6ZmFsc2UsInNrdXNGaWx0ZXIiOiJGSVJTVF9BVkFJTEFCTEUiLCJzaW11bGF0aW9uQmVoYXZpb3IiOiJkZWZhdWx0IiwiaW5zdGFsbG1lbnRDcml0ZXJpYSI6Ik1BWF9XSVRIT1VUX0lOVEVSRVNUIiwicHJvZHVjdE9yaWdpblZ0ZXgiOnRydWUsIm1hcCI6ImMiLCJxdWVyeSI6ImxhdmFkbyIsIm9yZGVyQnkiOiJPcmRlckJ5VG9wU2FsZURFU0MiLCJmcm9tIjoyNCwidG8iOjM1LCJzZWxlY3RlZEZhY2V0cyI6W3sia2V5IjoiYyIsInZhbHVlIjoibGF2YWRvIn1dLCJvcGVyYXRvciI6ImFuZCIsImZ1enp5IjoiMCIsInNlYXJjaFN0YXRlIjpudWxsLCJmYWNldHNCZWhhdmlvciI6IlN0YXRpYyIsImNhdGVnb3J5VHJlZUJlaGF2aW9yIjoiZGVmYXVsdCIsIndpdGhGYWNldHMiOmZhbHNlLCJhZHZlcnRpc2VtZW50T3B0aW9ucyI6eyJzaG93U3BvbnNvcmVkIjp0cnVlLCJzcG9uc29yZWRDb3VudCI6MywiYWR2ZXJ0aXNlbWVudFBsYWNlbWVudCI6InRvcF9zZWFyY2giLCJyZXBlYXRTcG9uc29yZWRQcm9kdWN0cyI6dHJ1ZX19%22%7D",
    "https://www.electrolux.com.pe/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=es-PE&operationName=productSearchV3&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%228e3fd5f65d7d83516bfea23051b11e7aa469d85f26906f27e18afbee52c56ce4%22%2C%22sender%22%3A%22vtex.store-resources%400.x%22%2C%22provider%22%3A%22vtex.search-graphql%400.x%22%7D%2C%22variables%22%3A%22eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6ZmFsc2UsInNrdXNGaWx0ZXIiOiJGSVJTVF9BVkFJTEFCTEUiLCJzaW11bGF0aW9uQmVoYXZpb3IiOiJkZWZhdWx0IiwiaW5zdGFsbG1lbnRDcml0ZXJpYSI6Ik1BWF9XSVRIT1VUX0lOVEVSRVNUIiwicHJvZHVjdE9yaWdpblZ0ZXgiOnRydWUsIm1hcCI6ImMiLCJxdWVyeSI6InJlZnJpZ2VyYWNpb24iLCJvcmRlckJ5IjoiT3JkZXJCeVRvcFNhbGVERVNDIiwiZnJvbSI6MzYsInRvIjo0Nywic2VsZWN0ZWRGYWNldHMiOlt7ImtleSI6ImMiLCJ2YWx1ZSI6InJlZnJpZ2VyYWNpb24ifV0sIm9wZXJhdG9yIjoiYW5kIiwiZnV6enkiOiIwIiwic2VhcmNoU3RhdGUiOm51bGwsImZhY2V0c0JlaGF2aW9yIjoiU3RhdGljIiwiY2F0ZWdvcnlUcmVlQmVoYXZpb3IiOiJkZWZhdWx0Iiwid2l0aEZhY2V0cyI6ZmFsc2UsImFkdmVydGlzZW1lbnRPcHRpb25zIjp7InNob3dTcG9uc29yZWQiOnRydWUsInNwb25zb3JlZENvdW50IjozLCJhZHZlcnRpc2VtZW50UGxhY2VtZW50IjoidG9wX3NlYXJjaCIsInJlcGVhdFNwb25zb3JlZFByb2R1Y3RzIjp0cnVlfX0%3D%22%7D",
    "https://www.electrolux.com.pe/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=es-PE&operationName=productSearchV3&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%228e3fd5f65d7d83516bfea23051b11e7aa469d85f26906f27e18afbee52c56ce4%22%2C%22sender%22%3A%22vtex.store-resources%400.x%22%2C%22provider%22%3A%22vtex.search-graphql%400.x%22%7D%2C%22variables%22%3A%22eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6ZmFsc2UsInNrdXNGaWx0ZXIiOiJGSVJTVF9BVkFJTEFCTEUiLCJzaW11bGF0aW9uQmVoYXZpb3IiOiJkZWZhdWx0IiwiaW5zdGFsbG1lbnRDcml0ZXJpYSI6Ik1BWF9XSVRIT1VUX0lOVEVSRVNUIiwicHJvZHVjdE9yaWdpblZ0ZXgiOnRydWUsIm1hcCI6ImMiLCJxdWVyeSI6ImNvY2luYSIsIm9yZGVyQnkiOiJPcmRlckJ5VG9wU2FsZURFU0MiLCJmcm9tIjoyNCwidG8iOjM1LCJzZWxlY3RlZEZhY2V0cyI6W3sia2V5IjoiYyIsInZhbHVlIjoiY29jaW5hIn1dLCJvcGVyYXRvciI6ImFuZCIsImZ1enp5IjoiMCIsInNlYXJjaFN0YXRlIjpudWxsLCJmYWNldHNCZWhhdmlvciI6IlN0YXRpYyIsImNhdGVnb3J5VHJlZUJlaGF2aW9yIjoiZGVmYXVsdCIsIndpdGhGYWNldHMiOmZhbHNlLCJhZHZlcnRpc2VtZW50T3B0aW9ucyI6eyJzaG93U3BvbnNvcmVkIjp0cnVlLCJzcG9uc29yZWRDb3VudCI6MywiYWR2ZXJ0aXNlbWVudFBsYWNlbWVudCI6InRvcF9zZWFyY2giLCJyZXBlYXRTcG9uc29yZWRQcm9kdWN0cyI6dHJ1ZX19%22%7D",
    "https://www.electrolux.com.pe/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=es-PE&operationName=productSearchV3&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%228e3fd5f65d7d83516bfea23051b11e7aa469d85f26906f27e18afbee52c56ce4%22%2C%22sender%22%3A%22vtex.store-resources%400.x%22%2C%22provider%22%3A%22vtex.search-graphql%400.x%22%7D%2C%22variables%22%3A%22eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6ZmFsc2UsInNrdXNGaWx0ZXIiOiJGSVJTVF9BVkFJTEFCTEUiLCJzaW11bGF0aW9uQmVoYXZpb3IiOiJkZWZhdWx0IiwiaW5zdGFsbG1lbnRDcml0ZXJpYSI6Ik1BWF9XSVRIT1VUX0lOVEVSRVNUIiwicHJvZHVjdE9yaWdpblZ0ZXgiOnRydWUsIm1hcCI6ImMiLCJxdWVyeSI6ImNvY2luYSIsIm9yZGVyQnkiOiJPcmRlckJ5VG9wU2FsZURFU0MiLCJmcm9tIjoxMiwidG8iOjIzLCJzZWxlY3RlZEZhY2V0cyI6W3sia2V5IjoiYyIsInZhbHVlIjoiY29jaW5hIn1dLCJvcGVyYXRvciI6ImFuZCIsImZ1enp5IjoiMCIsInNlYXJjaFN0YXRlIjpudWxsLCJmYWNldHNCZWhhdmlvciI6IlN0YXRpYyIsImNhdGVnb3J5VHJlZUJlaGF2aW9yIjoiZGVmYXVsdCIsIndpdGhGYWNldHMiOmZhbHNlLCJhZHZlcnRpc2VtZW50T3B0aW9ucyI6eyJzaG93U3BvbnNvcmVkIjp0cnVlLCJzcG9uc29yZWRDb3VudCI6MywiYWR2ZXJ0aXNlbWVudFBsYWNlbWVudCI6InRvcF9zZWFyY2giLCJyZXBlYXRTcG9uc29yZWRQcm9kdWN0cyI6dHJ1ZX19%22%7D",
]
for url in urls:
    print(f"Iniciando extracción en otra url")
    try:
        # Decodificar los parámetros de la URL
        scheme, netloc, path = separate_url_params(url)
        base_url = f"{scheme}://{netloc}{path}"
        urlVariables = decode_graphql_variables(url)
        products = fetch_products(base_url, urlVariables, paramsComunes)
        # Acumular los productos obtenidos
        all_products_total.extend(products)

    except ValueError as e:
        print(f"Error procesando la URL: {e}")

print(f"Total de productos obtenidos de todas las URLs: {len(all_products_total)}")
