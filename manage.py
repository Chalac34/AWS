#!/usr/bin/env python3
import argparse
from params import(REGION,AWS_ACCES_KEY,AWS_SECRET_KEY,SSH_KEY,SSH_FILE_LINUX)
import boto3
import datetime
import paramiko
import subprocess
from tools import (generer_chaine,
                   get_ipv4_pub,get_distib,
                   generate_ssh_key_pair,
                   search_username,
                   delete_key_on_AWS)


def generate():
     client = boto3.client(
               'ssm',
               aws_access_key_id=AWS_ACCES_KEY,
               aws_secret_access_key=AWS_SECRET_KEY,
               region_name=REGION
               )

     (public_key, private_key) = generate_ssh_key_pair()
     name_instance=input("Nom de la clé : ")
     description=input("Description de la clé : ")
     user=input("User: ")
          # Afficher les clés
     json={
               'name_of_key':name_instance,
               'time':datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
               'user':user,
               'cle_public':public_key,
          }
     ###POUR DEBUG VOIR CLE PRIVÉE ET PUBLIC###
     fichier = open(f".\\Cle_privé\\{name_instance}_{user}.pem", "a")
     fichier.write(f"{private_key}")
     fichier.close()
     fichier = open(f".\\Cle_public\\{name_instance}_{user}.pub", "a")
     fichier.write(f"{public_key}")
     fichier.close()
     destFile = r"temp.txt"


     ###LOG###
     with open(destFile, "a") as f:
               f.write(f"{json}\r\n")


     response = client.put_parameter(
          Name=f"{user}_{name_instance}",
          Description=description,
          # Value=str(private_key)[11:],
          Value=str(private_key),
          Type='SecureString',
          KeyId='0d2c729e-3320-48d8-8417-29a238edaba7',
          Overwrite=True,
          AllowedPattern='',
     )
     print(f'Clé publique : {public_key}')
     return 0
##############################

def distribute(instance_id,ssh_key,username=""):
     
     ip_pub_instance=get_ipv4_pub(instance_id)
     os_instance=get_distib(instance_id)
     username =search_username(os_instance)
     
     client = paramiko.client.SSHClient()
     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
     client.connect(ip_pub_instance, username=username,  key_filename=SSH_KEY)
     ssh_key_without_rsa=ssh_key.replace("ssh-rsa","")
     _stdin, _stdout,_stderr = client.exec_command(f'grep -n {SSH_FILE_LINUX} -e {ssh_key_without_rsa}')
     
     if (_stdout.read().decode()) == "" :
          _stdin, _stdout,_stderr = client.exec_command(f"echo '{ssh_key} {username}' >> {SSH_FILE_LINUX}") 
          client.close()
          print("clé ssh attribué")
          return 0
     else:
           client.close()
           print("clé déja attribué a cette machine")
           return 0


###gerer si clé en plusieur exemplaire
def revoke_key(instance_id,ssh_key,username=""):
      ip_pub_instance=get_ipv4_pub(instance_id)
      os_instance=get_distib(instance_id)
      username =search_username(os_instance)
      user=input("Utilisateur de la clé: ")
      ssh_key=ssh_key.replace("ssh-rsa","")

      client = paramiko.client.SSHClient()
      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      client.connect(ip_pub_instance, username=username,  key_filename=SSH_KEY)
      _stdin, _stdout,_stderr = client.exec_command(f'grep -n {SSH_FILE_LINUX} -e {ssh_key}')
      #Verifie qu'il est eu un resultat
      if (_stdout.read().decode()) == "":
            client.close()
            print('Aucune clé ssh trouvé dans le fichier')
            return 0
      #Suprrime tous les lignes du fichier avec cette clé
      val =(_stdout.read().decode()).split("\n")
      d=0
      #modifie la ligne de -1 a chaque passage vue que sed retire le \n
      for i in val:
            if i[:1] == "":
                  continue
            ligne=int(i[:1])+d
            _stdin, _stdout,_stderr = client.exec_command(f'sed -i {ligne}d {SSH_FILE_LINUX}')
            d-=1
      print("clé sur l'instance supprimée")
      delete_key_on_AWS(f"{user}_{instance_id}")
      print("clé sur le parameter_store supprimée")
            


def list_keys(instance_id,username=""):
      ip_pub_instance=get_ipv4_pub(instance_id)
      os_instance=get_distib(instance_id)
      username =search_username(os_instance)
      client = paramiko.client.SSHClient()
      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      client.connect(ip_pub_instance, username=username,  key_filename=SSH_KEY)
      _stdin, _stdout,_stderr = client.exec_command(f'cat {SSH_FILE_LINUX} ')
      val =(_stdout.read().decode()).split("\n")
      for i in val:
            print(i)
            print("\n")
      return 0



#####Creer un parser pour chaque commande
def arguments():
     ###PARSER
      parser = argparse.ArgumentParser(description='Création clé SSH')


      parser.add_argument('--generate', '-g', default=None,required=False,action='store_true', help='use python manage.py -g or --generate')
      parser.add_argument('--distribute', '-d', required=False,action='store_true', help='use python manage.py -d -i [INSTANCE_ID] -k [SSH_KEY]')
      parser.add_argument('--revoke', '-r', required=False,action='store_true', help='use python manage.py -r -i [INSTANCE_ID] -k [SSH_KEY]')
      parser.add_argument('--list', '-l',action='store_true', required=False, help='use python manage.py -r -i [INSTANCE_ID]')
      parser.add_argument('--instance', '-i',type=str, required=False,help=' ' )
      parser.add_argument('--key','-k',type=str, required=False,help =' ')
      args = parser.parse_args()

      


      if args.generate == True:
            generate()
      elif args.revoke == True and args.key != None and args.name != None:
            revoke_key(args.instance,args.key )
      elif args.distribute == True and args.name != None and args.key != None  :
            distribute(args.instance,args.key)

      elif args.list == True and args.instance != None:
            list_keys(args.instance)
      # elif args.command == "audit":
      #       # Implement the audit functionality
      #       pass
      else:
            parser.print_help()
       




arguments()

