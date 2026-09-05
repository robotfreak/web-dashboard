#!/usr/bin/env python3
"""
KI-OS Dashboard — Flask Web UI für Self-Hosted Services
Zeigt alle Services im Tailscale Mesh mit Health Checks an
"""

import os
import yaml
import requests
import threading
import time
from datetime import datetime
from flask import Flask, render_template, jsonify
from pathlib import Path

app = Flask(__name__)

# Globale State für Service Status
services_state = {}
state_lock = threading.Lock()

# Konfiguration laden
CONFIG_PATH = Path(__file__).parent / 'config.yaml'

def load_config():
    """Lade config.yaml"""
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

def check_service_health(service):
    """Prüft ob ein Service online ist"""
    url = service.get('url', '')
    health_endpoint = service.get('health_endpoint', '/api/health')
    
    # Skip file:// und terminal:// URLs
    if url.startswith('file://') or url.startswith('terminal://'):
        return 'local'
    
    # Try health endpoint first, then root
    try:
        # Try health endpoint
        if health_endpoint and not url.endswith(health_endpoint):
            test_url = url.rstrip('/') + health_endpoint
        else:
            test_url = url
            
        response = requests.get(test_url, timeout=2, verify=False)
        if response.status_code < 500:
            return 'online'
    except:
        pass
    
    # Fallback: Try root URL
    try:
        response = requests.get(url, timeout=2, verify=False)
        if response.status_code < 500:
            return 'online'
    except:
        pass
    
    return 'offline'

def health_check_loop():
    """Background Thread der alle 60s Health Checks macht"""
    config = load_config()
    
    while True:
        try:
            new_state = {}
            
            for service in config.get('services', []):
                name = service['name']
                status = check_service_health(service)
                new_state[name] = {
                    'status': status,
                    'last_check': datetime.now().isoformat(),
                    'url': service.get('url', ''),
                    'icon': service.get('icon', 'default'),
                    'category': service.get('category', 'Other'),
                    'description': service.get('description', ''),
                    'tags': service.get('tags', []),
                    'tailscale_ip': service.get('tailscale_ip'),
                }
            
            with state_lock:
                services_state.clear()
                services_state.update(new_state)
                
        except Exception as e:
            print(f"Health check error: {e}")
        
        # Warte 60 Sekunden
        time.sleep(60)

@app.route('/')
def index():
    """Dashboard Hauptseite"""
    config = load_config()
    
    # Hole aktuellen Status
    with state_lock:
        current_state = dict(services_state)
    
    # Gruppiere Services nach Kategorie
    categories = {}
    for service in config.get('services', []):
        cat = service.get('category', 'Other')
        if cat not in categories:
            categories[cat] = []
        
        # Füge Status hinzu
        service_with_status = service.copy()
        if service['name'] in current_state:
            service_with_status['status'] = current_state[service['name']]['status']
            service_with_status['last_check'] = current_state[service['name']]['last_check']
        else:
            service_with_status['status'] = 'unknown'
        
        categories[cat].append(service_with_status)
    
    return render_template('index.html',
                         categories=categories,
                         config=config.get('dashboard', {}),
                         total_services=len(config.get('services', [])),
                         online_count=sum(1 for s in current_state.values() if s['status'] == 'online'),
                         timestamp=datetime.now())

@app.route('/api/status')
def api_status():
    """API Endpoint für Service Status"""
    with state_lock:
        return jsonify(services_state)

@app.route('/api/refresh', methods=['POST'])
def api_refresh():
    """Trigger manuellen Health Check"""
    config = load_config()
    
    new_state = {}
    for service in config.get('services', []):
        name = service['name']
        status = check_service_health(service)
        new_state[name] = {
            'status': status,
            'last_check': datetime.now().isoformat(),
        }
    
    with state_lock:
        services_state.clear()
        services_state.update(new_state)
    
    return jsonify({'success': True, 'services': new_state})

if __name__ == '__main__':
    # Start Health Check Thread
    print("🚀 Starting KI-OS Dashboard...")
    print("📊 Loading config from", CONFIG_PATH)
    
    # Initiale Health Checks
    health_thread = threading.Thread(target=health_check_loop, daemon=True)
    health_thread.start()
    
    # Warte auf erste Checks
    print("⏳ Waiting for initial health checks...")
    time.sleep(3)
    
    # Start Flask Server
    print("🌐 Dashboard running on http://0.0.0.0:8050")
    app.run(host='0.0.0.0', port=8050, debug=False, threaded=True)
