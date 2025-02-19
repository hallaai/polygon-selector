# app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Read locations data
df = pd.read_csv('locations.csv')
locations = df.to_dict('records')

def point_in_polygon(point, polygon):
    # Ray casting algorithm
    x, y = point
    inside = False
    n = len(polygon)
    p1x, p1y = polygon[0]
    for i in range(n+1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/api/points')
def get_points():
    return jsonify([{
        'name': loc['name'],
        'lat': loc['lat'],
        'lng': loc['lon']
    } for loc in locations])

@app.route('/api/check-points', methods=['POST'])
def check_points():
    polygon = request.json.get('polygon', [])
    selected = []
    
    for loc in locations:
        point = (loc['lon'], loc['lat'])  # Leaflet uses [lat, lng] but we need (x, y)
        if point_in_polygon(point, polygon):
            selected.append({
                'name': loc['name'],
                'lat': loc['lat'],
                'lng': loc['lon']
            })
    
    return jsonify({'selected': selected})

if __name__ == '__main__':
    app.run(debug=True, port=5001)