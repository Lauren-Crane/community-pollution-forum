from flask import Blueprint, render_template, request, jsonify
from .models import ForumCategory, Post, Event
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/map')
def map_view():
    return render_template('map.html')

@main.route('/forum')
def forum_index():
    categories = ForumCategory.query.all()
    # If no categories exist, maybe we can just show posts directly or mock it
    return render_template('forum_index.html', categories=categories)

@main.route('/events')
def events_index():
    events = Event.query.all()
    return render_template('events.html', events=events)

@main.route('/contact')
def contact():
    return render_template('contact.html')

import requests
import random

@main.route('/api/geocode', methods=['GET'])
def geocode():
    query = request.args.get('q')
    if not query:
        return jsonify([])
    # Call Nominatim API
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
    headers = {'User-Agent': 'CommunityPollutionForum/1.0'}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if data:
            return jsonify({'lat': data[0]['lat'], 'lon': data[0]['lon'], 'display_name': data[0]['display_name']})
    except Exception as e:
        print("Geocoding error:", e)
    return jsonify({'error': 'Location not found'}), 404

@main.route('/api/pollution-data', methods=['GET'])
def pollution_data():
    lat = float(request.args.get('lat', 0))
    lon = float(request.args.get('lon', 0))
    
    # Generate some mock localized sources around the given coordinates
    sources = [
        {
            "id": 1,
            "name": "Industrial Factory Complex",
            "type": "Factory",
            "lat": lat + random.uniform(-0.05, 0.05),
            "lng": lon + random.uniform(-0.05, 0.05),
            "pollutant": "Particulate Matter (PM2.5)",
            "hazards": "Respiratory issues, asthma aggravation, lung damage.",
            "mitigation": "Install HEPA filters at home, avoid outdoor activities during high emission periods, support stronger industrial emission regulations."
        },
        {
            "id": 2,
            "name": "Local Data Center",
            "type": "Data Center",
            "lat": lat + random.uniform(-0.05, 0.05),
            "lng": lon + random.uniform(-0.05, 0.05),
            "pollutant": "E-waste & High Energy Grid Emissions",
            "hazards": "Indirect contributions to smog and climate change due to excessive fossil fuel power consumption.",
            "mitigation": "Advocate for renewable energy powering data centers, improve personal device energy efficiency."
        },
        {
            "id": 3,
            "name": "Highway Intersection",
            "type": "Traffic",
            "lat": lat + random.uniform(-0.05, 0.05),
            "lng": lon + random.uniform(-0.05, 0.05),
            "pollutant": "Nitrogen Dioxide (NO2)",
            "hazards": "Increased risk of respiratory infections, decreased lung function.",
            "mitigation": "Use public transport, bike or walk instead of driving. Plant trees locally to form green buffers."
        }
    ]
    return jsonify(sources)
