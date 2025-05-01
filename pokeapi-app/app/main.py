from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import requests
import csv
import os

app = Flask(__name__)
REQUEST_COUNT = Counter('pokeapi_requests_total', 'Total number of requests to /pokemon', ['pokemon_name'])

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"


if not os.path.exists('query_log.csv'):
    with open('query_log.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["pokemon_name", "hp", "attack", "defense", "special-attack", "special-defense", "speed"])

@app.route('/pokemon', methods=['GET'])
def get_pokemon():
    name = request.args.get('name')

    if not name:
        return jsonify({"error": "Please provide a 'name' query parameter"}), 400

    response = requests.get(f"{POKEAPI_URL}{name.lower()}")
    if response.status_code != 200:
        return jsonify({"error": "Pokemon not found"}), 404

    data = response.json()

    base_stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    
    
    pokemon_info = {
        "name": data['name'],
        "url": data['species']['url'],
        "hp": base_stats.get('hp', 0),
        "attack": base_stats.get('attack', 0),
        "defense": base_stats.get('defense', 0),
        "special-attack": base_stats.get('special-attack', 0),
        "special-defense": base_stats.get('special-defense', 0),
        "speed": base_stats.get('speed', 0)
    }

   
    with open('query_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            pokemon_info['name'],
            pokemon_info['hp'],
            pokemon_info['attack'],
            pokemon_info['defense'],
            pokemon_info['special-attack'],
            pokemon_info['special-defense'],
            pokemon_info['speed']
        ])

    return jsonify(pokemon_info)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
