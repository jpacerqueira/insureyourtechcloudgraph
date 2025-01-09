import os
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple
import csv
from time import time
from dateutil import parser
import pytz

# Map common timezone abbreviations to pytz timezones
TIMEZONE_MAP = {
    'UTC': 'UTC',
    'GMT': 'GMT',
    'EST': 'America/New_York',
    'EDT': 'America/New_York',
    'CST': 'America/Chicago',
    'CDT': 'America/Chicago',
    'MST': 'America/Denver',
    'MDT': 'America/Denver',
    'PST': 'America/Los_Angeles',
    'PDT': 'America/Los_Angeles',
    'AKST': 'America/Anchorage',
    'AKDT': 'America/Anchorage',
    'HST': 'Pacific/Honolulu',
    'HAST': 'Pacific/Honolulu',
    'HADT': 'Pacific/Honolulu',
    'AST': 'America/Halifax',
    'ADT': 'America/Halifax',
    'NST': 'America/St_Johns',
    'NDT': 'America/St_Johns',
    'BST': 'Europe/London',
    'CET': 'Europe/Paris',
    'CEST': 'Europe/Paris',
    'EET': 'Europe/Athens',
    'EEST': 'Europe/Athens',
    'IST': 'Asia/Kolkata',
    'JST': 'Asia/Tokyo',
    'KST': 'Asia/Seoul',
    'AEST': 'Australia/Sydney',
    'AEDT': 'Australia/Sydney',
    'ACST': 'Australia/Adelaide',
    'ACDT': 'Australia/Adelaide',
    'AWST': 'Australia/Perth',
    'NZST': 'Pacific/Auckland',
    'NZDT': 'Pacific/Auckland',
    'UT': 'UTC',
    'US': 'UTC',
    'UTCC': 'UTC',
    # Add more mappings as needed
}

# Define valid regions for each cloud provider
valid_regions = {
    "AWS": [
        # Global
        "global-default",
        # US Regions
        "us-east-1", "us-east-2", "us-west-1", "us-west-2",
        "us-gov-east-1", "us-gov-west-1",
        # Americas
        "ca-central-1", "sa-east-1",
        # Europe/Middle East/Africa
        "eu-central-1", "eu-central-2", "eu-west-1", "eu-west-2", "eu-west-3",
        "eu-north-1", "eu-south-1", "eu-south-2",
        "me-south-1", "me-central-1", "af-south-1",
        # Asia Pacific
        "ap-east-1", "ap-south-1", "ap-south-2",
        "ap-southeast-1", "ap-southeast-2", "ap-southeast-3", "ap-southeast-4",
        "ap-northeast-1", "ap-northeast-2", "ap-northeast-3",
        # China
        "cn-north-1", "cn-northwest-1",
        # Israel
        "il-central-1",
    ],
    "Azure": [
        # Global
        "global-default",
        # Americas
        "eastus", "eastus2", "eastus3", "westus", "westus2", "westus3",
        "centralus", "northcentralus", "southcentralus",
        "canadacentral", "canadaeast",
        "brazilsouth", "brazilsoutheast",
        # Europe
        "northeurope", "westeurope", "centraleurope",
        "uksouth", "ukwest",
        "francecentral", "francesouth",
        "germanywestcentral", "germanynorth",
        "swedencentral", "swedensouth",
        "norwayeast", "norwaywest",
        "switzerlandnorth", "switzerlandwest",
        "italynorth",
        # Asia Pacific
        "eastasia", "southeastasia",
        "australiaeast", "australiasoutheast", "australiacentral", "australiacentral2",
        "japaneast", "japanwest","japan east","japan west",
        "koreacentral", "koreasouth",
        # Middle East/Africa
        "uaenorth", "uaecentral",
        "southafricanorth", "southafricawest",
        "qatarcentral",
        # India
        "centralindia", "southindia", "westindia",
        # China
        "chinanorth", "chinanorth2", "chinanorth3", "chinaeast", "chinaeast2", "chinaeast3", "chinacloudapp.cn","chinacloudsites.cn",
        # Government
        "usgovvirginia", "usgovtexas", "usgovarizona",
    ],
    "GCP": [
        # Global
        "global-default",
        # Americas
        "us-central1", "us-east1", "us-east4", "us-east5",
        "us-west1", "us-west2", "us-west3", "us-west4",
        "us-south1",
        "northamerica-northeast1", "northamerica-northeast2",
        "southamerica-east1", "southamerica-west1",
        # Europe
        "europe-central2", "europe-north1",
        "europe-west1", "europe-west2", "europe-west3",
        "europe-west4", "europe-west6", "europe-west8", "europe-west9",
        "europe-southwest1",
        # Asia Pacific
        "asia-east1", "asia-east2",
        "asia-northeast1", "asia-northeast2", "asia-northeast3",
        "asia-south1", "asia-south2",
        "asia-southeast1", "asia-southeast2",
        "australia-southeast1", "australia-southeast2",
        # Middle East
        "me-west1", "me-central1",
    ],
    "Oracle": [
        # Global
        "global-default",
        # Americas
        "us-ashburn-1", "us-phoenix-1", "us-sanjose-1",
        "ca-montreal-1", "ca-toronto-1",
        "sa-saopaulo-1", "sa-vinhedo-1", "sa-santiago-1",
        # Europe
        "uk-london-1", "uk-cardiff-1",
        "eu-frankfurt-1", "eu-amsterdam-1", "eu-zurich-1",
        "eu-madrid-1", "eu-marseille-1", "eu-milan-1", "eu-paris-1",
        "eu-stockholm-1",
        # Middle East/Africa
        "me-dubai-1", "me-jeddah-1",
        "af-johannesburg-1",
        # Asia Pacific
        "ap-mumbai-1", "ap-hyderabad-1",
        "ap-tokyo-1", "ap-osaka-1",
        "ap-seoul-1", "ap-chuncheon-1",
        "ap-singapore-1",
        "ap-sydney-1", "ap-melbourne-1",
        # Government
        "us-gov-ashburn-1", "us-gov-chicago-1", "us-gov-phoenix-1",
    ],
    "IBM": [
        # Global
        "global-default",
        # Americas
        "us-south", "us-east",
        "br-sao",
        "ca-tor",
        # Europe
        "eu-gb", "eu-de", "eu-es",
        # Asia Pacific
        "au-syd",
        "jp-tok", "jp-osa",
        "kr-seo",
        # Government
        "us-south-govt", "us-east-govt",
        # Multi-zone regions
        "dal10", "dal12", "dal13",
        "wdc04", "wdc06", "wdc07",
        "lon04", "lon05", "lon06",
        "fra02", "fra04", "fra05",
        "syd04", "syd05",
        "tok02", "tok04", "tok05",
        "osa21", "osa22", "osa23",
        "sao01", "sao04", "sao05",
        "tor01", "tor04", "tor05",
        "mad02", "mad04", "mad05",
    ],
    # Add regions for other cloud providers
    # MongoDB Cloud Operates on AWS , Azure and Google Cloud Platform
    "MongoDB": [
        # Global
        "global-default",
        # Azure Regions
        # US Regions
        "us-east-1", "us-east-2", "us-west-1", "us-west-2",
        "us-gov-east-1", "us-gov-west-1",
        # Americas
        "ca-central-1", "sa-east-1",
        # Europe/Middle East/Africa
        "eu-central-1", "eu-central-2", "eu-west-1", "eu-west-2", "eu-west-3",
        "eu-north-1", "eu-south-1", "eu-south-2",
        "me-south-1", "me-central-1", "af-south-1",
        # Asia Pacific
        "ap-east-1", "ap-south-1", "ap-south-2",
        "ap-southeast-1", "ap-southeast-2", "ap-southeast-3", "ap-southeast-4",
        "ap-northeast-1", "ap-northeast-2", "ap-northeast-3",
        # China
        "cn-north-1", "cn-northwest-1",
        # Israel
        "il-central-1",
        # AWS Regions
        # Americas
        "eastus", "eastus2", "eastus3", "westus", "westus2", "westus3",
        "centralus", "northcentralus", "southcentralus",
        "canadacentral", "canadaeast",
        "brazilsouth", "brazilsoutheast",
        # Europe
        "northeurope", "westeurope", "centraleurope",
        "uksouth", "ukwest",
        "francecentral", "francesouth",
        "germanywestcentral", "germanynorth",
        "swedencentral", "swedensouth",
        "norwayeast", "norwaywest",
        "switzerlandnorth", "switzerlandwest",
        "italynorth",
        # Asia Pacific
        "eastasia", "southeastasia",
        "australiaeast", "australiasoutheast", "australiacentral", "australiacentral2",
        "japaneast", "japanwest","japan east","japan west",
        "koreacentral", "koreasouth",
        # Middle East/Africa
        "uaenorth", "uaecentral",
        "southafricanorth", "southafricawest",
        "qatarcentral",
        # India
        "centralindia", "southindia", "westindia",
        # China
        "chinanorth", "chinanorth2", "chinanorth3", "chinaeast", "chinaeast2", "chinaeast3", "chinacloudapp.cn","chinacloudsites.cn",
        # Government
        "usgovvirginia", "usgovtexas", "usgovarizona",
        # Google Cloud Platform Regions
        # Americas
        "us-central1", "us-east1", "us-east4", "us-east5",
        "us-west1", "us-west2", "us-west3", "us-west4",
        "us-south1",
        "northamerica-northeast1", "northamerica-northeast2",
        "southamerica-east1", "southamerica-west1",
        # Europe
        "europe-central2", "europe-north1",
        "europe-west1", "europe-west2", "europe-west3",
        "europe-west4", "europe-west6", "europe-west8", "europe-west9",
        "europe-southwest1",
        # Asia Pacific
        "asia-east1", "asia-east2",
        "asia-northeast1", "asia-northeast2", "asia-northeast3",
        "asia-south1", "asia-south2",
        "asia-southeast1", "asia-southeast2",
        "australia-southeast1", "australia-southeast2",
        # Middle East
        "me-west1", "me-central1",
    ],
}

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
        self.source_outage_report: str = ""
        self.outage_timestamp: float = 0.0

def parse_date(date_str: str) -> Optional[datetime]:
    """
    Flexible date parser that handles various formats found in the logs.
    Returns None if parsing fails.
    """
    try:
        # Replace any double spaces and normalize whitespace
        date_str = re.sub(r'\s+', ' ', date_str.strip())
        
        # Build tzinfos dictionary for dateutil parser
        tzinfos = {abbr: pytz.timezone(tz_name) for abbr, tz_name in TIMEZONE_MAP.items()}
        
        # Handle cases like "10:35 AM - 12:52 PM US/Pacific"
        if '-' in date_str:
            parts = date_str.split('-')
            date_str = parts[0].strip()
        
        dt = parser.parse(date_str, fuzzy=True, tzinfos=tzinfos)
        
        # If the datetime is naive (no timezone), assume UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.utc)
        else:
            # Convert to UTC
            dt = dt.astimezone(pytz.utc)
        
        return dt
    except Exception as e:
        # Optionally log e for debugging
        return None

