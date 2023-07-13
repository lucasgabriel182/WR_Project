from flask import Flask, render_template
import folium
import json

app = Flask(__name__, template_folder='template')

@app.route('/', methods=['GET'])
def render_index():
    return render_template('index.html')

@app.route('/posicaum', methods=['GET', 'POST'])
def render_posicaum():
    with open('positions.json') as file:
        data = json.load(file)
    
    latitudes = [float(item['latitude']) for item in data['data']]
    longitudes = [float(item['longitude']) for item in data['data']]
    coordenadas = list(zip(latitudes, longitudes))
    
    mapa = folium.Map(location=[latitudes[0], longitudes[0]], zoom_start=15)

    folium.PolyLine(
        locations=coordenadas,
        color='blue',
        weight=2,
        opacity=1
    ).add_to(mapa)

    for lat, lon in coordenadas:
        folium.Marker(location=[lat, lon]).add_to(mapa)
    
    mapa.save("template/static/mapa.html")
    
    return render_template('static/mapa.html')

if __name__ == '__main__':
    app.run()
