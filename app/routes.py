from flask import Blueprint, render_template, request, jsonify
from .models import ForumCategory, Post, Event
from . import db
import requests
import os

AIR_API_KEY = os.getenv("AIR_API_KEY")
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/map')
def map_view():
    return render_template('map.html')

@main.route('/hazards')
def hazards():
    return render_template('hazards.html')

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


import random

@main.route('/api/geocode', methods=['GET'])
def geocode():
    query = request.args.get('q')
    if not query:
        return jsonify([])
    # Call Nominatim API. Append "USA" to guide the query if it's just a zip code, 
    # but Nominatim should handle zip codes OK, we just need to format it nicely.
    # To be safe, if we determine it's just digits (a zip code), format searching USA.
    search_query = query
    if query.isdigit() and len(query) == 5:
        search_query = f"{query}, USA"

    url = f"https://nominatim.openstreetmap.org/search?q={search_query}&format=json&limit=1"
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
    
    url = "https://www.airnowapi.org/aq/observation/latLong/"
    
    params = {
        "format": "application/json",
        "latitude": lat,
        "longitude": lon,
        "distance": 25,
        "API_KEY": AIR_API_KEY
    }


    response = requests.get(url, params=params)





    # Generate some mock localized sources around the given coordinates
    sources = [
        {
            "id": 1,
            "name": "Industrial Factory Complex",
            "type": "Factory",
            "lat": lat + random.uniform(-0.05, 0.05),
            "lng": lon + random.uniform(-0.05, 0.05),
            "pollutant": "Particulate Matter (PM2.5), Sulfur Dioxide (SO2)",
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
            "name": "Major Highway Congestion",
            "type": "Traffic / Auto Emissions",
            "lat": lat + random.uniform(-0.05, 0.05),
            "lng": lon + random.uniform(-0.05, 0.05),
            "pollutant": "Nitrogen Dioxide (NO2), Carbon Monoxide (CO)",
            "hazards": "Increased risk of respiratory infections, decreased lung function, cardiovascular stress.",
            "mitigation": "Use public transport, bike or walk instead of driving. Plant trees locally to form green buffers. Keep windows closed during rush hour."
        },
        {
            "id": 4,
            "name": "Active Brush Fire / Wildfire",
            "type": "Environmental Hazard",
            "lat": lat + random.uniform(-0.08, 0.08),
            "lng": lon + random.uniform(-0.08, 0.08),
            "pollutant": "Severe Particulate Matter (PM10 & PM2.5), Ozone",
            "hazards": "Immediate severe respiratory distress, eye irritation, exacerbation of chronic heart and lung diseases.",
            "mitigation": "Stay indoors, seal windows, wear N95 masks if you must go outside, run air purifiers constantly."
        },
        {
            "id": 5,
            "name": "Agricultural Runoff / Farming Area",
            "type": "Water & Soil Pollution",
            "lat": lat + random.uniform(-0.06, 0.06),
            "lng": lon + random.uniform(-0.06, 0.06),
            "pollutant": "Pesticides, Nitrates, Phosphates",
            "hazards": "Contaminated local drinking water, toxic algae blooms, long term toxic exposure risks.",
            "mitigation": "Use water filtration systems for drinking water, advocate for organic farming practices, avoid swimming in local unregulated bodies of water."
        }
    ]
    return jsonify(sources)
