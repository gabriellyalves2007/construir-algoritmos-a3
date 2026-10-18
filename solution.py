import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Icon

# Autenticacao
load_dotenv(".env")

s = requests.Session()
res = s.post(
    f"https://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}"
)

print("Autenticacao:", res.text)

if res.json():

    # Buscar a linha 8000-10
    res = s.get(
        "https://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca=8000"
    )
    linhas = res.json()

    codigo = 0

    for linha in linhas:
        if linha["lt"] == "8000" and linha["tl"] == 10:
            codigo = linha["cl"]
            break

    if codigo != 0:

        # Buscar as paradas
        res = s.get(
            f"https://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={codigo}"
        )
        paradas = res.json()

        print("Paradas:", len(paradas))

        # Buscar os onibus em circulacao
        pos = s.get(
            f"https://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha={codigo}"
        )
        pos = pos.json()

        print("Onibus:", len(pos["vs"]))

        if paradas:

            # Criar o mapa
            m = Map(
                location=[paradas[0]["py"], paradas[0]["px"]],
                zoom_start=13
            )

            # Pins azuis para as paradas
            for i in paradas:
                Marker(
                    location=[i["py"], i["px"]],
                    popup=i["np"],
                    icon=Icon(color="blue")
                ).add_to(m)

            # Pins vermelhos para os onibus
            for i in pos["vs"]:
                Marker(
                    location=[i["py"], i["px"]],
                    popup=i["p"],
                    icon=Icon(color="red")
                ).add_to(m)

            # Salvar o mapa
            m.save("mapa_frota_8000.html")

            print("Mapa criado com sucesso!")
        else:
            print("Nenhuma parada encontrada.")
    else:
        print("Linha 8000-10 nao encontrada.")
else:
    print("Erro na autenticacao.")
