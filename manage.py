#!/usr/bin/env python3
import argparse
from params import(REGION,AWS_ACCES_KEY,AWS_SECRET_KEY,SSH_KEY,SSH_FILE_LINUX)
import boto3
import datetime
import paramiko
import subprocess
from tools import generer_chaine,get_ipv4_pub,get_distib,generate_ssh_key_pair

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
     fichier = open(f".\\Cle_public\\{name}_{user}.pem", "a")
     fichier.write(f"{private_key}")
     fichier.close()

     destFile = r"temp.txt"
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
     username =""
     if os_instance.count('Debian') == 1:
           username="admin"
     elif os_instance.count('Ubuntu') == 1:
           username="ubuntu"
     elif os_instance.count('Bitnami') == 1:
           username="bitnami"
     elif os_instance.count('Oracle') == 1:
           username="ec2-user"
     elif os_instance.count('SUSE') == 1:
           username="root"
     elif os_instance.count('RHEL') == 1:
           username="root"
     elif os_instance.count('Fedora') == 1:
           username="fedora"
     elif os_instance.count('Amazon Linux') == 1:
         username="ec2-user"
     elif os_instance.count('CentOS') == 1:
           username="centos"
     else:
           username=username  
           
     print(os_instance)


     client = paramiko.client.SSHClient()
     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
     client.connect(ip_pub_instance, username=username,  key_filename=SSH_KEY)
     _stdin, _stdout,_stderr = client.exec_command(f"echo '{ssh_key} {username}' >> {SSH_FILE_LINUX}")
     print(_stdout.read().decode())
     client.close()

#generate()
distribute("i-0e03163c8edc7683a","ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCwLgVaInMnFkW8Fsn6WTVM5PUSFOH0VHWI7mGy6iHSPnO7RM1f6IQLGJ6ZSYKf3pcQw1qYI1sCkeCAOxA2HhkWF2U0WMqdqaYITGPk5+3ktRkAr5SERFnOGbUrAueEow7OJMYVuWp9YvhYIlu2FmF/Ksbz4hPFlFdg1JyT5e+Tt/qnasp2n0ORgt9zbt1zhIVa5jqxGnyQyMdjpDVM7hT2kB4QU2g8yV8GezuJQHH8huuZz4CBskzieJrGrbjxzoWZgA7TzTrGzRzgpk4fqej/oVh/dNYG0fJLKhxI5e2Rl1U5ZTFBdrYOT8fJs/YAypAkV4laKqwSFc20vHKrGzP7, 65537, 9829816071124974922970316432555091484077140093560861638373671074188246517260442258681379940894877829548240685809270097482550708218868250557820443317748874013719100162161843847531744402637120775270375978345878575684247322620048228031938392799209338328842099007698734332481602647652544432594526445478213145838828405372525003693648365464832937577046909934879378844550910627190778479647137314600245701562038175455092393612939619063099429181162296254274125181300830154492574136009255394879892381366515430061408983901508943581142057330585863136908917368044078486168666545380787231225625346456908237908194124937678508888673, 2613343245967630113027742672330430476720409003514689087877705314603313269380274129461931273024275507883259891576489083321248244288186933443385861527743377109314078406859971039029473586967108601770031902789597592744727529784014938986555753777025385802670074765649829843791076275425365192376139870624314466183924477127871565963921, 7053032543131229708868643627188738071333575718004536705392338597656315947281277537886558693606236816256273807627998405277572549727397817147241756882391200622539930681430019554246265880354495156438988531667211041287399711279307463111486718191677272530706120849789841682199779115712402674971")


# def revoke_key(id_key):
#     pass

# def list_keys():
#     pass

#####Creer un parser pour chaque commande
def arguments():
     ###PARSER
     parser_generate = argparse.ArgumentParser(description='Création clé SSH')
     parser_distribute = argparse.ArgumentParser(description="Distribute keys")



     parser_generate.add_argument('--generate', '-g', default=None,required=False,action='store_true', help='Genere une paire de cle ssh')
     parser_distribute.add_argument('--name', '-n', type=str, required=False, help='Distribue la cle ssh')
     #parser.add_argument('--revoke', '-r', type=str, required=False, help='Revoke une paire de cle ssh')
     #parser.add_argument('--list', '-l', type=str, required=False, help='affiche les paires de cle ssh')
    ###ARGUMENT
     args_generate = parser_generate.parse_args()
     args_distribute=parser_distribute.parse_args()



#      if args_generate.generate != None:
#         generate()
#       elif args_distribute.name != None or args_distribute.  :
#     #     distribute(args.key_id, args.instance_id)
#     #  elif args.revoke == "revoke":
#     #    revoke_key(args.key_id, args.instance_id)
#     #  elif args.command == "list":
#     #     list_keys()
#     #  elif args.command == "audit":
#     #     # Implement the audit functionality
#     #     pass
#      else:
#         parser.print_help()




arguments()