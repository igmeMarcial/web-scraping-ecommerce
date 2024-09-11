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
