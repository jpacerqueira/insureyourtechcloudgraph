import feedparser
import pandas as pd
import requests
from datetime import datetime
import json

# GCP Cloud Status Feed, Incident Status History, Product Catalogue
# https://status.cloud.google.com/en/feed.atom
# https://status.cloud.google.com/incidents.json
# https://status.cloud.google.com/products.json
# Required libraries
# pip install feedparser pandas requests

def process_feed_atom(feed):
    """Process the GCP status feed.atom data"""
    feed_notifications = []
    for entry in feed.entries:
        notification = {
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'published': entry.get('published', ''),
            'updated': entry.get('updated', ''),
            'author': entry.get('author', ''),
            'category': entry.get('category', ''),
            'content': entry.get('content', [{}])[0].get('value', '') if entry.get('content') else '',
            'description': entry.get('description', ''),
            'id': entry.get('id', ''),
            'source': 'feed.atom'
        }
        feed_notifications.append(notification)
    return feed_notifications

def process_incidents_json(incidents):
    """Process the GCP incidents.json data maintaining original structure"""
    incidents_notifications = []
    if not isinstance(incidents, list):
        return incidents_notifications
        
    for incident in incidents:
        if isinstance(incident, dict):
            # Get latest update info
            updates = incident.get('updates', [])
            most_recent_update = incident.get('most_recent_update', {})
            
            notification = {
                'id': incident.get('id', ''),
                'number': incident.get('number', ''),
                'begin': incident.get('begin', ''),
                'created': incident.get('created', ''),
                'end': incident.get('end', ''),
                'modified': incident.get('modified', ''),
                'external_desc': incident.get('external_desc', ''),
                'status_impact': incident.get('status_impact', ''),
                'severity': incident.get('severity', ''),
                'service_key': incident.get('service_key', ''),
                'service_name': incident.get('service_name', ''),
                'uri': incident.get('uri', ''),
                
                # Most recent update fields
                'most_recent_update.created': most_recent_update.get('created', ''),
                'most_recent_update.modified': most_recent_update.get('modified', ''),
                'most_recent_update.when': most_recent_update.get('when', ''),
                'most_recent_update.text': most_recent_update.get('text', ''),
                'most_recent_update.status': most_recent_update.get('status', ''),
                
                # Updates count
                'updates.count': len(updates),
                'source': 'incidents.json'
            }
            
            # Handle affected products array maintaining original structure
            if 'affected_products' in incident:
                products = incident['affected_products']
                if products and isinstance(products[0], dict):
                    notification['affected_products'] = [p.get('title', '') for p in products]
                    notification['affected_products.ids'] = [p.get('id', '') for p in products]
                else:
                    notification['affected_products'] = products

            # Handle affected locations arrays maintaining original structure
            if 'currently_affected_locations' in incident:
                locations = incident['currently_affected_locations']
                notification['currently_affected_locations'] = [loc.get('title', '') for loc in locations]
                notification['currently_affected_locations.ids'] = [loc.get('id', '') for loc in locations]

            if 'previously_affected_locations' in incident:
                locations = incident['previously_affected_locations']
                notification['previously_affected_locations'] = [loc.get('title', '') for loc in locations]
                notification['previously_affected_locations.ids'] = [loc.get('id', '') for loc in locations]
                
            incidents_notifications.append(notification)
            
    return incidents_notifications

def process_products_json(products_data):
    """Process the GCP products.json data maintaining original structure"""
    products_notifications = []
    
    if not isinstance(products_data, dict) or 'products' not in products_data:
        return products_notifications
        
    for product in products_data['products']:
        notification = {
            'title': product.get('title', ''),
            'id': product.get('id', ''),
            'key': product.get('key', ''),
            'name': product.get('name', ''),
            'uri': product.get('uri', ''),
            'source': 'products.json'
        }
        products_notifications.append(notification)
            
    return products_notifications

def fetch_gcp_status():
    """Fetch and process GCP status feeds, then export to CSV"""
    # URLs from GCP status page
    feed_atom_url = "https://status.cloud.google.com/en/feed.atom"
    incidents_json_url = "https://status.cloud.google.com/incidents.json"
    products_json_url = "https://status.cloud.google.com/products.json"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    }
    
    # Initialize notifications lists
    feed_atom_notifications = []
    incidents_json_notifications = []
    products_json_notifications = []
    
    # Fetch and process feed.atom
    try:
        feed = feedparser.parse(feed_atom_url)
        feed_atom_notifications = process_feed_atom(feed)
    except Exception as e:
        print(f"Error processing feed.atom: {e}")
    
    # Fetch and process incidents.json
    try:
        incidents_json_response = requests.get(incidents_json_url, headers=headers)
        incidents_json_response.raise_for_status()
        incidents = incidents_json_response.json()
        incidents_json_notifications = process_incidents_json(incidents)
    except requests.RequestException as e:
        print(f"Error fetching incidents.json: {e}")
    except json.JSONDecodeError:
        print("Error decoding incidents.json")
    
    # Fetch and process products.json
    try:
        products_json_response = requests.get(products_json_url, headers=headers)
        products_json_response.raise_for_status()
        products = products_json_response.json()
        products_json_notifications = process_products_json(products)
    except requests.RequestException as e:
        print(f"Error fetching products.json: {e}")
    except json.JSONDecodeError:
        print("Error decoding products.json")
    
    # Function to save data to CSV
    def save_to_csv(data, source_name):
        if not data:
            print(f"No data to export for {source_name}")
            return
        df = pd.DataFrame(data)
        output_file = f'gcp_cloud_status_{source_name.lower().replace(".", "_")}.csv'
        df.to_csv(output_file, index=False)
        print(f"\nExported {len(data)} entries to {output_file}")
        print("Columns in output file:")
        for col in df.columns:
            print(f"- {col}")
    
    # Save each source's data to its respective CSV
    save_to_csv(feed_atom_notifications, "feed.atom")
    save_to_csv(incidents_json_notifications, "incidents.json")
    save_to_csv(products_json_notifications, "products.json")

if __name__ == "__main__":
    fetch_gcp_status()