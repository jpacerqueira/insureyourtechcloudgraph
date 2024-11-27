import os
import re
from datetime import datetime
from typing import Dict, List, Optional

class OutageInfo:
    def __init__(self):
        self.cloud_provider: str = ""
        self.services: List[str] = []
        self.regions: List[str] = []
        self.availability_zones: List[str] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.duration: str = ""
        self.root_cause: str = ""
        self.resolution: str = ""
        self.downtime_period: str = ""
        self.status: str = ""
        self.impact: str = ""
        self.incident_id: str = ""
        self.affected_components: List[str] = []
        self.mitigation_steps: List[str] = []

def extract_outage_info(text: str) -> List[OutageInfo]:
    outages = []
    current_outage = None
    
    # Extended provider patterns
    provider_patterns = {
        "AWS": r"(?i)(Amazon AWS|AWS|Amazon Web Services)",
        "Azure": r"(?i)(Microsoft Azure|Azure)",
        "GCP": r"(?i)(Google GCP|Google Cloud|GCP)",
        "IBM": r"(?i)(IBM Cloud)",
        "MongoDB": r"(?i)(MongoDB|MongoDB Atlas)",
        "Akamai": r"(?i)(Akamai|Akamai Technologies)",
        "Macrometa": r"(?i)(Macrometa|Macrometa GDN)",
        "Cloudflare": r"(?i)(Cloudflare|CloudFlare Inc)",
        "Databricks": r"(?i)(Databricks)",
        "Salesforce": r"(?i)(Salesforce|SFDC)",
        "Snowflake": r"(?i)(Snowflake|Snowflake Inc)",
        "Oracle": r"(?i)(Oracle Cloud|OCI|Oracle Corporation)",
    }
    
    # Extended service patterns for specific providers
    service_patterns = {
        "AWS": [
            r"(?i)(EC2|S3|RDS|Lambda|DynamoDB|CloudFront|Route53|ECS|EKS|SQS|SNS)",
            r"(?i)(AWS Direct Connect|Amazon Connect|AWS Management Console)"
        ],
        "Azure": [
            r"(?i)(Azure SQL|Azure Storage|Azure VM|Azure Functions|Azure Cosmos DB)",
            r"(?i)(Azure App Service|Azure Kubernetes Service|Azure DevOps)"
        ],
        "Cloudflare": [
            r"(?i)(DNS|CDN|DDoS Protection|Workers|Access|Pages)",
            r"(?i)(Cloudflare Stream|Magic Transit|Load Balancing)"
        ],
        "Databricks": [
            r"(?i)(Databricks SQL|Delta Lake|MLflow|Unity Catalog)",
            r"(?i)(Databricks Runtime|Databricks Workflows)"
        ],
        "Salesforce": [
            r"(?i)(Sales Cloud|Service Cloud|Marketing Cloud|Commerce Cloud)",
            r"(?i)(Platform Services|Core Services|API Services)"
        ],
        "Snowflake": [
            r"(?i)(Data Warehouse|Data Lake|Data Engineering|Data Science)",
            r"(?i)(Snowpipe|Snowpark|Data Sharing|Data Marketplace)"
        ]
    }
    
    # Extended status patterns
    status_patterns = {
        "investigating": r"(?i)(investigating|identified|monitoring|increased error rates|elevated delays|issues|disruption)",
        "resolved": r"(?i)(resolved|restored|recovered|mitigated|marked as resolved)",
        "outage": r"(?i)(complete outage|service disruption|unavailable|increased api errors|increased latencies)",
        "degraded": r"(?i)(degraded performance|degraded service|partial outage|intermittent connectivity|elevated packet loss)"
    }
    
    # Extended impact patterns
    impact_patterns = {
        "critical": r"(?i)(critical impact|severe impact|major outage|complete failure|service unavailable)",
        "moderate": r"(?i)(moderate impact|partial impact|minor outage|increased error rates|intermittent issues)",
        "minimal": r"(?i)(minimal impact|slight impact|limited disruption|elevated delays|degraded performance)"
    }
    
    # Add timestamp patterns
    time_patterns = {
        "start": [
            r"(?i)Start(?:\s+Time)?:\s*([^\n]+)",
            r"(?i)Between\s+([\d:]+\s*(?:AM|PM|UTC|PDT|PST|JST|CST).*?)(?:and|to|-)",
            r"(?i)at\s+([\d:]+\s*(?:AM|PM|UTC|PDT|PST|JST|CST))",
            r"(?i)started.*?at\s+([\d:]+\s*(?:AM|PM|UTC|PDT|PST|JST|CST))",
            r"(?i)(\d{1,2}:\d{2}(?:\s*(?:AM|PM))?\s*(?:UTC|PDT|PST|JST|CST))",
        ],
        "end": [
            r"(?i)End(?:\s+Time)?:\s*([^\n]+)",
            r"(?i)and\s+([\d:]+\s*(?:AM|PM|UTC|PDT|PST|JST|CST))",
            r"(?i)resolved.*?at\s+([\d:]+\s*(?:AM|PM|UTC|PDT|PST|JST|CST))",
            r"(?i)until\s+([\d:]+\s*(?:AM|PM|UTC|PDT|PST|JST|CST))",
        ]
    }
    
    # Add duration extraction patterns
    duration_patterns = [
        r"(?i)Duration:\s*([^\n]+)",
        r"(?i)(\d+)\s*(?:days?|hours?|minutes?|hrs?|mins?)",
        r"(?i)approximately\s+(\d+\s+(?:days?|hours?|minutes?|hrs?|mins?)(?:\s+and\s+\d+\s+(?:days?|hours?|minutes?|hrs?|mins?))*)",
    ]
    
    # Add region extraction patterns
    region_patterns = [
        r"(?i)Region(?:s)?(?:\s+Affected)?:\s*([^\n]+)",
        r"(?i)in\s+(?:the\s+)?([\w\s-]+)\s+Region",
        r"(?i)((?:us|eu|ap|sa|ca|me)-(?:east|west|north|south|central|southeast|northeast)-\d+)",
        r"(?i)(Northern Virginia|Tokyo|Seoul|Singapore|London|Frankfurt|Paris|Sydney)",
    ]
    
    # Split text into sections by outage
    sections = re.split(r"--\nOutage Filename:", text)
    
    for section in sections:
        # Skip empty sections
        if not section.strip():
            continue
            
        outage = OutageInfo()
        
        # Identify cloud provider
        for provider, pattern in provider_patterns.items():
            if re.search(pattern, section):
                outage.cloud_provider = provider
                break
        
        if not outage.cloud_provider:
            continue
            
        # Extract services using provider-specific patterns
        if outage.cloud_provider in service_patterns:
            for pattern in service_patterns[outage.cloud_provider]:
                matches = re.finditer(pattern, section)
                for match in matches:
                    service = match.group(1).strip()
                    if service not in outage.services:
                        outage.services.append(service)
        
        # Extract status
        for status, pattern in status_patterns.items():
            if re.search(pattern, section):
                outage.status = status
                break
        
        # Extract impact level
        for impact, pattern in impact_patterns.items():
            if re.search(pattern, section):
                outage.impact = impact
                break
        
        # Extract common fields using patterns
        patterns = {
            "regions": r"(?i)Regions?(?:\s+Affected)?:\s*([^\n]+)",
            "availability_zones": r"(?i)Availability Zones?(?:\s+Affected)?:\s*([^\n]+)",
            "root_cause": r"(?i)Root Cause:\s*([^\n]+)",
            "duration": r"(?i)Duration:\s*([^\n]+)",
            "downtime_period": r"(?i)Downtime Period:\s*([^\n]+)",
            "resolution": r"(?i)Resolution:\s*([^\n]+)"
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, section)
            if match:
                value = match.group(1).strip()
                if field in ["regions", "availability_zones"]:
                    # Split comma or bullet-separated lists
                    items = re.split(r'[,•*]+', value)
                    setattr(outage, field, [item.strip() for item in items if item.strip()])
                else:
                    setattr(outage, field, value)
        
        # Extract regions using multiple patterns
        for pattern in region_patterns:
            matches = re.finditer(pattern, section)
            for match in matches:
                region = match.group(1).strip()
                if region and region not in outage.regions:
                    outage.regions.append(region)
        
        # Extract duration using multiple patterns
        for pattern in duration_patterns:
            match = re.search(pattern, section)
            if match:
                outage.duration = match.group(1).strip()
                break
        
        # Extract timestamps using multiple patterns
        for field, patterns in time_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, section)
                if match:
                    try:
                        timestamp = parse_timestamp(match.group(1))
                        if field == "start":
                            outage.start_time = timestamp
                        else:
                            outage.end_time = timestamp
                        break
                    except:
                        continue
        
        outages.append(outage)
    
    return outages

