
import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Icon

# Autenticacao na SPTrans
load_dotenv(".env")

s = requests.Session()

res = s.post(
    f"https://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}"
)

print("Autenticacao:", res.text)

if res.json():

    # Criar o mapa
    m = Map(location=[-23.60, -46.68], zoom_start=11)

    # Codigos dos dois sentidos da linha 8700-10
    linhas = [1877, 34645]

    for codigo in linhas:

        # Buscar as paradas
        res = s.get(
            f"https://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={codigo}"
        )

        paradas = res.json()

        print("Paradas:", len(paradas))

        # Pins azuis para as paradas
        for i in paradas:
            Marker(
                location=[i["py"], i["px"]],
                popup=i["np"],
                icon=Icon(color="blue")
            ).add_to(m)

        # Buscar os onibus
        res = s.get(
            f"https://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha={codigo}"
        )

        pos = res.json()

        print("Onibus:", len(pos["vs"]))

        # Pins vermelhos para os onibus
        for i in pos["vs"]:
            Marker(
                location=[i["py"], i["px"]],
                popup=str(i["p"]),
                icon=Icon(color="red")
            ).add_to(m)

    # Salvar o mapa
    m.save("mapa_frota_8700.html")

    print("Mapa criado com sucesso!")

else:
    print("Erro na autenticacao.")
