import feedparser
import pandas as pd
from datetime import datetime

# IBM Cloud Status Feed
# https://cloud.ibm.com/status/api/notifications/feed.rss
# Required libraries
# pip install feedparser pandas

def fetch_ibm_status():
    # Parse the RSS feed
    feed_url = "https://cloud.ibm.com/status/api/notifications/feed.rss"
    feed = feedparser.parse(feed_url)
    
    # Initialize lists to store data
    notifications = []
    
    # Extract data from each entry
    for entry in feed.entries:
        # Extract basic fields
        title = entry.title
        link = entry.link
        published = entry.published
        description = entry.description
        
        # Parse the description to extract additional metadata
        type_info = ""
        regions = ""
        resources = ""
        update_time = ""
        
        # Split description into lines and extract metadata
        desc_lines = description.split('\n')
        for line in desc_lines:
            line = line.strip()
            if line.startswith('Type:'):
                type_info = line.replace('Type:', '').strip()
            elif line.startswith('Regions:'):
                regions = line.replace('Regions:', '').strip()
            elif line.startswith('Resources:'):
                resources = line.replace('Resources:', '').strip()
            elif line.startswith('Update Time:'):
                update_time = line.replace('Update Time:', '').strip()
        
        # Create notification entry
        notification = {
            'Title': title,
            'Link': link,
            'Published': published,
            'Type': type_info,
            'Regions': regions,
            'Resources': resources,
            'Update_Time': update_time,
            'Description': description
        }
        
        notifications.append(notification)
    
    # Create DataFrame
    df = pd.DataFrame(notifications)
    
    # Export to CSV
    df.to_csv('ibm_cloud_status.csv', index=False)
    print(f"Exported {len(notifications)} notifications to ibm_cloud_status.csv")

if __name__ == "__main__":
    fetch_ibm_status()