import os
import csv
import re
from datetime import datetime

def run_merge_script():
    # Run the merge_text_files script
    os.system('./merge_text_files.sh')

def parse_merge_file():
    # Read the merge.txt file
    with open('merge.txt', 'r') as file:
        content = file.read()

    # Split the content by "Outage Filename:"
    outages = content.split('Outage Filename:')[1:]

    # Prepare data for CSV
    csv_data = []
    for outage in outages:
        lines = outage.strip().split('\n')
        filename = lines[0].strip()
        cloud_provider = extract_info(lines, r'(Cloud Provider|Provider):\s*(.*)')
        region = extract_info(lines, r'(Region[s]?|Location[s]?|Area[s]?):\s*(.*)')
        availability_zone = extract_info(lines, r'(Availability Zone[s]?|Zone[s]?):\s*(.*)')
        services = extract_info(lines, r'(Service[s]? Impacted|Affected Service[s]?|Service[s]?):\s*(.*)')
        duration = extract_info(lines, r'(Duration of Outage|Outage Duration|Downtime Period):\s*(.*)')
        total_minutes = calculate_total_minutes(duration)
        outage_date = extract_outage_date(lines)

        csv_data.append([filename, cloud_provider, region, availability_zone, services, duration, total_minutes, outage_date])

    return csv_data

def extract_info(lines, pattern):
    for line in lines:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return match.group(2).strip()
    return 'N/A'

def extract_outage_date(lines):
    # Patterns to match various date formats
    date_patterns = [
        r'Start Time:.*?(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
        r'(\d{1,2} [A-Za-z]+ \d{4})',  # DD Month YYYY
        r'(\d{4}/\d{2}/\d{2})',  # YYYY/MM/DD
        r'(\d{1,2}/\d{1,2}/\d{4})',  # MM/DD/YYYY or DD/MM/YYYY
        r'(\d{1,2}-\d{1,2}-\d{4})',  # MM-DD-YYYY or DD-MM-YYYY
    ]

    for line in lines:
        for pattern in date_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1)

    return 'N/A'

def calculate_total_minutes(duration):
    if not duration or duration == 'N/A':
        return 0

    days = hours = minutes = 0
    match = re.search(r'(\d+)\s*day', duration, re.IGNORECASE)
    if match:
        days = int(match.group(1))

    match = re.search(r'(\d+)\s*hour', duration, re.IGNORECASE)
    if match:
        hours = int(match.group(1))

    match = re.search(r'(\d+)\s*minute', duration, re.IGNORECASE)
    if match:
        minutes = int(match.group(1))

    total_minutes = days * 1440 + hours * 60 + minutes
    return total_minutes

def write_to_csv(data):
    # Write the data to a CSV file
    with open('merge_results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Output Filename', 'Cloud Provider', 'Region', 'Availability Zone', 'Services', 'Duration', 'Total Outage Minutes', 'Outage Date'])
        writer.writerows(data)

def main():
    run_merge_script()
    csv_data = parse_merge_file()
    write_to_csv(csv_data)
    print("CSV file 'merge_results.csv' has been created.")

if __name__ == '__main__':
    main()