def speculate_region_from_az(provider: str, az: str) -> Optional[str]:
    """
    Attempt to speculate the region from an availability zone string.
    Returns None if no match found.
    """
    az = az.lower().strip()
    
    # Common AZ to region mapping patterns
    az_patterns = {
        "AWS": {
            r"(\w+-\w+-\d+)[a-z]": lambda x: x.group(1),  # us-east-1a -> us-east-1
            r"(us|eu|ap|sa|ca|me|af)(\d+)-az\d+": lambda x: f"{x.group(1)}-{x.group(2)}",  # us1-az2 -> us-1
        },
        "Azure": {
            r"(\w+)\s*zone\s*\d+": lambda x: x.group(1),  # eastus zone 1 -> eastus
            r"(\w+)-az-\d+": lambda x: x.group(1),  # eastus-az-1 -> eastus
        },
        "GCP" or "Google Cloud Platform": {
            r"(\w+-\w+-\w+)-\w": lambda x: x.group(1),  # us-central1-a -> us-central1
            r"zone\s+(\w+-\w+-\w+)-\w": lambda x: x.group(1),  # zone us-central1-a -> us-central1
        },
        "Akamai": {
            r"(\w+-\w+-\w+)-\w": lambda x: x.group(1),  # us-central1-a -> us-central1
        },
        "Macrometa": {
            r"(\w+-\w+-\w+)-\w": lambda x: x.group(1),  # us-central1-a -> us-central1
        },
        "Cloudflare": {
            r"(\w+-\w+-\w+)-\w": lambda x: x.group(1),  # us-central1-a -> us-central1
        },
        "Databricks": {
            r"(\w+-\w+-\w+)-\w": lambda x: x.group(1),  # us-central1-a -> us-central1
        },
        "Salesforce": {
            r"(\w+-\w+-\w+)-\w": lambda x: x.group(1),  # us-central1-a -> us-central1
        },
        "Snowflake": {
            r"(\w+-\w+-\w+)-\w": lambda x: x.group(1),  # us-central1-a -> us-central1
        },
        "Oracle": {
            r"(\w+-\w+-\w+)-\w": lambda x: x.group(1),  # us-central1-a -> us-central1
        },
        "IBM": {
            r"(\w+-\w+-\w+)-\w": lambda x: x.group(1),  # us-central1-a -> us-central1
        },
        "MongoDB": {
            r"(\w+-\w+-\w+)-\w": lambda x: x.group(1),  # us-central1-a -> us-central1
        },
    }
    
    if provider in az_patterns:
        for pattern, transform in az_patterns[provider].items():
            match = re.match(pattern, az)
            if match:
                return transform(match)
    
    # If no pattern matches, return the AZ as is
    return az

