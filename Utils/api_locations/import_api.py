import requests
import json


class GeoApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_distritos(self):
        try:
            response = requests.get(f"{self.base_url}/distritos/municipios")
            if response.status_code == 200:
                return response.json() 
            else:
                print(f"Erro ao acessar a lista de distritos: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro ao acessar a lista de distritos: {e}")
            return None

    def get_municipios_coordinates(self, municipio):
        url = f"{self.base_url}/municipio/{municipio}"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response.json()  
            else:
                print(f"Erro ao acessar a API para {municipio}: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro ao acessar a API para {municipio}: {e}")
            return None

    def get_freguesias_coordinates(self, municipio):
        url = f"{self.base_url}/municipio/{municipio}/Freguesias"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response.json()  
            else:
                print(f"Erro ao acessar a API para {municipio}: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro ao acessar a API para {municipio}: {e}")
            return None


def main():
    geo_api_client = GeoApiClient(base_url="https://json.geoapi.pt")

    distritos = geo_api_client.get_distritos()

    if distritos is None:
        print("Não foi possível obter a lista de distritos.")
        return

    distritos_data = {}

    for distrito in distritos:
        nome_distrito = distrito["distrito"]
        municipios = distrito["municipios"]

        print(f"Obtendo dados para o distrito: {nome_distrito}")

        distrito_geojson = distrito.get("geojson", {})
        distrito_info = {
            "coordenadas": distrito_geojson.get("properties", {}).get("centros", {}).get("centro", None),
            "municipios": []
        }

        for municipio in municipios:
            nome_municipio = municipio["nome"]
            print(f"  Obtendo coordenadas para o município: {nome_municipio}")

            municipio_info = geo_api_client.get_municipios_coordinates(nome_municipio)

            if municipio_info:
                municipio_geojson = municipio_info.get("geojson", {})
                municipio_data = {
                    "nome": nome_municipio,
                    "coordenadas": municipio_geojson.get("properties", {}).get("centros", {}).get("centro", None),
                    "freguesias": []
                }

                freguesias = geo_api_client.get_freguesias_coordinates(nome_municipio)
                if freguesias:
                    for freguesia in freguesias.get("geojsons", {}).get("freguesias", []):
                        nome_freguesia = freguesia["properties"]["Freguesia"]
                        centro = freguesia["properties"]["centros"]["centro"]  
                        municipio_data["freguesias"].append({
                            "nome_freguesia": nome_freguesia,
                            "centro": centro
                        })
                distrito_info["municipios"].append(municipio_data)
            else:
                print(f"Não foi possível obter coordenadas para o município {nome_municipio}")

        distritos_data[nome_distrito] = distrito_info

    with open("distritos_municipios_freguesias.json", "w", encoding="utf-8") as f:
        json.dump(distritos_data, f, ensure_ascii=False, indent=4)

    print("Arquivo JSON com os dados de distritos, municípios e freguesias foi criado com sucesso!")


if __name__ == "__main__":
    main()
