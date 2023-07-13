# Pequeno projeto para criação de um mapa com localização e rastro de um veículo
# Para ultilizar o projeto basta usar seu login e senha e clicar no botão acessar, que será automaticamente redirecionado para a página para poder acessar o mapa.
# Tecnologias ultilizadas - HTML, CSS, Python e Flask.
# API para o mapa - OpenLayers - Link: https://openlayers.org/download/
# Github do Projeto: https://github.com/lucasgabriel182/WR_Project
# O mapa mostrará os pontos da ultima visualização do veículo, possuindo também um rastro para traçar a rota feito pelo mesmo.

# Aqui é feita a importação das bibliotecas que serão usadas no projeto.

from flask import Flask, render_template
import folium
import json

app = Flask(__name__, template_folder='template')

# Aqui informamos a rota para que o código encontre os dados para gerar o mapa
@app.route('/', methods=['GET'])
def render_index():
    return render_template('index.html')


# Informamos onde ele irá buscar as pocições e onde será mostrado as mesmas
@app.route('/posicaum', methods=['GET', 'POST'])
def render_posicaum():
    with open('positions.json') as file:
        data = json.load(file)
    
# Informamos a latitude/longitude das posições que serão vistas no nosso navegador
    latitudes = [float(item['latitude']) for item in data['data']]
    longitudes = [float(item['longitude']) for item in data['data']]
    coordenadas = list(zip(latitudes, longitudes))
    
    # Geramos o mapa com as posições e o zoom (Zoom serve para inicar o mapa em uma certa distancia de visão do mesmo)
    mapa = folium.Map(location=[latitudes[0], longitudes[0]], zoom_start=15)

# Aqui inserimos a linha, rastro ou trastejado. Como está descrito no código será uma linha vermelha que ligará as posições do mapa assim gerando um "caminho" feito pelo veículo.
    folium.PolyLine(
        locations=coordenadas,
        color='red',
        weight=2,
        opacity=1
    ).add_to(mapa)

    for lat, lon in coordenadas:
        folium.Marker(location=[lat, lon]).add_to(mapa)
    
    # Aqui o mapa será gerado pelo navegador, demonstrando o caminho do arquivo para gerar o item.
    mapa.save("template/static/mapa.html")
    
    return render_template('static/mapa.html')

if __name__ == '__main__':
    app.run()