def extract_outage_info(text: str) -> List[OutageInfo]:
    """
    Extract outage information from the merged text content.
    """
    outages = []
    current_filename = "Unknown"
    default_time = datetime(2024, 1, 1, tzinfo=pytz.UTC)

    #TODO: Add more patterns of analysis based on the latest data generated by the LLM 
    # A new LLM for pattern creations may be needed and source it as input file
    
    # Extended provider patterns
    provider_patterns = {
            "AWS": r"(?i)(Amazon AWS|AWS|Amazon Web Services|Amazon|AWS Cloud)",
            "Azure": r"(?i)(Microsoft Azure|Microsoft|Azure)",
            "GCP": r"(?i)(Google GCP|Google Cloud|Google|GCP)",
            "IBM": r"(?i)(IBM Cloud|IBM)",
            "MongoDB": r"(?i)(MongoDB|MongoDB Cloud|MongoDB Atlas)",
            "Akamai": r"(?i)(Akamai|Akamai Technologies)",
            "Macrometa": r"(?i)(Macrometa|Macrometa GDN)",
            "Cloudflare": r"(?i)(Cloudflare|CloudFlare Inc)",
            "Databricks": r"(?i)(Databricks)",
            "Salesforce": r"(?i)(Salesforce|SFDC)",
            "Snowflake": r"(?i)(Snowflake|Snowflake Inc)",
            "Oracle": r"(?i)(Oracle Cloud|OCI|Oracle Corporation|Oracle Database)",
        }
    
    # Extended service patterns for specific providers
    service_patterns = {
        "AWS": [
            # API & Gateway Services
            r"(?i)(Amazon API Gateway|API Gateway|AGW)",
            r"(?i)(Amazon Direct Connect|Direct Connect|Direct Connect trac|DC)",
            # AI/ML Services
            r"(?i)(Amazon Bedrock|Bedrock|ABR)",
            # Serverless Messaging
            r"(?i)(Amazon Kinesis|Kinesis|AKN)",
            # CDN & DNS Services
            r"(?i)(Amazon CloudFront|CloudFront|CF)",
            r"(?i)(Amazon Route 53|Route 53|R53|DNS)",
            # Monitoring & Insights
            r"(?i)(Amazon CloudWatch|CloudWatch|CW|CloudWatch Application Insights|CloudWatch Events and EventBridge)",
            r"(?i)(Amazon CodeGuru Profiler|CodeGuru|CGP)",
            # Data Services
            r"(?i)(Amazon DataZone|DataZone|ADZ)",
            r"(?i)(Amazon DocumentDB|DocumentDB|DDB)",
            r"(?i)(Amazon DynamoDB|DynamoDB|DDB)",
            r"(?i)(Amazon RDS|RDS|Relational Database Service)",
            r"(?i)(Amazon Aurora Serverless|Aurora|AAS)",
            # Compute Services
            r"(?i)(Amazon EC2 Instance Connect|EC2 Instance Connect|Instance Connect|EIC)",
            r"(?i)(Aazon Elastic Compute Cloud|Amazon EC2|EC2|Elastic Compute Cloud)",
            r"(?i)(Amazon ECS|ECS|Elastic Container Service)",
            # Storage Services
            r"(?i)(Amazon Elastic File System|Amazon EFS|EFS|Elastic File System)",
            r"(?i)(Amazon Elastic Block Store|Amazon EBS|EBS|Elastic Block Store)",
            # Load Balancing
            r"(?i)(Amazon Elastic Load Balancing|Amazon ELB|ELB|Elastic Load Balancing)",
            # Analytics Services
            r"(?i)(Amazon EMR|EMR|Elastic MapReduce)",
            r"(?i)(Amazon EMR Serverless|EMR Serverless)",
            r"(?i)(Amazon ElastiCache|ElastiCache|EC)",
            r"(?i)(Amazon FinSpace|FinSpace)",
            r"(?i)(Amazon QuickSight|QuickSight|QS)",
            # Serverless
            r"(?i)(Amazon AWS Lambda|AWS Lambda|Amazon Lambda|Lambda|lambda|λ)",
            r"(?i)(Amazon AWS Step Functions|AWS Step Functions|Step Functions|SF)",
            # Data Processing
            r"(?i)(Amazon Redshift|Redshift|RS)",
            r"(?i)(Amazon AWS Glue|AWS Glue|Glue)",
            # Container Services
            r"(?i)(Amazon AWS Fargate|AWS Fargate|Fargate)",
            r"(?i)(Amazon Elastic Kubernetes Service|Amazon EKS|EKS|Elastic Kubernetes Service|Kubernetes Service)",
            r"(?i)(Amazon s3|Amazon S3|s3|S3|Simple Storage Service)",
        ],
        "GCP": [
            # AI/ML Services
            r"(?i)(Google Cloud VertexAI|VertexAI|VAI)",
            r"(?i)(Google Cloud Machine Learning|ML Engine|GCML)",
            # API Services
            r"(?i)(Google Cloud Apigee API|Apigee|GAPI)",
            # Compute Services
            r"(?i)(Google Cloud Run|Cloud Run|GCR)",
            # Data Services
            r"(?i)(Google Cloud BigQuery|BigQuery|BQ)",
            r"(?i)(AlloyDB for PostgreSQL|AlloyDB|ADB)",
            r"(?i)(Google Cloud SQL|Cloud SQL|GCS)",
            r"(?i)(Google Cloud Bigtable|Bigtable|CBT)",
            # Compute & Processing
            r"(?i)(Google Cloud Compute Engine|Compute Engine|GCE)",
            r"(?i)(Google Cloud Dataproc|Dataproc|DP)",
            r"(?i)(Google Cloud Dataflow|Dataflow|DF)",
            # Storage
            r"(?i)(Google Cloud Storage|GCS|Cloud Storage)",
            # Analytics
            r"(?i)(Google Cloud DataStudio|DataStudio|DS)",
            r"(?i)(Google Cloud Datalab|Datalab|DL)",
            r"(?i)(Google Cloud Composer|Composer|GCC)",
            r"(?i)(Google Cloud Looker Studio Pro|Looker|LSP)",
            # Security
            r"(?i)(Google Cloud reCAPTCHA Enterprise|reCAPTCHA|RCE)",
            # Network Services
            r"(?i)(Google Cloud Load Balancing|Load Balancing|GCLB)",
            r"(?i)(Google Cloud And Media CDN|Media CDN|GCDN)",
            r"(?i)(Google Cloud DNS|Cloud DNS|GCDNS)",
            # Container Services
            r"(?i)(Google Kubernetes Engine (GKE)|Google Kubernetes Engine|GKE)",
            r"(?i)(Google Cloud Functions|Cloud Functions|GCF)",
            r"(?i)(Google Cloud Pub/Sub|Pub/Sub|GCP Pub/Sub)",
            # Google Distributed Cloud Edge
            r"(?i)(Google Distributed Cloud Edge|Distributed Cloud Edge|GDC Edge)",
        ],
        "Azure": [
            # Identity Services
            r"(?i)(Azure Active Directory AAD|Azure Active Directory|Azure AD|AAD|AD)",
            r"(?i)(Microsoft Entra ID|Entra ID|EID)",
            r"(?i)(Azure Active Directory B2C|Azure AD B2C|AAD B2C)",
            # AI/ML Services
            r"(?i)(Azure Machine Learning|AML|Azure ML)",
            r"(?i)(Azure AI|AAI)",
            r"(?i)(Azure AI Search|Cognitive Search|AIS)",
            r"(?i)(Azure OpenAI Service|Azure OpenAI|AOAI)",
            # API Services
            r"(?i)(Azure API Management|APIM)",
            # Data Services
            r"(?i)(Azure Databricks|ADB|Databricks)",
            r"(?i)(Azure SQL Managed Instance|SQL MI|ASQLMI)",
            r"(?i)(Azure SQL Database|SQL DB|ASDB)",
            r"(?i)(Azure Cosmos DB|Cosmos|ACDB)",
            r"(?i)(Azure Database for PostgreSQL|Azure PostgreSQL|APS)",
            r"(?i)(Azure Database for MySQL|Azure MySQL|AMS)",
            # Compute Services
            r"(?i)(Azure Batch|Batch)",
            r"(?i)(Azure App Service|App Service|AAS)",
            r"(?i)(Azure Functions|Functions|AF)",
            # Analytics
            r"(?i)(Azure PowerBI App|PowerBI|PBI)",
            # Network Services
            r"(?i)(Azure CDN|Content Delivery Network)",
            # Storage
            r"(?i)(Azure Storage Accounts|Azure Storage|ASA)",
            # Container Services
            r"(?i)(Azure Kubernetes Service|AKS)",
            r"(?i)(Azure Blob Storage|Blob Storage|ABS|ADLS|ADLS2)",
            r"(?i)(Azure Logic Apps|Logic Apps|ALA)",
            # Azure MongoDB
            r"(?i)(Azure Cosmos DB for MongoDB|Cosmos DB for MongoDB|Cosmos DB for MongoDB|Cosmos DB|Cosmos|MongoDB|MongoDB Cloud|MongoDB|mongodb|MongoDB Atlas)",
        ],
        "IBM": [
            # AI/ML Services
            r"(?i)(IBM Watson Platform|Watson|IWP)",
            # Storage Services
            r"(?i)(IBM Dedicated Storage Instance|Storage Instance|DSI)",
            # Data Services
            r"(?i)(IBM Data Engine|SQL Query|IDE)",
            r"(?i)(IBM Data Product Hub|DPH)",
            r"(?i)(IBM Databases|IDB)",
            r"(?i)(IBM Databases for DataStax|DataStax|IDD)",
            r"(?i)(IBM Databases for EDB|EDB|IDE)",
            r"(?i)(IBM Databases for Elasticsearch|Elasticsearch|IDE)",
            r"(?i)(IBM Databases for etcd|etcd|IDE)",
            r"(?i)(IBM Databases for MongoDB|MongoDB|IDM)",
            r"(?i)(IBM Databases for MySQL|MySQL|IDM)",
            r"(?i)(IBM Databases for PostgreSQL|PostgreSQL|IDP)",
            r"(?i)(IBM Databases for Redis|Redis|IDR)",
            r"(?i)(IBM DataStage|DataStage|IDS)",
            r"(?i)(IBM Db2|Db2)",
            r"(?i)(IBM Db2 Warehouse|Db2W)",
            # Analytics
            r"(?i)(IBM watsonx BI Assistant|BI Assistant|WBA)",
            # Storage
            r"(?i)(IBM Cloud Object Storage|Object Storage|COS)",
            # Management
            r"(?i)(IBM Cloud Console|Console|ICC)",
            # Container Services
            r"(?i)(IBM Kubernetes|IKS)",
            r"(?i)(Red Hat OpenShift on IBM Cloud|OpenShift|RHOIC)",
            # BareMetal servers
            r"(?i)(BareMetal servers|BareMetal|BM)",
            # Load Balancers
            r"(?i)(Load Balancers|Load Balancer|LB)",
            # VSI-San Storage
            r"(?i)(VSI-San Storage|VSI-San|VSIs|VSI)",
            # API Connect
            r"(?i)(OCI API Connect|API Connect|API|APIC)",
            # Compute
            r"(?i)(OCI Compute|Compute|OCI Compute Cloud|Compute Cloud|Compute)",
            # Network
            r"(?i)(OCI Network|Network|OCI Network Cloud|Network Cloud|Network)",
            # Storage
            r"(?i)(OCI Storage|Storage|OCI Storage Cloud|Storage Cloud|Storage)",
            # Database
            r"(?i)(OCI Database|Database|OCI Database Cloud|Database Cloud|Database)",
            # API Gateway
            r"(?i)(OCI API Gateway|API Gateway|OCI API|API)",
            #Cloudant NoSQL DB
            r"(?i)(Cloudant NoSQL DB|Cloudant|NoSQL DB)",
        ],
        "Oracle": [
            # Database Services
            r"(?i)(Oracle AutonomousDB 21c|AutonomousDB|ADB)",
            # Storage Services
            r"(?i)(Object Storage OCI|OCI Storage|OCIS)",
            # Data Services
            r"(?i)(Oracle Big Data Service|BDS|OBDS)",
            # Oracle Cloud Infrastructure Container Engine for Kubernetes (OKE)
            r"(?i)(Oracle Cloud Infrastructure Container Engine for Kubernetes (OKE)|Oracle Cloud Infrastructure Container Engine for Kubernetes|Oracle Kubernetes Service (OKE)|Oracle Kubernetes Service|OKE)",
            # Oracle Identity Cloud
            r"(?i)(Oracle Identity Cloud|OCI Identity|OCI Identity Cloud|Identity Cloud|Identity)",
            # Oracle Cloud Infrastructure Compute
            r"(?i)(Oracle Cloud Infrastructure Compute|OCI Compute|OCI Compute Cloud|Compute Cloud|Compute)",
            # Oracle Cloud Infrastructure Object Storage
            r"(?i)(Oracle Cloud Infrastructure Object Storage|OCI Object Storage|OCI Object|Object Storage)",
            # Oracle Cloud Infrastructure Storage
            r"(?i)(Oracle Cloud Infrastructure Storage|OCI Storage|OCI Storage Cloud|Storage Cloud|Storage)",
            # Oracle Cloud Infrastructure Network or Network OCI
            r"(?i)(Oracle Cloud Infrastructure Network|OCI Network|OCI Network Cloud|Network Cloud|Network|Network Oracle Cloud Infrastructure (OCI)|Network OCI|Networking OCI|OCI Networking|OCI Network|Network OCI|Networking|Network)",
            # Oracle Cloud Infrastructure Database
            r"(?i)(Oracle Cloud Infrastructure Database|OCI Database|OCI Database Cloud|Database Cloud|Database)",
            # Oracle Cloud Infrastructure API Gateway
            r"(?i)(Oracle Cloud Infrastructure API Gateway|OCI API Gateway|OCI API|API Gateway)",
            # Oracle Cloud Infrastructure Data Flow
            r"(?i)(Oracle Cloud Infrastructure Data Flow|OCI Data Flow|OCI Data|Data Flow)",
            # Oracle Cloud Infrastructure Events
            r"(?i)(Oracle Cloud Infrastructure Events|OCI Events|OCI Event|Events)",
            # Oracle Cloud Infrastructure Monitoring
            r"(?i)(Oracle Cloud Infrastructure Monitoring|OCI Monitoring|OCI Monitor|Monitoring)",
            # Oracle Cloud Infrastructure Notifications
            r"(?i)(Oracle Cloud Infrastructure Notifications|OCI Notifications|OCI Notification|Notifications)",
            # Oracle Cloud Guard
            r"(?i)(Oracle Cloud Guard|OCI Guard|OCI Guard Cloud|Guard Cloud|Guard)",
            # Oracle Cloud Infrastructure Registry (OCIR)
            r"(?i)(Oracle Cloud Infrastructure Registry (OCIR)|OCI Registry|OCI Registry Cloud|Registry Cloud|Registry)",
            # Oracle Cloud Infrastructure Resource Manager
            r"(?i)(Oracle Cloud Infrastructure Resource Manager|OCI Resource Manager|OCI Resource|Resource Manager)",
            # Oracle Cloud Infrastructure Vulnerability Scanning Service
            r"(?i)(Oracle Cloud Infrastructure Vulnerability Scanning Service|OCI Vulnerability Scanning Service|OCI Vulnerability|Vulnerability Scanning Service)",
            # Oracle Digital Assistant
            r"(?i)(Oracle Digital Assistant|OCI Digital Assistant|OCI Digital|Digital Assistant)",
            # Oracle Functions
            r"(?i)(Oracle Functions|OCI Functions|OCI Function|Functions)",
            # Oracle Integration
            r"(?i)(Oracle Integration|OCI Integration|OCI Integration Cloud|Integration Cloud|Integration)",
            # Oracle Visual Builder
            r"(?i)(Oracle Visual Builder|OCI Visual Builder|OCI Visual|Visual Builder)",
            # Oracle Web Application Firewall (WAF)
            r"(?i)(Oracle Web Application Firewall (WAF)|OCI Web Application Firewall (WAF)|OCI Web Application Firewall|Web Application Firewall (WAF)|Web Application Firewall)",
            # Oracle Cloud Infrastructure API Gateway
            r"(?i)(Oracle Cloud Infrastructure API Gateway|OCI API Gateway|OCI API|API Gateway)",
            # Oracle Cloud VMware Solution
            r"(?i)(Oracle Cloud VMware Solution|OCI VMware Solution|OCI VMware|VMware Solution)",
            # Multiple services
            r"(?i)(Multiple services|Multiple services in|Multiple services in Oracle Cloud Infrastructure (OCI)|Oracle Cloud Infrastructure (OCI))",

        ],
        "Snowflake": [
            r"(?i)(Snowflake on AWS|SFAWS)",
            r"(?i)(Snowflake on Azure|SFA)",
            r"(?i)(Snowflake on GCP|SFGCP)",
        ],
        "Databricks": [
            r"(?i)(Databricks SaaS|DBSAAS)",
            r"(?i)(Databricks Workspace|DBW)",
            r"(?i)(Databricks MLflow|MLflow)",
            r"(?i)(Databricks Notebooks|DBN)",
        ],
        "Salesforce": [
            r"(?i)(Salesforce SaaS|SFSAAS)",
            r"(?i)(Salesforce Sales Cloud|Sales Cloud|SSC)",
            r"(?i)(Salesforce Service Cloud|Service Cloud|SSC)",
            r"(?i)(Salesforce Marketing Cloud|Marketing Cloud|SMC)",
            r"(?i)(Salesforce Mulesoft Anypoint Platform|Mulesoft|MAP)",
        ],
        "MongoDB": [
            r"(?i)(MongoDB Atlas|MongoDB|MongoDB Cloud Atlas|Atlas|mongodb)",
            r"(?i)(MongoDB Atlas AWS|MongoDB AWS|Atlas AWS|mongodb aws)",
            r"(?i)(MongoDB Atlas Azure|MongoDB Azure|Atlas Azure|mongodb azure)",
            r"(?i)(MongoDB Atlas GCP|MongoDB GCP|Atlas GCP|mongodb gcp)",
            r"(?i)(MongoDB Atlas Search|MongoDB Search|Search|Atlas Search|mongodb search)",
            r"(?i)(MongoDB Atlas Vector Search|MongoDB Vector Search|Vector Search|Atlas Vector Search)",
            r"(?i)(MongoDB Atlas Stream Processing|MongoDB Stream Processing|Stream Processing|Atlas Stream Processing)",
            r"(?i)(MongoDB Atlas BI Connector|MongoDB BI Connector|BI Connector|Atlas BI Connector)",
            r"(?i)(MongoDB Atlas SQL|Atlas SQL)",
            r"(?i)(MongoDB Atlas Data Federation|Data Federation)",
            r"(?i)(MongoDB Atlas Online Archive|Online Archive)",
        ],
        "Cloudflare": [
            r"(?i)(AnyCast CloudFlare|AnyCast)",
            r"(?i)(CDN CloudFlare|CF CDN)",
            r"(?i)(Cloudflare DNS|CF DNS)",
            r"(?i)(Cloudflare DDoS Protection|CF DDoS)",
        ],
        "Akamai": [
            r"(?i)(CDN Akamai|Akamai CDN| Akamai)", # Generic Akamai from where it is used by other crossing cloud providers , cross analysis
            r"(?i)(Edge Computing Akamai|Akamai Edge)",
            r"(?i)(Security Akamai|Akamai Security)",
        ],
        "Macrometa": [
            r"(?i)(CDN Macrometa|Macrometa CDN)",
            r"(?i)(Edge Computing Macrometa|Macrometa Edge)",
        ]
    }
    
    # Extended status patterns to include more granular states
    status_patterns = {
        "investigating": r"(?i)(investigating|identified|monitoring|increased error rates|elevated delays|issues|disruption|degradation|intermittent connectivity|under review)",
        "resolved": r"(?i)(resolved|restored|recovered|mitigated|marked as resolved|normal operations|issue fixed)",
        "outage": r"(?i)(complete outage|service disruption|unavailable|increased api errors|increased latencies|service unavailable)",
        "degraded": r"(?i)(degraded performance|degraded service|partial outage|intermittent connectivity|elevated packet loss|impaired|congestion)",
        "maintenance": r"(?i)(scheduled maintenance|planned downtime|maintenance window)",
        "recovering": r"(?i)(recovery in progress|partially recovered|improvement observed|started seeing recovery)",
        "active": r"(?i)(active incident|ongoing|in progress|currently investigating)",
        "planned": r"(?i)(planned maintenance|scheduled work|upcoming maintenance)",
        "warning": r"(?i)(warning|potential issue|monitoring closely|increased latency)",
    }
    
    # Extended impact patterns to include more specific levels
    impact_patterns = {
        "critical": r"(?i)(critical impact|severe impact|major outage|complete failure|service unavailable|widespread disruption|total service failure)",
        "high": r"(?i)(high impact|significant impact|service degradation|multiple services affected|major service disruption)",
        "moderate": r"(?i)(moderate impact|partial impact|minor outage|increased error rates|intermittent issues)",
        "minimal": r"(?i)(minimal impact|slight impact|limited disruption|elevated delays|degraded performance)",
        "none": r"(?i)(no impact|no outage reported|normal operation)",
        "regional": r"(?i)(regional impact|specific region affected|isolated to region)",
        "global": r"(?i)(global impact|worldwide|all regions affected)",
        "service-specific": r"(?i)(specific service|single service affected|limited to)",
    }
    
    # Add incident ID pattern
    incident_patterns = [
        r"(?i)Incident(?:\s+ID)?:\s*([^\n]+)",
        r"(?i)Event(?:\s+ID)?:\s*([^\n]+)",
        r"(?i)Reference(?:\s+Number)?:\s*([^\n]+)",
        r"(?i)Incident Number:\s*([^\n]+)",
    ]
    
    # Enhanced affected components patterns
    affected_components_patterns = [
        r"(?i)Affected(?:\s+Components?)?:\s*([^\n]+)",
        r"(?i)Impacted(?:\s+Components?)?:\s*([^\n]+)",
        r"(?i)Components?\s+Affected:\s*([^\n]+)",
        r"(?i)Impacted Components:\s*([^\n]+)",
    ]
    
    # Enhanced mitigation steps patterns
    mitigation_patterns = [
        r"(?i)Mitigation(?:\s+Steps?)?:\s*([^\n]+)",
        r"(?i)Resolution(?:\s+Steps?)?:\s*([^\n]+)",
        r"(?i)Steps?\s+Taken:\s*([^\n]+)",
        r"(?i)Actions?\s+Taken:\s*([^\n]+)",
        r"(?i)Actions Taken:\s*([^\n]+)",
    ]
    
    # Enhanced timestamp patterns with more flexibility
    time_patterns = {
        "start": [
            r"(?i)Start(?:ed)?(?:\s+Time)?:\s*([^\n]+)",
            r"(?i)Impact Date(?: and Time)?:\s*([^\n]+)",
            r"(?i)The outage started (?:at)?\s*([^\n]+)",
            r"(?i)Downtime Period:\s*The outage started (?:on)?\s*([^\n]+)\s*and ended",
            r"(?i)Downtime Period:\s*([\w\s,:\-\/]+)(?:\sand\s|\sto\s|\s-\s)(?:[\w\s,:\-\/]+)",
            r"(?i)Outage\s+started[:\s]*\s*([^\n]+)",
            r"(?i)Began\s+on\s*([^\n]+)",
        ],
        "end": [
            r"(?i)End(?:ed)?(?:\s+Time)?:\s*([^\n]+)",
            r"(?i)Resolved(?: Date(?: and Time)?)?:\s*([^\n]+)",
            r"(?i)The outage (?:ended|resolved) (?:at)?\s*([^\n]+)",
            r"(?i)Downtime Period:.*?and ended (?:on)?\s*([^\n]+)",
            r"(?i)Downtime Period:\s*(?:[\w\s,:\-\/]+)\s*(?:\sand\s|\sto\s|\s-\s)\s*([\w\s,:\-\/]+)",
            r"(?i)Resolved\s+Date:\s*([^\n]+)",
            r"(?i)Restored at\s*([^\n]+)",
        ]
    }
    
    # Enhanced duration patterns to account for variations and incorrect formats
    duration_patterns = [
        r"(?i)Duration(?: of outage)?:\s*([^\n]+)",
        r"(?i)Duration:\s*([^\n]+)",
        r"(?i)Lasted for[:\s]*\s*([^\n]+)",
        r"(?i)(\d+\s*(?:day|days|hour|hours|minute|minutes|hrs|mins)[,\s]*(?:and\s*)?\d*\s*(?:day|days|hour|hours|minute|minutes|hrs|mins)?[,\s]*(?:and\s*)?\d*\s*(?:day|days|hour|hours|minute|minutes|hrs|mins)?)",
        r"(?i)Downtime Period:\s*.*?\(([\d\s]+(?:day|days|hour|hours|minute|minutes|hrs|mins)[^\)]*)\)",
        r"(?i)Total Duration:\s*([^\n]+)",
        r"(?i)Duration of impact:\s*([^\n]+)",
    ]

    # Enhanced region patterns
    region_patterns = [
        r"(?i)Region(?:s)?(?:\s+Affected)?:\s*([^\n]+)",
        r"(?i)in\s+(?:the\s+)?([\w\s-]+)\s+Region",
        r"(?i)((?:us|eu|ap|sa|ca|me)-(?:east|west|north|south|central|southeast|northeast)-\d+)",
        r"(?i)(Northern Virginia|Tokyo|Seoul|Singapore|London|Frankfurt|Paris|Sydney)",
        r"(?i)Regions impacted:\s*([^\n]+)",
    ]

    # Enhanced root cause patterns
    root_cause_patterns = [
        r"(?i)Root Cause(?: of the outage)?:\s*([^\n]+)",
        r"(?i)Root cause:\s*([^\n]+)"
    ]

    # Enhanced multi-line outage patterns
    multi_line_outage_patterns = [
        r"(?i)Outage\s+\d+:\s*[\s\S]*?Service impacted:\s*([^\n]+)[\s\S]*?Region:\s*([^\n]*)[\s\S]*?Availability Zone:\s*([^\n]*)[\s\S]*?Root cause:\s*([^\n]*)[\s\S]*?Duration:\s*([^\n]*)[\s\S]*?Start date:\s*([^\n]*)[\s\S]*?Downtime period:\s*([^\n]*)[\s\S]*?Resolution date:\s*([^\n]*)",
        r"(?i)Outage\s+\d+:\s*[\s\S]*?Service affected:\s*([^\n]+)[\s\S]*?Region impacted:\s*([^\n]*)[\s\S]*?Root cause identified:\s*([^\n]*)[\s\S]*?Duration of outage:\s*([^\n]*)",
    ]

    # New patterns for extracting additional information
    new_duration_patterns = [
        r"(?i)Duration:\s*([^\n]+)",
        r"(?i)(\d+)\s*(?:days?|hours?|minutes?|hrs?|mins?)",
        r"(?i)lasted\s+(?:for\s+)?(\d+\s+(?:days?|hours?|minutes?|hrs?|mins?)(?:\s+and\s+\d+\s+(?:days?|hours?|minutes?|hrs?|mins?))*)",
        r"(?i)Total Duration:\s*([^\n]+)",
    ]

    new_downtime_patterns = [
        r"(?i)Downtime period:\s*([^\n]+)",
        r"(?i)Downtime\s+period:\s*([^\n]+)",
        r"(?i)Downtime Duration:\s*([^\n]+)",
    ]

    new_root_cause_patterns = [
        r"(?i)Root cause of the outage:\s*([^\n]+)",
        r"(?i)Root Cause:\s*([^\n]+)",
    ]

    new_region_patterns = [
        r"(?i)Regions?\s+Affected:\s*([^\n]+)",
        r"(?i)Affected Regions and Availability Zones:\s*([^\n]+)",
        r"(?i)Affected Regions:\s*([^\n]+)",
    ]
    
    # Add new patterns for additional information extraction
    new_affected_components_patterns = [
        r"(?i)Affected Services:\s*([^\n]+)",
        r"(?i)Services Impacted:\s*([^\n]+)"
    ]
    
    new_mitigation_patterns = [
        r"(?i)Mitigation Actions:\s*([^\n]+)",
        r"(?i)Resolution Actions:\s*([^\n]+)"
    ]
    
    new_time_patterns = {
        "start": [
            r"(?i)Outage Start Time:\s*([^\n]+)",
            r"(?i)Incident Start:\s*([^\n]+)"
        ],
        "end": [
            r"(?i)Outage End Time:\s*([^\n]+)",
            r"(?i)Incident Resolved:\s*([^\n]+)"
        ]
    }
    
    new_duration_patterns = [
        r"(?i)Total Outage Duration:\s*([^\n]+)",
        r"(?i)Outage Lasted:\s*([^\n]+)"
    ]
    
    new_region_patterns = [
        r"(?i)Regions Affected:\s*([^\n]+)",
        r"(?i)Impacted Regions:\s*([^\n]+)"
    ]
    
    # Integrate new patterns into existing logic
    affected_components_patterns.extend(new_affected_components_patterns)
    mitigation_patterns.extend(new_mitigation_patterns)
    for key in time_patterns:
        time_patterns[key].extend(new_time_patterns[key])
    duration_patterns.extend(new_duration_patterns)
    region_patterns.extend(new_region_patterns)
    
    # New patterns for Google Cloud Service Health incident format
    new_service_patterns = [
        r"(?i)Service:\s*([^\n]+)"
    ]
    
    new_region_patterns = [
        r"(?i)Region:\s*([^\n]+)"
    ]
    
    new_availability_zone_patterns = [
        r"(?i)Availability Zone:\s*([^\n]+)"
    ]
    
    new_impact_date_patterns = [
        r"(?i)Impact Date:\s*([^\n]+)"
    ]

    new_impact_dates_patterns = [
        r"(?i)Impact Dates:\s*([^\n]+)"
    ]
    
    new_duration_patterns = [
        r"(?i)Duration:\s*([^\n]+)"
    ]
    
    new_root_cause_patterns = [
        r"(?i)Root Cause:\s*([^\n]+)"
    ]
    
    new_downtime_period_patterns = [
        r"(?i)Downtime Period:\s*([^\n]+)"
    ]
    
    new_resolved_date_patterns = [
        r"(?i)Resolved Date:\s*([^\n]+)"
    ]
    
    # Integrate new patterns into existing logic
    service_patterns["GCP"].extend(new_service_patterns)
    region_patterns.extend(new_region_patterns)
    availability_zone_patterns = new_availability_zone_patterns  # Assuming this is a new addition
    time_patterns["start"].extend(new_impact_date_patterns)
    time_patterns["start"].extend(new_impact_dates_patterns)
    duration_patterns.extend(new_duration_patterns)
    root_cause_patterns.extend(new_root_cause_patterns)
    downtime_period_patterns = new_downtime_period_patterns  # Assuming this is a new addition
    resolved_date_patterns = new_resolved_date_patterns  # Assuming this is a new addition
    
    # Add new patterns for Impact Date and Impact Dates
    impact_date_patterns = [
        r"(?i)Impact Date:\s*([^\n]+)",
        r"(?i)Impact Dates:\s*([^\n]+)"
    ]
    
    # Split text into sections by outage
    sections = re.split(r"--\nOutage Filename:", text)
    
    # Before adding regions to outage.regions, standardize the region names
    # For example, map "Northern Virginia" to "us-east-1" for AWS

    # Add this function inside 'merger.py'
    def standardize_region_name(provider: str, region_name: str) -> str:
        """Standardize region names based on provider."""
        region_name = region_name.strip()
        if not provider or not region_name:
            return region_name
        provider_regions = valid_regions.get(provider, [])

        # Map common names to standardized region IDs
        region_aliases = {
            "AWS": {
                # US Regions
                "Northern Virginia": "us-east-1",
                "Ohio": "us-east-2",
                "N. California": "us-west-1",
                "Northern California": "us-west-1",
                "Oregon": "us-west-2",
                # Asia Pacific
                "Tokyo": "ap-northeast-1",
                "Seoul": "ap-northeast-2",
                "Osaka": "ap-northeast-3",
                "Singapore": "ap-southeast-1",
                "Sydney": "ap-southeast-2",
                "Mumbai": "ap-south-1",
                # Europe
                "Ireland": "eu-west-1",
                "London": "eu-west-2",
                "Paris": "eu-west-3",
                "Frankfurt": "eu-central-1",
                "Stockholm": "eu-north-1",
                # Other
                "São Paulo": "sa-east-1",
                "Sao Paulo": "sa-east-1",
                "Canada": "ca-central-1",
            },
            "Azure": {
                # US Regions
                "East US": "eastus",
                "East US 2": "eastus2",
                "Central US": "centralus",
                "North Central US": "northcentralus",
                "South Central US": "southcentralus",
                "West US": "westus",
                "West US 2": "westus2",
                "West US 3": "westus3",
                # Europe
                "North Europe": "northeurope",
                "West Europe": "westeurope",
                "UK South": "uksouth",
                "UK West": "ukwest",
                # Asia Pacific
                "East Asia": "eastasia",
                "Southeast Asia": "southeastasia",
                "Japan East": "japaneast",
                "Japan West": "japanwest",
                "Australia East": "australiaeast",
                "Australia Southeast": "australiasoutheast",
            },
            "GCP": {
                # US Regions
                "Iowa": "us-central1",
                "South Carolina": "us-east1",
                "Northern Virginia": "us-east4",
                "Oregon": "us-west1",
                "Los Angeles": "us-west2",
                "Salt Lake City": "us-west3",
                "Las Vegas": "us-west4",
                # Europe
                "Belgium": "europe-west1",
                "London": "europe-west2",
                "Frankfurt": "europe-west3",
                "Netherlands": "europe-west4",
                "Zurich": "europe-west6",
                "Milan": "europe-west8",
                "Paris": "europe-west9",
                # Asia Pacific
                "Taiwan": "asia-east1",
                "Hong Kong": "asia-east2",
                "Tokyo": "asia-northeast1",
                "Osaka": "asia-northeast2",
                "Seoul": "asia-northeast3",
                "Mumbai": "asia-south1",
                "Delhi": "asia-south2",
                "Singapore": "asia-southeast1",
                "Jakarta": "asia-southeast2",
            },
            "Oracle": {
                # US Regions
                "Ashburn": "us-ashburn-1",
                "Phoenix": "us-phoenix-1",
                "San Jose": "us-sanjose-1",
                "Chicago": "us-chicago-1",
                # Europe
                "Frankfurt": "eu-frankfurt-1",
                "London": "uk-london-1",
                "Amsterdam": "nl-amsterdam-1",
                "Zurich": "eu-zurich-1",
                "Paris": "eu-paris-1",
                "Marseille": "eu-marseille-1",
                "Milan": "eu-milan-1",
                "Stockholm": "eu-stockholm-1",
                # Asia Pacific
                "Tokyo": "ap-tokyo-1",
                "Osaka": "ap-osaka-1",
                "Seoul": "ap-seoul-1",
                "Chuncheon": "ap-chuncheon-1",
                "Singapore": "ap-singapore-1",
                "Mumbai": "ap-mumbai-1",
                "Hyderabad": "ap-hyderabad-1",
            },
            "IBM": {
                # US Regions
                "Dallas": "us-south",
                "Washington DC": "us-east",
                # Europe
                "London": "eu-gb",
                "Frankfurt": "eu-de",
                # Asia Pacific
                "Sydney": "au-syd",
                "Tokyo": "jp-tok",
                "Osaka": "jp-osa",
                "Seoul": "kr-seo",
            },
            "MongoDB": {
                # Using AWS region names since MongoDB Atlas runs on AWS
                "N. Virginia": "us-east-1",
                "Oregon": "us-west-2",
                "Ireland": "eu-west-1",
                "Frankfurt": "eu-central-1",
                "Mumbai": "ap-south-1",
                "Singapore": "ap-southeast-1",
            },
            "Snowflake": {
                # Mapped to underlying cloud provider regions
                "US East": "aws-us-east-1",
                "US West": "aws-us-west-2",
                "EU Central": "azure-westeurope",
                "Asia Pacific": "gcp-asia-southeast1",
            },
            "Databricks": {
                # Using underlying cloud provider regions
                "US East": "aws-us-east-1",
                "EU West": "azure-westeurope",
                "Asia Southeast": "gcp-asia-southeast1",
            },
            "Salesforce": {
                # Generic region mapping
                "North America": "na1",
                "Europe": "eu1",
                "Asia Pacific": "ap1",
            }
        }

        # Get provider-specific aliases
        aliases = region_aliases.get(provider, {})
        
        # Try to match the region name directly
        standardized_name = aliases.get(region_name, region_name)
        
        # If no direct match, try case-insensitive matching
        if standardized_name == region_name:
            for alias, std_name in aliases.items():
                if region_name.lower() == alias.lower():
                    return std_name
        
        return standardized_name

    # Add helper function to handle unspecified regions
    def handle_unspecified_region(provider: str, region_text: str) -> List[str]:
        """Handle cases where region is marked as unspecified/unknown"""
        if not region_text or region_text.lower() in ['not specified', 'not declared', 'unknown', '', 'none']:
            # Return all valid regions for the provider as a fallback
            return valid_regions.get(provider, [])
        
        # Split and clean the region text
        regions = re.split(r'[,•*]+', region_text)
        cleaned_regions = []
        
        for region in regions:
            region = region.strip()
            if region and region.lower() not in ['not specified', 'not declared', 'unknown', '', 'none']:
                standardized = standardize_region_name(provider, region)
                if standardized:
                    cleaned_regions.append(standardized)
        
        # If no valid regions found after cleaning, return all valid regions
        return cleaned_regions if cleaned_regions else valid_regions.get(provider, [])

    for section in sections:
        # Skip empty sections
        if not section.strip():
            continue
            
        # Extract filename if present
        filename_match = re.match(r'\s*\./?(.*?)\s*\n', section)
        if filename_match:
            current_filename = filename_match.group(1)
            section = section[filename_match.end():]  # Remove filename from section
            
        outage = OutageInfo()
        outage.source_outage_report = current_filename.replace('.txt', '')
        
        # Initialize a set to track excluded providers
        excluded_providers = set()

        # Check for the phrase indicating the provider was not mentioned
        for provider in provider_patterns.keys():
            if f"{provider} was not mentioned in the text" in section:
                excluded_providers.add(provider)

        # Identify cloud provider
        identified_providers = []
        for provider, pattern in provider_patterns.items():
            if provider not in excluded_providers and re.search(pattern, section):
                identified_providers.append(provider)

        # If more than one provider is identified, exclude those that were not mentioned
        if len(identified_providers) > 1:
            identified_providers = [provider for provider in identified_providers if provider not in excluded_providers]

        # Assign the first N identified provider if any
        # TODO : Changed logic to capture multi-cloud incidents like JULY Azure impacting MongoDB, Databricks and others.
        # Extended provider patterns
        provider_patterns = {
            "AWS": r"(?i)(Amazon AWS|AWS|Amazon Web Services|Amazon|AWS Cloud)",
            "Azure": r"(?i)(Microsoft Azure|Microsoft|Azure)",
            "GCP": r"(?i)(Google GCP|Google Cloud|Google|GCP)",
            "IBM": r"(?i)(IBM Cloud|IBM)",
            "MongoDB": r"(?i)(MongoDB|MongoDB Cloud|MongoDB Atlas)",
            "Akamai": r"(?i)(Akamai|Akamai Technologies)",
            "Macrometa": r"(?i)(Macrometa|Macrometa GDN)",
            "Cloudflare": r"(?i)(Cloudflare|CloudFlare Inc)",
            "Databricks": r"(?i)(Databricks)",
            "Salesforce": r"(?i)(Salesforce|SFDC)",
            "Snowflake": r"(?i)(Snowflake|Snowflake Inc)",
            "Oracle": r"(?i)(Oracle Cloud|OCI|Oracle Corporation|Oracle Database)",
        }

        # First check if provider can be determined from filename
        provider_from_filename = None
        if current_filename:
            for provider, pattern in provider_patterns.items():
                # Match to outage.source_outage_report
                if re.search(pattern, outage.source_outage_report , re.IGNORECASE): 
                    provider_from_filename = provider
                    break
        
        # Assign provider with priority to filename match
        if provider_from_filename:
            outage.cloud_provider = provider_from_filename
        elif identified_providers:
            outage.cloud_provider = identified_providers[0]

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
        common_patterns = {
            "regions": r"(?i)Regions?(?:\s+Affected)?:\s*([^\n]+)",
            "availability_zones": r"(?i)Availability Zones?(?:\s+Affected)?:\s*([^\n]+)",
            "root_cause": r"(?i)Root Cause(?: of the outage)?:\s*([^\n]+)",
            "duration": r"(?i)Duration(?: of outage)?:\s*([^\n]+)",
            "downtime_period": r"(?i)Downtime Period(?: of outage)?:\s*([^\n]+)",
            "resolved_date": r"(?i)Resolved Date(?: and Time)?:\s*([^\n]+)"
        }
        
        for field, pattern in common_patterns.items():
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
                region_text = match.group(1).strip()
                regions = handle_unspecified_region(outage.cloud_provider, region_text)
                for region in regions:
                    if region not in outage.regions:
                        outage.regions.append(region)
        
        # If no regions were found, add all valid regions for the provider
        if not outage.regions and outage.cloud_provider:
            outage.regions = valid_regions.get(outage.cloud_provider, [])
            # Use just the first region
            if outage.regions:
                outage.regions = [outage.regions[0]]
        
        # Extract duration using multiple patterns
        for pattern in duration_patterns:
            match = re.search(pattern, section)
            if match:
                outage.duration = match.group(1).strip()
                break
        
        # Extract start and end times using updated patterns
        for field, patterns in time_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, section)
                if match:
                    timestamp_str = match.group(1).strip()
                    timestamp = parse_timestamp(timestamp_str)  # Use parse_timestamp instead of parse_date
                    if timestamp:
                        if field == "start":
                            outage.start_time = timestamp
                        elif field == "end":
                            outage.end_time = timestamp
                        break  # Exit the loop if a timestamp is found
                        
        # New logic to use Impact Date as a fallback for start_time
        if outage.start_time is None:
            for pattern in impact_date_patterns:
                match = re.search(pattern, section)
                if match:
                    timestamp_str = match.group(1).strip()
                    timestamp = parse_timestamp(timestamp_str)  # Use parse_timestamp instead of parse_date
                    if timestamp:
                        outage.start_time = timestamp
                        break  # Exit the loop if a timestamp is found
        
        # Try to extract start time from the source outage report name before using default time
        if outage.start_time is None and current_filename:
            filename_date_str = parse_filename_date(current_filename)
            if filename_date_str:
                timestamp = parse_timestamp(filename_date_str)  # Use parse_timestamp instead of parse_date
                if timestamp:
                    outage.start_time = timestamp
        
        # Existing logic to apply default time if no start_time is found
        if outage.start_time is None:
            outage.start_time = default_time
        
        # Calculate missing start_time or end_time using duration or downtime_period
        if outage.start_time is not None and outage.end_time is None and outage.duration:
            outage.end_time = outage.start_time + timedelta(minutes=calculate_duration_in_minutes(outage.duration))
        elif outage.end_time is not None and outage.start_time is None and outage.duration:
            outage.start_time = outage.end_time - timedelta(minutes=calculate_duration_in_minutes(outage.duration))
        
        # If duration is not available, try using downtime_period
        if outage.start_time is not None and outage.end_time is None and outage.downtime_period:
            outage.end_time = outage.start_time + timedelta(minutes=calculate_duration_in_minutes(outage.downtime_period))
        elif outage.end_time is not None and outage.start_time is None and outage.downtime_period:
            outage.start_time = outage.end_time - timedelta(minutes=calculate_duration_in_minutes(outage.downtime_period))
        
        # Extract incident ID
        for pattern in incident_patterns:
            match = re.search(pattern, section)
            if match:
                outage.incident_id = match.group(1).strip()
                break
        
        # Extract affected components
        for pattern in affected_components_patterns:
            match = re.search(pattern, section)
            if match:
                components = re.split(r'[,•*]+', match.group(1))
                outage.affected_components.extend([c.strip() for c in components if c.strip()])
        
        # Extract mitigation steps
        for pattern in mitigation_patterns:
            match = re.search(pattern, section)
            if match:
                steps = re.split(r'[;\n]+', match.group(1))
                outage.mitigation_steps.extend([s.strip() for s in steps if s.strip()])
        
        # Extract additional fields using new patterns
        # Duration extraction already handled above
        
        # Extract downtime period using new patterns
        for pattern in new_downtime_patterns:
            match = re.search(pattern, section)
            if match:
                outage.downtime_period = match.group(1).strip()
                break
        
        # Extract root cause using new patterns
        for pattern in root_cause_patterns:
            match = re.search(pattern, section)
            if match:
                outage.root_cause = match.group(1).strip()
                break
        
        # Extract regions using new patterns
        for pattern in new_region_patterns:
            match = re.search(pattern, section)
            if match:
                regions = re.split(r'[,•*]+', match.group(1))
                outage.regions.extend([r.strip() for r in regions if r.strip()])
        
        # Extract outage details using multi-line patterns
        for pattern in multi_line_outage_patterns:
            matches = re.finditer(pattern, section)
            for match in matches:
                detailed_outage = OutageInfo()  # Create a new OutageInfo object
                detailed_outage.service = match.group(1).strip()
                detailed_outage.region = match.group(2).strip()
                detailed_outage.availability_zone = match.group(3).strip()
                detailed_outage.root_cause = match.group(4).strip()
                detailed_outage.duration = match.group(5).strip()
                detailed_outage.start_time = parse_timestamp(match.group(6).strip())  # Convert to datetime
                detailed_outage.downtime_period = match.group(7).strip()
                detailed_outage.resolution_time = parse_timestamp(match.group(8).strip())  # Convert to datetime
                outages.append(detailed_outage)
                break  # Exit after the first match
        
        # After parsing start_time and end_time
        # Ensure they are in UTC
        if outage.start_time and outage.start_time.tzinfo is not None:
            outage.start_time = outage.start_time.astimezone(pytz.utc)
        if outage.end_time and outage.end_time.tzinfo is not None:
            outage.end_time = outage.end_time.astimezone(pytz.utc)
        
        # If start_time and end_time are still None, try to parse them from downtime_period
        if outage.start_time is None or outage.end_time is None:
            if outage.downtime_period:
                parsed_times = parse_downtime_period(outage.downtime_period)
                if parsed_times:
                    outage.start_time, outage.end_time = parsed_times
        
        # Calculate outage_timestamp (as epoch time in UTC)
        if outage.start_time:
            outage.outage_timestamp = outage.start_time.timestamp()
        else:
            outage.outage_timestamp = 0.0  # Default if start_time is missing
        
        # Normalize regions to lowercase and remove duplicates
        outage.regions = list(set(region.lower() for region in outage.regions))

        # Normalize availability zones to lowercase and remove duplicates
        outage.availability_zones = list(set(zone.lower() for zone in outage.availability_zones))

        # If no regions but have availability zones, try to speculate regions
        if (not outage.regions or outage.regions == [""]) and outage.availability_zones:
            speculated_regions = set()
            
            for az in outage.availability_zones:
                # Try to speculate region from AZ
                speculated_region = speculate_region_from_az(outage.cloud_provider, az)
                if speculated_region:
                    # Verify if it's a valid region for the provider
                    if outage.cloud_provider in valid_regions:
                        valid_provider_regions = [r.lower() for r in valid_regions[outage.cloud_provider]]
                        if speculated_region.lower() in valid_provider_regions:
                            speculated_regions.add(speculated_region)
                        else:
                            # If speculation doesn't match valid regions, use AZ as is
                            speculated_regions.add(az)
                    else:
                        # If provider not in valid_regions, use AZ as is
                        speculated_regions.add(az)
            
            # Update regions with speculated ones
            if speculated_regions:
                outage.regions = list(speculated_regions)

        outages.append(outage)
    
    return outages

