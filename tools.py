import random
import string
import boto3
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from params import AWS_ACCES_KEY,AWS_SECRET_KEY,REGION

def generer_chaine():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(50))
###Donne ipv4 pub
def get_ipv4_pub(instance_id):
     client_EC2=boto3.client(
               'ec2',
               aws_access_key_id=AWS_ACCES_KEY,
               aws_secret_access_key=AWS_SECRET_KEY,
               region_name=REGION
               )
     
     response = client_EC2.describe_instances(
           InstanceIds=[
        instance_id,
    ],

  )
     return response["Reservations"][0]["Instances"][0]["PublicIpAddress"]


####Trouve la distribution utilisé
def get_distib(instance_id):
    client_EC2=boto3.client(
               'ec2',
               aws_access_key_id=AWS_ACCES_KEY,
               aws_secret_access_key=AWS_SECRET_KEY,
               region_name=REGION
               )
     
    response = client_EC2.describe_instances(
           InstanceIds=[
        instance_id,
    ],
    )
    ami_id = response["Reservations"][0]["Instances"][0]['ImageId']

    response2=client_EC2.describe_images(ImageIds=[
        ami_id,
    ],)
    return response2["Images"][0]['Description']
  


def generate_ssh_key_pair(key_size=2048, passphrase=None):

    # Génération de la clé privée
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    
    # Sérialisation de la clé privée
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(passphrase.encode()) if passphrase else serialization.NoEncryption()
    )
    
    # Sérialisation de la clé publique
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )
    
    
    #print(private_key_pem)
    return public_key_pem.decode("utf-8"), private_key_pem.decode("utf-8")

generate_ssh_key_pair()