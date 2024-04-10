#!/usr/bin/env python3
import argparse
from params import(REGION,AWS_ACCES_KEY,AWS_SECRET_KEY,SSH_KEY,SSH_FILE_LINUX)
import boto3
import datetime
import paramiko
import subprocess
from tools import generer_chaine,get_ipv4_pub,get_distib,generate_ssh_key_pair,search_username

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

     (public_key, private_key) = generate_ssh_key_pair()
     name=input("Nom de la clé : ")
     description=input("Description de la clé : ")
     user=input("User: ")
          # Afficher les clés
     if name == "":
          name=generer_chaine()
     json={
               'name_of_key':name,
               'time':datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
               'user':user,
               'cle_public':public_key,
          }
     ###POUR DEBUG VOIR CLE PRIVÉE ET PUBLIC###
     fichier = open(f".\\Cle_privé\\{name}_{user}.pem", "a")
     fichier.write(f"{private_key}")
     fichier.close()
     fichier = open(f".\\Cle_public\\{name}_{user}.pub", "a")
     fichier.write(f"{public_key}")
     fichier.close()
     destFile = r"temp.txt"


     ###LOG###
     with open(destFile, "a") as f:
               f.write(f"{json}\r\n")


     response = client.put_parameter(
          Name=name,
          Description=description,
          # Value=str(private_key)[11:],
          Value=str(private_key),
          Type='SecureString',
          KeyId='0d2c729e-3320-48d8-8417-29a238edaba7',
          Overwrite=True,
          AllowedPattern='',
     )
     print(f'Clé publique : {public_key}')
##############################

def distribute(instance_id,ssh_key,username=""):
     
     ip_pub_instance=get_ipv4_pub(instance_id)
     os_instance=get_distib(instance_id)
     username =search_username(os_instance)


     client = paramiko.client.SSHClient()
     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
     client.connect(ip_pub_instance, username=username,  key_filename=SSH_KEY)
     _stdin, _stdout,_stderr = client.exec_command(f"echo '{ssh_key} {username}' >> {SSH_FILE_LINUX}")
     #print(_stdout.read().decode())
     client.close()
     print("clé ssh attribué")


###PAS FINI
def revoke_key(instance_id,ssh_key,username=""):
      ip_pub_instance=get_ipv4_pub(instance_id)
      os_instance=get_distib(instance_id)
      username =search_username(os_instance)

      client = paramiko.client.SSHClient()
      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      client.connect(ip_pub_instance, username=username,  key_filename=SSH_KEY)
      #_stdin, _stdout,_stderr = client.exec_command(f'grep -n {SSH_FILE_LINUX} -e {ssh_key} | grep -o "^." | sed -i $(</dev/stdin)d {SSH_FILE_LINUX}')
      _stdin, _stdout,_stderr = client.exec_command(f'grep -n test.txt -e {ssh_key}')
      #_stdin, _stdout,_stderr = client.exec_command(f'ls -asl ')
      #_stdin, _stdout,_stderr = client.exec_command(f'grep -n tryme.txt -e {ssh_key} | grep -n -o ".................$" ')
      print(_stdout.read().decode())
      #sortie=_stdout.read().decode()
     #  sortie=sortie.split('.ssh/authorized_keys:')#[4]== ssh_key 
     #  for i in sortie:
     #        print(i)
     #  # print(_stdout.err().decode())

#####Creer un parser pour chaque commande
def arguments():
     ###PARSER
      parser = argparse.ArgumentParser(description='Création clé SSH')


      parser.add_argument('--generate', '-g', default=None,required=False,action='store_true', help='Genere une paire de cle ssh')
      parser.add_argument('--name', '-n',type=str, required=False, help='Distribue la cle ssh')
      parser.add_argument('--key','-k',type=str, required=False, help='cle ssh')
      parser.add_argument('--distribute', '-d', required=False,action='store_true', help='Revoke une paire de cle ssh')
      parser.add_argument('--revoke', '-r', required=False,action='store_true', help='Revoke une paire de cle ssh')
     #parser.add_argument('--list', '-l', type=str, required=False, help='affiche les paires de cle ssh')
    ###ARGUMENT
      args = parser.parse_args()

      


      if args.generate == True:
            generate()
      elif args.revoke == True and args.key != None and args.name != None:
            revoke_key(args.name,args.key )
      elif args.distribute == True and args.name != None and args.key != None  :
            distribute(args.name,args.key)

      # elif args.command == "list":
      #       list_keys()
      # elif args.command == "audit":
      #       # Implement the audit functionality
      #       pass
      else:
            parser.print_help()
       




arguments()