def parse_timestamp(timestamp_str: str) -> Optional[datetime]:
    """
    Flexible timestamp parser that handles various formats found in the logs.
    Returns None if parsing fails.
    """
    try:
        # Clean the timestamp string
        timestamp_str = timestamp_str.strip().rstrip('.')

        # Define timezone mappings
        timezone_mappings = {
            'PDT': -7 * 3600,
            'PST': -8 * 3600,
            'US/Pacific': -8 * 3600,
            'JST': 9 * 3600,
            'JST (UTC+9)': 9 * 3600,
            'JST (UTC9)': 9 * 3600,
            'CST': -6 * 3600,
            'CDT': -5 * 3600,
            'EDT': -4 * 3600,
            'EST': -5 * 3600,
            'UTC-7': -7 * 3600,
            'UTC-8': -8 * 3600,
            'UTC+9': 9 * 3600,
            'UTC': 0,
            'GMT': 0,
            'UT': 0,
            'US': -4 * 3600,
            'UTCC': 0,
        }

        # Parse the timestamp with timezone mappings
        return parser.parse(timestamp_str, fuzzy=True, tzinfos=timezone_mappings)
    except Exception:
        return None

# Add this mapping dictionary after the service_patterns
service_full_names = {
    "AWS": {
        "AGW": "Amazon API Gateway",
        "ABR": "Amazon Bedrock",
        "AKN": "Amazon Kinesis",
        "DC": "Direct Connect",
        "CF": "Amazon CloudFront",
        "R53": "Amazon Route 53",
        "CW": "Amazon CloudWatch",
        "CGP": "Amazon CodeGuru Profiler",
        "ADZ": "Amazon DataZone",
        "DDB": "Amazon DynamoDB",
        "RDS": "Amazon Relational Database Service",
        "AAS": "Amazon Aurora Serverless",
        "EIC": "EC2 Instance Connect",
        "EC2": "Amazon Elastic Compute Cloud",
        "ec2": "Amazon Elastic Compute Cloud",
        "ECS": "Amazon Elastic Container Service",
        "EFS": "Amazon Elastic File System",
        "EBS": "Amazon Elastic Block Store",
        "ELB": "Amazon Elastic Load Balancing",
        "EMR": "Amazon Elastic MapReduce",
        "EC": "Amazon ElastiCache",
        "QS": "Amazon QuickSight",
        "Fargate": "Amazon AWS Fargate",
        "λ": "AWS Lambda",
        "SF": "AWS Step Functions",
        "RS": "Amazon Redshift",
        "EKS": "Amazon Elastic Kubernetes Service",
        "eks": "Amazon Elastuc Kubernetes Service",
        "CWAI": "Amazon CloudWatch Application Insights",
        "DDB": "Amazon DynamoDB",
        "EMRS": "Amazon EMR Serverless",
        "EMR": "Amazon Elastic Mapreduce",
        "FS": "Amazon FinSpace",
        "GL": "Amazon AWS Glue",
        "RDS": "Amazon AWS RDS",
        "rds": "Amazon AWS RDS",
        "s3": "Amazon s3",
        "S3": "Amazon s3"
    },
    "GCP": {
        "VAI": "Google Cloud VertexAI",
        "vai": "Google Cloud VertexAI",
        "GCML": "Google Cloud Machine Learning",
        "GAPI": "Google Cloud Apigee API",
        "GCR": "Google Cloud Run",
        "BQ": "Google Cloud BigQuery",
        "ADB": "AlloyDB for PostgreSQL",
        "GCS": "Google Cloud SQL",
        "CBT": "Google Cloud Bigtable",
        "GCE": "Google Cloud Compute Engine",
        "DP": "Google Cloud Dataproc",
        "DF": "Google Cloud Dataflow",
        "GCS": "Google Cloud Storage",
        "DS": "Google Cloud DataStudio",
        "ds": "Google Cloud DataStudio",
        "DL": "Google Cloud Datalab",
        "dl": "Google Cloud Datalab",
        "GCC": "Google Cloud Composer",
        "LSP": "Google Cloud Looker Studio Pro",
        "RCE": "Google Cloud reCAPTCHA Enterprise",
        "GCLB": "Google Cloud Load Balancing",
        "GCDN": "Google Cloud And Media CDN",
        "GCDNS": "Google Cloud DNS",
        "GKE": "Google Kubernetes Engine (GKE)"
    },
    "Azure": {
        "AAD": "Azure Active Directory",
        "AD": "Azure Active Directory",
        "ad": "Azure Active Directory",
        "aD": "Azure Active Directory",
        "EID": "Microsoft Entra ID",
        "AADB2C": "Azure Active Directory B2C",
        "AML": "Azure Machine Learning",
        "AAI": "Azure AI",
        "AIS": "Azure AI Search",
        "AOAI": "Azure OpenAI Service",
        "APIM": "Azure API Management",
        "ADB": "Azure Databricks",
        "aDB": "Azure Databricks",
        "ASQLMI": "Azure SQL Managed Instance",
        "ASDB": "Azure SQL Database",
        "ACDB": "Azure Cosmos DB",
        "APS": "Azure Database for PostgreSQL",
        "AMS": "Azure Database for MySQL",
        "AB": "Azure Batch",
        "AAS": "Azure App Service",
        "AF": "Azure Functions",
        "Af": "Azure Functions",
        "af": "Azure Functions",
        "PBI": "Azure PowerBI",
        "ACDN": "Azure CDN",
        "ASA": "Azure Storage Accounts",
        "AKS": "Azure Kubernetes Service (AKS)",
        "ABS": "Azure Blob Storage",
        "ADLS": "Azure Blob Storage",
        "ADLS2": "Azure Blog Storage"
    },
    "IBM": {
        "WP": "IBM Watson Platform",
        "DSI": "IBM Dedicated Storage Instance",
        "DE": "IBM Data Engine",
        "DPH": "IBM Data Product Hub",
        "DB": "IBM Databases",
        "DBDS": "IBM Databases for DataStax",
        "DBEDB": "IBM Databases for EDB",
        "DBES": "IBM Databases for Elasticsearch",
        "DBETCD": "IBM Databases for etcd",
        "DBMONGO": "IBM Databases for MongoDB",
        "DBMYSQL": "IBM Databases for MySQL",
        "DBPG": "IBM Databases for PostgreSQL",
        "DBREDIS": "IBM Databases for Redis",
        "DS": "IBM DataStage",
        "DB2": "IBM Db2",
        "DB2W": "IBM Db2 Warehouse",
        "WBIA": "IBM watsonx BI Assistant",
        "FN": "IBM Functions",
        "COS": "IBM Cloud Object Storage",
        "CC": "IBM Cloud Console",
        "K8S": "IBM Kubernetes",
        "IDE": "IBM Cloud IDE",
        "ide": "IBM Cloud IDE",
        "RHOIC": "Red Hat OpenShift on IBM Cloud"
    },
    "OCI": {
        "ADB": "Oracle AutonomousDB 21c",
        "OS": "Object Storage OCI",
        "BDS": "Oracle Big Data Service",
        "OKE": "Oracle Kubernetes Service"
    },
    "Snowflake": {
        "SFAWS": "Snowflake on AWS",
        "SFAZURE": "Snowflake on Azure",
        "SFGCP": "Snowflake on GCP"
    },
    "Databricks": {
        "DBS": "Databricks SaaS",
        "DBW": "Databricks Workspace",
        "DBML": "Databricks Mlflow",
        "DBN": "Databricks Notebooks"
    },
    "Salesforce": {
        "SFS": "Salesforce SaaS",
        "SFSC": "Salesforce Sales Cloud",
        "SFSERV": "Salesforce Service Cloud",
        "SFMC": "Salesforce Marketing Cloud",
        "SFMAP": "Salesforce Mulesoft Anypoint Platform"
    },
    "MongoDB": {
        "MDB": "MongoDB Atlas",
        "MDBA": "MongoDB Atlas AWS",
        "MDBAZ": "MongoDB Atlas Azure",
        "MDBG": "MongoDB Atlas GCP",
        "MDBS": "MongoDB Atlas Search",
        "MDBV": "MongoDB Atlas Vector Search",
        "MDBSP": "MongoDB Atlas Stream Processing",
        "MDBBI": "MongoDB Atlas BI Connector",
        "MDBSQL": "MongoDB Atlas SQL"
    },
    "Cloudflare": {
        "CFA": "AnyCast CloudFlare",
        "CFCDN": "CDN CloudFlare",
        "CFDNS": "Cloudflare DNS",
        "CFDDOS": "Cloudflare DDoS Protection"
    },
    "Akamai": {
        "ACDN": "CDN Akamai",
        "AEC": "Edge Computing Akamai",
        "AS": "Security Akamai"
    },
    "Macrometa": {
        "MCDN": "CDN Macrometa",
        "MEC": "Edge Computing Macrometa"
    }
}

