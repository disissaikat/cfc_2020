import ibm_db
from ibm_botocore.client import Config
import ibm_boto3

# for connecting to IBM DB2
dsn_driver = "IBM DB2 ODBC DRIVER"
dsn_database = "BLUDB"           
dsn_hostname = "dashdb-txn-sbox-yp-lon02-07.services.eu-gb.bluemix.net"
dsn_port = "50000"             
dsn_protocol = "TCPIP" 
dsn_uid = "lps30376" 
dsn_pwd = "9m88-tjmx1p3c1zz" 

dsn = (
    "DRIVER={{IBM DB2 ODBC DRIVER}};"
    "DATABASE={0};"
    "HOSTNAME={1};"
    "PORT={2};"
    "PROTOCOL=TCPIP;"
    "UID={3};"
    "PWD={4};").format(dsn_database, dsn_hostname, dsn_port, dsn_uid, dsn_pwd)

conn = ibm_db.connect(dsn, "", "")

# for connecting to IBM Cloud Object Storage 
credentials = {
  "apikey": "GjxCkQq7wWTASP3KXJ9DlxTzULlfI5CqpOt_IWrjD3yW",
  "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
  "iam_apikey_description": "Auto-generated for key 76d16767-f5ab-43dd-8585-ca9d334ecbc8",
  "iam_apikey_name": "Service credentials-1",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/790e1b084ba44e0b875733b8dec8461b::serviceid:ServiceId-16750b18-f7cc-4fec-96c1-4a4828a9efb4",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/790e1b084ba44e0b875733b8dec8461b:5a72aa32-71bf-4b8b-8ab7-597ecd9a1597::"
}

auth_endpoint = 'https://iam.bluemix.net/identity/token'
service_endpoint = 'https://s3.jp-tok.cloud-object-storage.appdomain.cloud'
cos = ibm_boto3.client('s3',
ibm_api_key_id=credentials['apikey'],
ibm_service_instance_id=credentials['resource_instance_id'],
ibm_auth_endpoint=auth_endpoint,
config=Config(signature_version='oauth'),
endpoint_url=service_endpoint)

def upload_contact_image(filename, key):
    bucket = "aaksathe-app"
    cos.upload_file(Filename=filename,Bucket=bucket,Key=key)

def download_contact_image(filename):
    bucket = "aaksathe-app"
    try :
        cos.download_file(Bucket=bucket,Key=filename,Filename='resources/contact/'+filename)
        file_found = True
    except :
        file_found = False
    finally :
        return file_found

def upload_org_logo(filename, key):
    bucket = "aaksathe-app"
    cos.upload_file(Filename=filename,Bucket=bucket,Key=key)