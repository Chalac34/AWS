#!/usr/bin/env python3
import argparse
import boto3
from params import(REGION,AWS_ACCES_KEY,AWS_SECRET_KEY,SSH_KEY,SSH_FILE_LINUX)
import boto3
import rsa
import time
import paramiko
import subprocess
from tools import generer_chaine

hostname="13.37.213.89"
username="admin"

##TODDO
#Mettre des tag au clé pour pouvoir les retrouver dans le parameter Store , faire une fonction qui retrouve les clé dans le parameter store pour finir le distribute
#METTRE LES ARGUMENT PAR RAPPORT AU BESOINS DANS LES FOCNTION
##
# subprocess.Popen(
#     "ssh {user}@{host} -i {pkey}  ".format(user=username, host=hostname, pkey=SSH_FILE_LINUX, cmd="echo 'bonjour' >> taoi.txt "),
#     shell=True,
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
# ).communicate()




def generate():
     client = boto3.client(
               'ssm',
               aws_access_key_id=AWS_ACCES_KEY,
               aws_secret_access_key=AWS_SECRET_KEY,
               region_name=REGION
               )

     (public_key, private_key) = rsa.newkeys(2048)
     name=input("Nom de la clé : ")
     description=input("Description de la clé : ")
          # Afficher les clés
     if name == "":
          name=generer_chaine()
     json={
               'name_of_key':name,
               'time':time.time(),
               'user':'t()',
               'cle_public':str(public_key)[10:],
          }

     destFile = r"temp.txt"
     with open(destFile, "a") as f:
               f.write(f"{json}\r\n")


     response = client.put_parameter(
          Name=name,
          Description=description,
          Value=str(private_key)[11:],
          Type='SecureString',
          KeyId='0d2c729e-3320-48d8-8417-29a238edaba7',
          Overwrite=True,
          AllowedPattern='',
     )
     print(f'Clé publique : {public_key}')

# def distribute(ssh_key,id_instance,user_instance):
#     client = boto3.client(
#                'ec2',
#                aws_access_key_id=AWS_ACCES_KEY,
#                aws_secret_access_key=AWS_SECRET_KEY,
#                region_name=REGION
#                )
#     response = client.send_ssh_public_key(
#     InstanceId=f'{id_instance}',
#     InstanceOSUser=f'{user_instance}',
#     SSHPublicKey=f'{ssh_key}',
#     AvailabilityZone=f'{REGION}'
# )  
# def distribute(ssh_key,id_instance,user_instance):
#     client = paramiko.client.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     client.connect(hostname, username=username,  key_filename=SSH_KEY)
#     _stdin, _stdout,_stderr = client.exec_command(f"echo '{ssh_key}' >> {SSH_FILE_LINUX} ")
#     print(_stdout.read().decode())
#     client.close()
# def revoke_key(id_key):
#     pass

# def list_keys():
#     pass

#####Creer un parser pour chaque commande
def arguments():
     parser = argparse.ArgumentParser(description='Mangement clé SSH')
     parser.add_argument('--generate', '-g', default=None,required=False,action='store_true', help='Genere une paire de cle ssh')
     #parser.add_argument('--name', '-n', type=str, required=False, help='Genere une paire de cle ssh')
     parser.add_argument('--revoke', '-r', type=str, required=False, help='Revoke une paire de cle ssh')
     parser.add_argument('--list', '-l', type=str, required=False, help='affiche les paires de cle ssh')
     args = parser.parse_args()
     print(args.generate)   
     if args.generate != None:
        generate()
    #  elif args.distribute != None:
    #     distribute(args.key_id, args.instance_id)
    #  elif args.revoke == "revoke":
    #    revoke_key(args.key_id, args.instance_id)
    #  elif args.command == "list":
    #     list_keys()
    #  elif args.command == "audit":
    #     # Implement the audit functionality
    #     pass
     else:
        parser.print_help()




arguments()