def get_full_service_name(provider: str, service: str) -> str:
    """Convert service abbreviation to full name if available"""
    if provider in service_full_names:
        # First try exact match
        if service in service_full_names[provider]:
            return service_full_names[provider][service]
        
        # Then try to match any part of the service name # source in Uppercase match
        for abbr, full_name in service_full_names[provider].items():
            if abbr in service or service in full_name:
                return full_name
    
    # Return original if no mapping found
    return service

def calculate_duration_in_minutes(duration_str: str) -> int:
    """
    Calculate the duration in minutes from various duration string formats found in merge.txt.
    Returns 0 if duration cannot be parsed or if the calculated duration is negative.
    """
    if not duration_str:
        return 0
        
    duration_str = duration_str.lower().strip()
    total_minutes = 0

    # Replace commas and 'and' with spaces for easier parsing make it singular
    duration_str = duration_str.replace(',', ' ').replace('and', ' ').replace('s', '')
    # Split the duration string into parts
    parts = duration_str.split()
    
    time_dict = {'day': 0, 'hour': 0, 'minute': 0}
    i = 0
    while i < len(parts):
        try:
            value = int(parts[i])
            unit = parts[i + 1]
            if 'day'  in unit:
                time_dict['day'] += value
            elif 'hour' in unit:
                time_dict['hour'] += value
            elif 'minute' in unit:
                time_dict['minute'] += value
            i += 2
        except (IndexError, ValueError):
            i += 1  # Skip if parsing fails

    total_minutes = (
        time_dict['day'] * 1440 +
        time_dict['hour'] * 60 +
        time_dict['minute']
    )
    
    # Ensure the total minutes is not negative
    return max(total_minutes, 0)

