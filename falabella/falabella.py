from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json


def main():
    def extract_prices(product):
        try:
            # Obtener el precio de evento (precio actual)
            event_price_str = product["prices"][0]["price"][0]
            # Obtener el precio normal (precio anterior)
            normal_price_str = product["prices"][1]["price"][0]

            # Convertir los strings de precios a float, removiendo las comas
            event_price = float(event_price_str.replace(",", ""))
            normal_price = float(normal_price_str.replace(",", ""))

            return event_price, normal_price
        except (IndexError, ValueError) as e:
            # print(f"Error al extraer precios: {e}")
            return None, None

    def calcular_descuento(normal_price: float, event_price: float) -> float:
        """
        Calcula el porcentaje de descuento basado en el precio original (normal_price) y el precio con descuento (event_price).

        Args:
            normal_price (float): Precio original del producto.
            event_price (float): Precio con descuento del producto.

        Returns:
            float: Porcentaje de descuento calculado.
        """
        if normal_price <= 0:
            raise ValueError("El precio original debe ser mayor a 0")

        descuento = ((normal_price - event_price) / normal_price) * 100
        return descuento

    def fetch_products_from_category(base_url, driver, discount):

        page = 1
        all_products = []

        while True:
            url = f"{base_url}&page={page}"
            driver.get(url)

            # Esperar un momento para que la página cargue (mejor usar WebDriverWait si posible)
            time.sleep(2)

            try:
                pre = driver.find_element(By.TAG_NAME, "pre")
                data = pre.text
                # Convertir el texto JSON a un objeto Python
                json_data = json.loads(data)
                products = json_data.get("data", {}).get("results", [])

                if not products:
                    break

                for product in products:
                    display_name = product.get("displayName", "Producto sin nombre")
                    prices = product.get("prices", [])
                    url_product = product.get("url")

                    # Filtrar los precios normal y event
                    event_price, normal_price = extract_prices(product)

                    # Calcular el descuento si ambos precios están presentes
                    if normal_price is not None and event_price is not None:
                        try:
                            descuento = calcular_descuento(normal_price, event_price)
                            if descuento >= discount:
                                print("===============================================")
                                print(f"{display_name}: {descuento:.2f}% de descuento")
                                print(f"URL del producto: {url_product}")
                                print("===============================================")
                        except ValueError as e:
                            print(
                                f"Error calculando descuento para {display_name}: {e}"
                            )
                    else:
                        # print(
                        #     f"{display_name}: No se encontraron precios adecuados para calcular el descuento"
                        # )
                        # print(f"URL del producto: {url_product}")
                        pass

                all_products.extend(products)
                print(f"Fetched products from page {page}")
                page += 1

            except Exception as e:
                print(f"Error: {e}")
                break
        return all_products

    # Options

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # cat4220604/Carteras

    # cat50588/Ropa-de-Cama
    # cat800486/Dormitorio-Infantil
    # cat870548 / Funda-plumon
    # cat4350568 / Joyas
    # CATG11954 / Bebidas-y-licores

    category_urls = [
        "https://www.falabella.com.pe/s/browse/v1/listing/pe?sid=HO_CD_F19_GC_TEC_2768&categoryId=cat40793&categoryName=Tecnologia&pgid=2&pid=799c102f-9b4c-44be-a421-23e366a63b82&zones=IBIS_51%2CPPE3342%2CPPE3361%2CPPE1112%2CPPE3384%2C912_LIMA_2%2CPPE1280%2C150000%2CPPE4%2C912_LIMA_1%2CPPE1279%2C150101%2CPPE344%2CPPE3059%2CPPE2665%2CPPE2492%2CIMP_2%2CPPE3331%2CPPE3357%2CPPE1091%2CPERF_TEST%2CPPE1653%2CPPE2486%2COLVAA_81%2CPPE2815%2CIMP_1%2CPPE3164%2CPPE2918%2CURBANO_83%2CPPE2429%2CPPE3152%2CPPE3479%2CPPE3483%2CPPE3394%2CLIMA_URB1_DIRECTO%2CPPE2511%2CIBIS_19%2CPPE1382%2CIBIS_3PL_83%2CPPE3248",
        "https://www.falabella.com.pe/s/browse/v1/listing/pe?sid=HO_CD_F19_GC_TEC_2768&categoryId=cat13820483&categoryName=Sillas-gamer&pgid=2&pid=799c102f-9b4c-44be-a421-23e366a63b82&zones=IBIS_51%2CPPE3342%2CPPE3361%2CPPE1112%2CPPE3384%2C912_LIMA_2%2CPPE1280%2C150000%2CPPE4%2C912_LIMA_1%2CPPE1279%2C150101%2CPPE344%2CPPE3059%2CPPE2665%2CPPE2492%2CIMP_2%2CPPE3331%2CPPE3357%2CPPE1091%2CPERF_TEST%2CPPE1653%2CPPE2486%2COLVAA_81%2CPPE2815%2CIMP_1%2CPPE3164%2CPPE2918%2CURBANO_83%2CPPE2429%2CPPE3152%2CPPE3479%2CPPE3483%2CPPE3394%2CLIMA_URB1_DIRECTO%2CPPE2511%2CIBIS_19%2CPPE1382%2CIBIS_3PL_83%2CPPE3248",
        "https://www.falabella.com.pe/s/browse/v1/listing/pe?sid=HO_CD_F19_GC_TEC_2768&categoryId=cat760706&categoryName=Celulares-y-Telefonos&pgid=2&pid=799c102f-9b4c-44be-a421-23e366a63b82&zones=IBIS_51%2CPPE3342%2CPPE3361%2CPPE1112%2CPPE3384%2C912_LIMA_2%2CPPE1280%2C150000%2CPPE4%2C912_LIMA_1%2CPPE1279%2C150101%2CPPE344%2CPPE3059%2CPPE2665%2CPPE2492%2CIMP_2%2CPPE3331%2CPPE3357%2CPPE1091%2CPERF_TEST%2CPPE1653%2CPPE2486%2COLVAA_81%2CPPE2815%2CIMP_1%2CPPE3164%2CPPE2918%2CURBANO_83%2CPPE2429%2CPPE3152%2CPPE3479%2CPPE3483%2CPPE3394%2CLIMA_URB1_DIRECTO%2CPPE2511%2CIBIS_19%2CPPE1382%2CIBIS_3PL_83%2CPPE3248",
        "https://www.falabella.com.pe/s/browse/v1/listing/pe?sid=HO_CD_F19_GC_TEC_2768&categoryId=cat40584&categoryName=Electrohogar&pgid=2&pid=799c102f-9b4c-44be-a421-23e366a63b82&zones=IBIS_51%2CPPE3342%2CPPE3361%2CPPE1112%2CPPE3384%2C912_LIMA_2%2CPPE1280%2C150000%2CPPE4%2C912_LIMA_1%2CPPE1279%2C150101%2CPPE344%2CPPE3059%2CPPE2665%2CPPE2492%2CIMP_2%2CPPE3331%2CPPE3357%2CPPE1091%2CPERF_TEST%2CPPE1653%2CPPE2486%2COLVAA_81%2CPPE2815%2CIMP_1%2CPPE3164%2CPPE2918%2CURBANO_83%2CPPE2429%2CPPE3152%2CPPE3479%2CPPE3483%2CPPE3394%2CLIMA_URB1_DIRECTO%2CPPE2511%2CIBIS_19%2CPPE1382%2CIBIS_3PL_83%2CPPE3248",
        "https://www.falabella.com.pe/s/browse/v1/listing/pe?sid=HO_CD_F19_GC_TEC_2768&categoryId=cat1830468&categoryName=Smartwatch-y-wearables&pgid=2&pid=799c102f-9b4c-44be-a421-23e366a63b82&zones=IBIS_51%2CPPE3342%2CPPE3361%2CPPE1112%2CPPE3384%2C912_LIMA_2%2CPPE1280%2C150000%2CPPE4%2C912_LIMA_1%2CPPE1279%2C150101%2CPPE344%2CPPE3059%2CPPE2665%2CPPE2492%2CIMP_2%2CPPE3331%2CPPE3357%2CPPE1091%2CPERF_TEST%2CPPE1653%2CPPE2486%2COLVAA_81%2CPPE2815%2CIMP_1%2CPPE3164%2CPPE2918%2CURBANO_83%2CPPE2429%2CPPE3152%2CPPE3479%2CPPE3483%2CPPE3394%2CLIMA_URB1_DIRECTO%2CPPE2511%2CIBIS_19%2CPPE1382%2CIBIS_3PL_83%2CPPE3248",
        "https://www.falabella.com.pe/s/browse/v1/listing/pe?sid=HO_CD_F19_GC_TEC_2768&categoryId=cat6370558&categoryName=Electrodomesticos-de-Cocina&pgid=2&pid=799c102f-9b4c-44be-a421-23e366a63b82&zones=IBIS_51%2CPPE3342%2CPPE3361%2CPPE1112%2CPPE3384%2C912_LIMA_2%2CPPE1280%2C150000%2CPPE4%2C912_LIMA_1%2CPPE1279%2C150101%2CPPE344%2CPPE3059%2CPPE2665%2CPPE2492%2CIMP_2%2CPPE3331%2CPPE3357%2CPPE1091%2CPERF_TEST%2CPPE1653%2CPPE2486%2COLVAA_81%2CPPE2815%2CIMP_1%2CPPE3164%2CPPE2918%2CURBANO_83%2CPPE2429%2CPPE3152%2CPPE3479%2CPPE3483%2CPPE3394%2CLIMA_URB1_DIRECTO%2CPPE2511%2CIBIS_19%2CPPE1382%2CIBIS_3PL_83%2CPPE3248",
        "https://www.falabella.com.pe/s/browse/v1/listing/pe?sid=HO_CD_F19_GC_TEC_2768&categoryId=cat40556&categoryName=Videojuegos&pgid=2&pid=799c102f-9b4c-44be-a421-23e366a63b82&zones=IBIS_51%2CPPE3342%2CPPE3361%2CPPE1112%2CPPE3384%2C912_LIMA_2%2CPPE1280%2C150000%2CPPE4%2C912_LIMA_1%2CPPE1279%2C150101%2CPPE344%2CPPE3059%2CPPE2665%2CPPE2492%2CIMP_2%2CPPE3331%2CPPE3357%2CPPE1091%2CPERF_TEST%2CPPE1653%2CPPE2486%2COLVAA_81%2CPPE2815%2CIMP_1%2CPPE3164%2CPPE2918%2CURBANO_83%2CPPE2429%2CPPE3152%2CPPE3479%2CPPE3483%2CPPE3394%2CLIMA_URB1_DIRECTO%2CPPE2511%2CIBIS_19%2CPPE1382%2CIBIS_3PL_83%2CPPE3248",
        "https://www.falabella.com.pe/s/browse/v1/listing/pe?sid=HO_CD_F19_GC_TEC_2768&categoryId=cat11810489&categoryName=Sofas-y-Sillones&pgid=2&pid=799c102f-9b4c-44be-a421-23e366a63b82&zones=IBIS_51%2CPPE3342%2CPPE3361%2CPPE1112%2CPPE3384%2C912_LIMA_2%2CPPE1280%2C150000%2CPPE4%2C912_LIMA_1%2CPPE1279%2C150101%2CPPE344%2CPPE3059%2CPPE2665%2CPPE2492%2CIMP_2%2CPPE3331%2CPPE3357%2CPPE1091%2CPERF_TEST%2CPPE1653%2CPPE2486%2COLVAA_81%2CPPE2815%2CIMP_1%2CPPE3164%2CPPE2918%2CURBANO_83%2CPPE2429%2CPPE3152%2CPPE3479%2CPPE3483%2CPPE3394%2CLIMA_URB1_DIRECTO%2CPPE2511%2CIBIS_19%2CPPE1382%2CIBIS_3PL_83%2CPPE3248",
        "https://www.falabella.com.pe/s/browse/v1/listing/pe?sid=HO_CD_F19_GC_TEC_2768&categoryId=cat40500&categoryName=Bicicletas&pgid=2&pid=799c102f-9b4c-44be-a421-23e366a63b82&zones=IBIS_51%2CPPE3342%2CPPE3361%2CPPE1112%2CPPE3384%2C912_LIMA_2%2CPPE1280%2C150000%2CPPE4%2C912_LIMA_1%2CPPE1279%2C150101%2CPPE344%2CPPE3059%2CPPE2665%2CPPE2492%2CIMP_2%2CPPE3331%2CPPE3357%2CPPE1091%2CPERF_TEST%2CPPE1653%2CPPE2486%2COLVAA_81%2CPPE2815%2CIMP_1%2CPPE3164%2CPPE2918%2CURBANO_83%2CPPE2429%2CPPE3152%2CPPE3479%2CPPE3483%2CPPE3394%2CLIMA_URB1_DIRECTO%2CPPE2511%2CIBIS_19%2CPPE1382%2CIBIS_3PL_83%2CPPE3248",
        "https://www.falabella.com.pe/s/browse/v1/listing/pe?sid=HO_CD_F19_GC_TEC_2768&categoryId=cat13820483&categoryName=Sillas-gamer&pgid=2&pid=799c102f-9b4c-44be-a421-23e366a63b82&zones=IBIS_51%2CPPE3342%2CPPE3361%2CPPE1112%2CPPE3384%2C912_LIMA_2%2CPPE1280%2C150000%2CPPE4%2C912_LIMA_1%2CPPE1279%2C150101%2CPPE344%2CPPE3059%2CPPE2665%2CPPE2492%2CIMP_2%2CPPE3331%2CPPE3357%2CPPE1091%2CPERF_TEST%2CPPE1653%2CPPE2486%2COLVAA_81%2CPPE2815%2CIMP_1%2CPPE3164%2CPPE2918%2CURBANO_83%2CPPE2429%2CPPE3152%2CPPE3479%2CPPE3483%2CPPE3394%2CLIMA_URB1_DIRECTO%2CPPE2511%2CIBIS_19%2CPPE1382%2CIBIS_3PL_83%2CPPE3248",
        "https://www.falabella.com.pe/s/browse/v1/listing/pe?sid=HO_CD_F19_GC_TEC_2768&categoryId=cat6370558&categoryName=Electrodomesticos-de-Cocina&pgid=2&pid=799c102f-9b4c-44be-a421-23e366a63b82&zones=IBIS_51%2CPPE3342%2CPPE3361%2CPPE1112%2CPPE3384%2C912_LIMA_2%2CPPE1280%2C150000%2CPPE4%2C912_LIMA_1%2CPPE1279%2C150101%2CPPE344%2CPPE3059%2CPPE2665%2CPPE2492%2CIMP_2%2CPPE3331%2CPPE3357%2CPPE1091%2CPERF_TEST%2CPPE1653%2CPPE2486%2COLVAA_81%2CPPE2815%2CIMP_1%2CPPE3164%2CPPE2918%2CURBANO_83%2CPPE2429%2CPPE3152%2CPPE3479%2CPPE3483%2CPPE3394%2CLIMA_URB1_DIRECTO%2CPPE2511%2CIBIS_19%2CPPE1382%2CIBIS_3PL_83%2CPPE3248",
        "https://www.falabella.com.pe/s/browse/v1/listing/pe?sid=HO_CD_F19_GC_TEC_2768&categoryId=cat11810489&categoryName=Sofas-y-Sillones&pgid=2&pid=799c102f-9b4c-44be-a421-23e366a63b82&zones=IBIS_51%2CPPE3342%2CPPE3361%2CPPE1112%2CPPE3384%2C912_LIMA_2%2CPPE1280%2C150000%2CPPE4%2C912_LIMA_1%2CPPE1279%2C150101%2CPPE344%2CPPE3059%2CPPE2665%2CPPE2492%2CIMP_2%2CPPE3331%2CPPE3357%2CPPE1091%2CPERF_TEST%2CPPE1653%2CPPE2486%2COLVAA_81%2CPPE2815%2CIMP_1%2CPPE3164%2CPPE2918%2CURBANO_83%2CPPE2429%2CPPE3152%2CPPE3479%2CPPE3483%2CPPE3394%2CLIMA_URB1_DIRECTO%2CPPE2511%2CIBIS_19%2CPPE1382%2CIBIS_3PL_83%2CPPE3248",
    ]

    total_products = []

    for url in category_urls:
        print(f"Iniciando extracción para la URL: {url}")
        products = fetch_products_from_category(url, driver, 70)
        total_products.extend(products)
        print(f"Total de productos obtenidos de esta categoría: {len(products)}")

    driver.quit()
    print(
        f"Total de productos obtenidos de todas las categorías: {len(total_products)}"
    )


def main_loop():
    while True:
        main()
        # Opcional: Puedes poner un delay para evitar un bucle excesivamente rápido
        time.sleep(10)  # Espera 60 segundos antes de volver a ejecutar el script


if __name__ == "__main__":
    main_loop()