def parse_timestamp(timestamp_str: str) -> Optional[datetime]:
    """
    Flexible timestamp parser that handles various formats found in the logs
    Returns None if parsing fails
    """
    # Add timestamp parsing logic here
    # This is a placeholder - implement based on your specific timestamp formats
    return None

def write_outage_summary(outage: OutageInfo, file):
    """Helper function to write outage summary with new fields"""
    file.write(f"Cloud Provider: {outage.cloud_provider}\n")
    file.write(f"Services: {', '.join(outage.services)}\n")
    file.write(f"Regions: {', '.join(outage.regions)}\n")
    file.write(f"Availability Zones: {', '.join(outage.availability_zones)}\n")
    file.write(f"Status: {outage.status}\n")
    file.write(f"Impact Level: {outage.impact}\n")
    file.write(f"Duration: {outage.duration}\n")
    file.write(f"Root Cause: {outage.root_cause}\n")
    file.write(f"Resolution: {outage.resolution}\n")
    file.write(f"Downtime Period: {outage.downtime_period}\n")
    if outage.incident_id:
        file.write(f"Incident ID: {outage.incident_id}\n")
    if outage.affected_components:
        file.write(f"Affected Components: {', '.join(outage.affected_components)}\n")
    if outage.mitigation_steps:
        file.write("Mitigation Steps:\n")
        for step in outage.mitigation_steps:
            file.write(f"- {step}\n")
    file.write("\n---\n\n")

def run_merge_script():
    """Run the merge_text_files script and process the merged output"""
    os.system('./merge_text_files.sh')
    
    try:
        with open('merge.txt', 'r') as f:
            content = f.read()
            
        outages = extract_outage_info(content)
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        summary_file = f'outage_summary_{timestamp}.txt'
        
        with open(summary_file, 'w') as f:
            for outage in outages:
                write_outage_summary(outage, f)
                
    except Exception as e:
        print(f"Error processing merged file: {str(e)}")

if __name__ == "__main__":
    run_merge_script()