def calculate_downtime_minutes(outage: OutageInfo) -> int:
    """
    Calculate downtime in minutes using various fields from the outage info.
    Tries multiple approaches to get the most accurate duration.
    """
        
    # Try to calculate from duration string - more reliable method 1
    if outage.duration:
        minutes = calculate_duration_in_minutes(outage.duration)
        if minutes > 0:
            minutes = minutes
        else:
            minutes = 0
        return minutes
            
    # Try to calculate from downtime_period - more reliable method 2
    elif outage.downtime_period:
        minutes = calculate_duration_in_minutes(outage.downtime_period)
        if minutes > 0:
            minutes = minutes
        else:
            minutes = 0
        return minutes

    # Try to calculate from start_time and end_time if both are available - less reliable method 3
    elif outage.start_time and outage.end_time:
        # Ensure both datetimes are timezone-aware
        start_time = outage.start_time
        end_time = outage.end_time
        
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=pytz.utc)
        else:
            start_time = start_time.astimezone(pytz.utc)
        
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=pytz.utc)
        else:
            end_time = end_time.astimezone(pytz.utc)
        
        delta = end_time - start_time
        return int(delta.total_seconds() / 60)
    else:
        return 0
    return 0

def write_outage_summary(outage: OutageInfo, file):
    """Helper function to write outage summary with enhanced fields"""
    file.write(f"Source Outage Report: {outage.source_outage_report}\n")
    file.write(f"Cloud Provider: {outage.cloud_provider}\n")
    
    # Convert service abbreviations to full names
    full_service_names = [get_full_service_name(outage.cloud_provider, service) 
                         for service in outage.services]
    file.write(f"Cloud Services: {', '.join(full_service_names)}\n")
    
    file.write(f"Regions: {', '.join(outage.regions)}\n")
    file.write(f"Availability Zones: {', '.join(outage.availability_zones)}\n")
    file.write(f"Start Time: {outage.start_time}\n" if outage.start_time else "")
    file.write(f"End Time: {outage.end_time}\n" if outage.end_time else "")
    file.write(f"Outage Status: {outage.status}\n")
    file.write(f"Impact Level: {outage.impact}\n")
    file.write(f"Duration: {outage.duration}\n")
    
    # Calculate and write duration in minutes
    duration_minutes = calculate_duration_in_minutes(outage.duration)
    file.write(f"Duration (minutes): {duration_minutes}\n")
    
    file.write(f"Root Cause: {outage.root_cause}\n")
    file.write(f"Resolution: {outage.resolution}\n")
    file.write(f"Downtime Period: {outage.downtime_period}\n")
    if outage.incident_id:
        file.write(f"Incident ID: {outage.incident_id}\n")
    if outage.affected_components:
        full_component_names = [get_full_service_name(outage.cloud_provider, component) 
                              for component in outage.affected_components]
        file.write(f"Affected Components: {', '.join(full_component_names)}\n")
    if outage.mitigation_steps:
        file.write("Mitigation Steps:\n")
        for step in outage.mitigation_steps:
            file.write(f"- {step}\n")
    if hasattr(outage, 'severity'):
        file.write(f"Severity: {outage.severity}\n")
    if hasattr(outage, 'customer_impact'):
        file.write(f"Customer Impact: {outage.customer_impact}\n")
    file.write("\n---\n\n")

def extract_date_from_text(text: str) -> Optional[datetime]:
    """
    Extract date from the text content of merge.txt.
    Returns None if no valid date pattern is found.
    """
    # Define patterns to search for dates in the text
    date_patterns = [
        r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
        r'(\d{8})',              # YYYYMMDD
        r'(\d{2}\.\w{3}\.\d{4})',  # DD.MMM.YYYY
        r'(\w{3,9} \d{1,2},? \d{4})'  # Month DD, YYYY
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                date_str = match.group(1)
                # Try parsing with dateutil as last resort
                return parser.parse(date_str)
            except:
                continue
                
    return None

def parse_filename_date(filename: str) -> Optional[datetime]:
    """
    Extract date from filename patterns found in merge.txt
    Returns None if no valid date pattern is found
    """
    if not filename:
        return None
        
    # Normalize filename
    filename = filename.strip().replace('\\', '/').replace('./','')
    
    patterns = [
        # Pattern 1: YYYYMMDD-Summary format
        (r'(\d{8})-Summary.*\.txt$', '%Y%m%d'),
        
        # Pattern 2: Incident YYYY-MM-DD format
        (r'Incident (\d{4}-\d{2}-\d{2})\.txt$', '%Y-%m-%d'),
        
        # Pattern 3: YYYY-MM-DD in parentheses
        (r'\((\d{4}-\d{2}-\d{2})\)\.txt$', '%Y-%m-%d'),
        
        # Pattern 4: Service Health - Incident YYYY-MM-DD
        (r'Service Health - Incident (\d{4}-\d{2}-\d{2})\.txt$', '%Y-%m-%d'),
        
        # Pattern 5: DD.MMM.YYYY format
        (r'(\d{2}\.(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.\d{4})\.txt$', '%d.%b.%Y'),
        
        # Pattern 6: YYYYMMDD in middle of filename
        (r'.*?(\d{8}).*?\.txt$', '%Y%m%d'),
        
        # Pattern 7: Month DD, YYYY format
        (r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (\d{1,2}),? \d{4}', '%B %d %Y'),
        
        # Pattern 8: YYYY-MM-DD anywhere in filename
        (r'.*?(\d{4}-\d{2}-\d{2}).*?\.txt$', '%Y-%m-%d'),
    ]
    
    for pattern, date_format in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            try:
                date_str = match.group(1)
                # Handle special case for DD.MMM.YYYY format
                if '.%b.' in date_format:
                    # Convert abbreviated month to full name
                    date_str = date_str.replace('.', ' ')
                    return datetime.strptime(date_str, '%d %b %Y')
                return datetime.strptime(date_str, date_format)
            except ValueError:
                continue
    
    return None

def parse_downtime_period(downtime_str: str) -> Optional[Tuple[datetime, datetime]]:
    """
    Parses the downtime_period string to extract start and end times.
    Returns a tuple of (start_time, end_time) or None if parsing fails.
    """
    time_patterns = [
        # Pattern: From [start_time] to [end_time]
        r"(?i)from\s+(.*?)\s+to\s+(.*?)(?:$|\s*\()",
        # Pattern: The outage started on [start_time] and ended on [end_time]
        r"(?i)The outage started on\s+(.*?)\s*(?:and|&)\s*(?:ended|resolved)\s*(?:on\s*)?(.*?)(?:$|\s*\()",
        # Pattern: Started at [start_time] and ended at [end_time]
        r"(?i)Started at\s+(.*?)\s*(?:and|&)\s*ended at\s+(.*?)(?:$|\s*\()",
        # Pattern: Downtime Period: [start_time] - [end_time]
        r"(?i)Downtime Period:\s*(.*?)\s*-\s*(.*?)(?:$|\s*\()",
    ]

    for pattern in time_patterns:
        match = re.search(pattern, downtime_str)
        if match:
            start_str = match.group(1).strip()
            end_str = match.group(2).strip()
            
            # Parse start time
            start_time = parse_timestamp(start_str)
            
            # Check if end_str is just a time and append date from start_str
            if start_time and re.match(r"^\d{1,2}:\d{2}(?::\d{2})?$", end_str):
                end_str = f"{start_time.strftime('%Y-%m-%d')} {end_str}"
            
            # Parse end time
            end_time = parse_timestamp(end_str)
            
            if start_time and end_time:
                # Ensure both times are timezone-aware and in UTC
                if start_time.tzinfo is None:
                    start_time = start_time.replace(tzinfo=pytz.utc)
                else:
                    start_time = start_time.astimezone(pytz.utc)
                if end_time.tzinfo is None:
                    end_time = end_time.replace(tzinfo=pytz.utc)
                else:
                    end_time = end_time.astimezone(pytz.utc)
                return start_time, end_time
    return None

def format_outage_text(outage: OutageInfo) -> str:
    """
    Format outage information as a multi-line string for genai output
    """
    lines = []
    lines.append(f"Source Outage Report: {outage.source_outage_report}")
    lines.append(f"Cloud Provider: {outage.cloud_provider}")
    
    # Convert service abbreviations to full names
    full_service_names = [get_full_service_name(outage.cloud_provider, service) 
                         for service in outage.services]
    lines.append(f"Cloud Services: {', '.join(full_service_names)}")
    
    lines.append(f"Regions: {', '.join(outage.regions)}")
    lines.append(f"Availability Zones: {', '.join(outage.availability_zones)}")
    
    if outage.start_time:
        lines.append(f"Start Time: {outage.start_time}")
    if outage.end_time:
        lines.append(f"End Time: {outage.end_time}")
        
    lines.append(f"Outage Status: {outage.status}")
    lines.append(f"Impact Level: {outage.impact}")
    lines.append(f"Duration: {outage.duration}")
    
    # Calculate and add duration in minutes
    duration_minutes = calculate_downtime_minutes(outage)
    lines.append(f"Duration (minutes): {duration_minutes}")
    
    lines.append(f"Root Cause: {outage.root_cause}")
    lines.append(f"Resolution: {outage.resolution}")
    lines.append(f"Downtime Period: {outage.downtime_period}")
    
    if outage.incident_id:
        lines.append(f"Incident ID: {outage.incident_id}")
        
    if outage.affected_components:
        full_component_names = [get_full_service_name(outage.cloud_provider, component) 
                              for component in outage.affected_components]
        lines.append(f"Affected Components: {', '.join(full_component_names)}")
        
    if outage.mitigation_steps:
        lines.append("Mitigation Steps:")
        for step in outage.mitigation_steps:
            lines.append(f"- {step}")
            
    return "\n".join(lines)

def write_outage_csv_summary(outages: List[OutageInfo], timestamp: str):
    """Write outage summary as CSV with one line per service per region"""
    csv_file = f'pdf_bot_usebatch/outage_report_summary_{timestamp}.csv'
    
    headers = [
        'outage_timestamp',
        'source_outage_report',
        'cloud_provider',
        'cloud_service',  
        'regions',
        'availability_zones',
        'start_time',
        'end_time',
        'outage_status',
        'impact',
        'duration',
        'duration_minutes',
        'root_cause',
        'resolution',
        'downtime_period',
        'incident_id',
        'affected_components',  # Restored affected_components column
        'mitigation_steps',
        'cloudrisk_genai_output'
    ]

    def clean_text(text):
        """Remove invalid characters from text"""
        if isinstance(text, str):
            return text.replace("\'", ".").replace("\"", ".").replace("'", ".").strip()
        return text

    def clean_list(items):
        """Clean and join list items"""
        if isinstance(items, list):
            return " ".join(clean_text(item) for item in items)
        return ""

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for outage in outages:
            # Get timestamp
            if outage.start_time and isinstance(outage.start_time, datetime):
                record_timestamp = outage.start_time.timestamp()
            else:
                record_timestamp = time()

            # Get date from text or filename
            text_date = extract_date_from_text(outage.source_outage_report)
            if not text_date and outage.source_outage_report:
                text_date = parse_filename_date(outage.source_outage_report)
            default_time = text_date if text_date else datetime(2024, 1, 1, 0, 0)
            
            # Calculate downtime
            downtime_minutes = calculate_downtime_minutes(outage)
            
            # Format genai output
            genai_output = format_outage_text(outage)

            # Get regions
            regions = outage.regions if outage.regions else [""]
            
            # Get provider and validate regions
            provider = outage.cloud_provider or ""
            valid_provider_regions = valid_regions.get(provider, [])

            # Process services
            all_services = set()
            for service in outage.services:
                all_services.add(get_full_service_name(provider, service))
            
            # If no services found, add at least one empty record
            if not all_services:
                all_services.add("")

            # Format affected components separately
            affected_components_str = ", ".join(
                get_full_service_name(provider, component) 
                for component in outage.affected_components
            )

            # Create records for each service and region combination
            for service in all_services:
                service_name = clean_text(service)
                
                # If no regions, create single record
                if not regions or regions == [""]:
                    row = {
                        'outage_timestamp': record_timestamp,
                        'source_outage_report': clean_text(outage.source_outage_report),
                        'cloud_provider': clean_text(provider),
                        'cloud_service': service_name,
                        'regions': "",
                        'availability_zones': clean_list(outage.availability_zones),
                        'start_time': outage.start_time.isoformat() if outage.start_time else default_time.isoformat(),
                        'end_time': outage.end_time.isoformat() if outage.end_time else default_time.isoformat(),
                        'outage_status': clean_text(outage.status),
                        'impact': clean_text(outage.impact),
                        'duration': clean_text(outage.duration),
                        'duration_minutes': downtime_minutes,
                        'root_cause': clean_text(outage.root_cause),
                        'resolution': clean_text(outage.resolution),
                        'downtime_period': clean_text(outage.downtime_period),
                        'incident_id': clean_text(outage.incident_id),
                        'affected_components': clean_text(affected_components_str),  # Added back
                        'mitigation_steps': clean_list(outage.mitigation_steps),
                        'cloudrisk_genai_output': clean_text(genai_output)
                    }
                    writer.writerow(row)
                else:
                    # Create record for each region
                    for region in regions:
                        region_clean = clean_text(region)
                        
                        row = {
                            'outage_timestamp': record_timestamp,
                            'source_outage_report': clean_text(outage.source_outage_report),
                            'cloud_provider': clean_text(provider),
                            'cloud_service': service_name,
                            'regions': region_clean,
                            'availability_zones': clean_list(outage.availability_zones),
                            'start_time': outage.start_time.isoformat() if outage.start_time else default_time.isoformat(),
                            'end_time': outage.end_time.isoformat() if outage.end_time else default_time.isoformat(),
                            'outage_status': clean_text(outage.status),
                            'impact': clean_text(outage.impact),
                            'duration': clean_text(outage.duration),
                            'duration_minutes': downtime_minutes,
                            'root_cause': clean_text(outage.root_cause),
                            'resolution': clean_text(outage.resolution),
                            'downtime_period': clean_text(outage.downtime_period),
                            'incident_id': clean_text(outage.incident_id),
                            'affected_components': clean_text(affected_components_str),  # Added back
                            'mitigation_steps': clean_list(outage.mitigation_steps),
                            'cloudrisk_genai_output': clean_text(genai_output)
                        }
                        writer.writerow(row)

def cleanup_merge_file():
    """Remove lines containing 'is not mentioned in the text' from the merge.txt file."""
    file_path = 'pdf_bot_usebatch/merge.txt'
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Define patterns to exclude
    exclude_patterns = [
        "is not mentioned in the text",
        "the other cloud providers mentioned",
        "The other cloud providers mentioned",
        "identify other cloud providers",
        "No outages were reported",
        "no outages were reported"
    ]
    
    # Filter out lines with the specified expressions
    cleaned_lines = [
        line for line in lines 
        if not any(pattern in line for pattern in exclude_patterns)
    ]

    # Update incorrect patterns: fix common typos and standardize
    cleaned_lines = [
        line.replace("Azur e", "Azure")
            .replace("AzurE", "Azure")
            .replace("Databr icks", "Databricks")
            .replace("Googl e", "Google")
            .replace("AW S", "AWS")
            .replace("+", "")  # Remove plus signs
            .replace("*", "")  # Remove asterisks
            .replace("**", "")  # Remove double asterisks
            .replace("* **", "")  # Remove one plus double asterisks
            .replace("** *", "")  # Remove double plus one asterisks
            .replace("**:", ":")  # Remove double asterisks and colon
            for line in cleaned_lines
    ]
    
    with open(file_path, 'w') as file:
        file.writelines(cleaned_lines)


def run_merge_script():
    """Run the merge_text_files script and process the merged output"""
    os.system(' cd pdf_bot_usebatch ; sh merge_text_files ; cd .. ')

    # Call the cleanup function before processing the merged output
    # Removes "is not mentioned in the text"
    cleanup_merge_file()
    
    try:
        with open('pdf_bot_usebatch/merge.txt', 'r') as f:
            content = f.read()
            
        outages = extract_outage_info(content)
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Write text summary
        summary_file = f'pdf_bot_usebatch/outage_report_summary_{timestamp}.txt'
        with open(summary_file, 'w') as f:
            for outage in outages:
                write_outage_summary(outage, f)
        
        # Write CSV summary
        write_outage_csv_summary(outages, timestamp)
                
    except Exception as e:
        print(f"Error processing merged file: {str(e)}")

if __name__ == "__main__":
    run_merge_script()