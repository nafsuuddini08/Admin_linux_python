#!/usr/bin/python

import os
import time, subprocess
from tkinter import W
from termcolor import colored
from yaml import compose_all 

#check if it's install it the ssh service
def installation_status():
    os.system("apt list | grep openssh-server")

#install ssh if you don't have install it 
def install_ssh():
    os.system("sudo apt -y install openssh-server")

#check ssh service status
def service_status():
    stat = subprocess.call(["systemctl", "is-active", "--quiet", "ssh"])
    if(stat == 0):# if 0 (active), print "Active"
        print("ssh -> is running")
    else:
        print("ssh -> is NOT running")
        statuscommand = input("Dou you want to check more datail why it not running?[y/n]: ")
        if(statuscommand == "y"):
            print(colored("Press Q to exit", 'red'))
            os.system("service ssh status")
    
#stop, restart, status, start openssh server
def change_service_status():

    estat = input("\nstart / stop / restart :")
    
    if estat == "start":
        
        print("Starting the dhcp service...\n")
    
        os.system("sudo service ssh start")
        
        time.sleep(2)

        print("ssh service start successfully\n")
                
    elif estat == "stop":
                        
        print("Stopping the service...\n")

        os.system("sudo service ssh stop")
    
        time.sleep(2)

        print("ssh service successfully stopped\n")

    elif estat == "restart":
        
        print("Restarting the service..\n")

        os.system("sudo service ssh restart")
    
        time.sleep(2)

        print("ssh service restarted successfully\n")
    
    else:
        print ("")
        input("Please select the correct option...\npress any key to continue")

#Date that the ssh private key and public key was created, modifiend, etc.
def date_generate_keys():
    print("\nPrivate key generation date: \n")
    os.system("stat /etc/ssh/ssh_host_rsa_key")
    time.sleep(2)
    print("\nPublic key generation date: \n")
    os.system("stat /etc/ssh/ssh_host_rsa_key.pub")


#Show the actual welcome message ssh connetion.

def print_ssh_welcomemsg():
    print("\nIf you don't have any message set it will don't print anything.\n") 
    time.sleep(3)
    print("Actual ssh welcome message: \n") 
    os.system("cat /etc/motd 2> /dev/null")

#change or set ssh welcome message

def change_ssh_welcomemsg():
    os.system("touch /etc/motd") # create motd file in the case that your system dont have this file created.
    time.sleep(2)
    with open('/etc/motd','w') as f:
        f.write(input("Write the new welcome message: "))
    print("\nThe Actual message: \n")
    os.system("cat /etc/motd")
    print("Mofiying config files...")
    '''with open("/etc/ssh/sshd.conf","r") as f:
        text = f.read().replace("#PrintLastLog yes", "PrintLastLog no")
    with open("/etc/ssh/sshd.conf", "w") as w:
        w.write()'''

#Show the dafault ssh port.
def default_port():
    os.system("cat /etc/ssh/sshd_config | grep 'Port' | grep -vE 'GatewayPorts no' | sed 's/[#]//g'")
    #os.system("cat /etc/services | grep 'ssh' | sed -e 's/\<SSH Remote Login Protocol\>//g' | sed 's/[#]//g'") -> i recommend to use this command

#Failed attempts to enter the password 
def print_failed_attempts():
    os.system("cat /etc/ssh/sshd_config | grep 'MaxAuthTries' | sed 's/[#]//g'")

#The known_hosts file lets the client authenticate the server, to check that it isn't connecting to an impersonator. This is for avoid man-in-the-middle attacks. 
#The authorized_keys file lets the server authenticate the user.

#regenerate keys for the server
def regenerate_keys():
    print("\nRegenerating keys for the server... \n")
    os.system("/bin/rm -v /etc/ssh/ssh_host_*")
    time.sleep(2)
    os.system("sudo dpkg-reconfigure openssh-server 1>/dev/null")
    time.sleep(2)
    print("restarting the service...")
    os.system("sudo service ssh restart")
    print("Remember that if you want to connect to the server on your client machine you need to update the file .ssh/know_hosts")
    time.sleep(3)

'''#update the file know_hots
def update_kown_hots():
    hostname = input("Put the hostname or the IP address: ")
    print("removing the old key from known_hosts...")
    os.system("ssh-keygen -R $"+hostname+"")
    print()'''

#Change the default ssh port.

'''def canviar_port():
    with open('/etc/ssh/sshd_config', 'r') as f:
        data = f.readlines()
    nou_port = input("Escull un port (Has d'escriure el següent: \nPort: 20 (o el numero que vulguis): ")
    data[14] = nou_port + "\n"
    with open('/etc/ssh/sshd_config', 'w') as f:
        f.writelines(data)
        f.close()'''
        
#Change the number of failed attempts allowed on ssh connection

def change_password_attempts():
    print("Your actual failed attempts:\n")
    command = os.system("cat /etc/ssh/sshd_config | grep 'MaxAuthTries' | sed 's/[#]//g'")
    userattempts = input("\nSet a num value to set failed attempts to login: ")
    #un-comment the line that contain "MaxAuthTries"
    time.sleep(2)
    os.system("sed -i '/MaxAuthTries/s/^#//g' /etc/ssh/sshd_config")
    with open("/etc/ssh/sshd.conf", "r") as f:
        text = f.read().replace(command, "{0}".format(userattempts)) 
    with open("/etc/ssh/sshd.conf", "w") as w:    
        w.write(text)

#PERMETRE QUE UN USUSARI ACCEDEIXI AL SERVIDOR SSH SENSE CONTRASENYA.

def accedir_sense_contrasenya():

    print("Per accedir al servidor es necessita una clau publica\n")
    print("Sino la tens aquest programa la genera auotmàticament\n")
    print("Si ja tens una clau publica simplement selecciona la opció n per no sobresciure la clau\n")

    #Generem un parell de claus noves
    os.system("ssh-keygen -t rsa")
    
    #Amb els seguents inputs guardem la informació del ususari
    #i la utlitzem posteriorment per accedir al servidor ssh
    usuari = input("\nNom d'usuari al qual es vol accedir sense contrasenya: ")
    
    lloc = input("\nIp o host del servidor ssh: ")

    print("\n")

    print("Creant directori...\n")
    #Creem un directori .ssh al directori del usuari
    os.system("ssh " + usuari + "@" + lloc + " mkdir -p .ssh")

    print("Copiant clau publica al servidor...\n")
    #Finalment copiem el contingut de la clau pública del pc client al fitxer
    #.ssh/authorized_keys del usuari del servidor.
    os.system("cat .ssh/id_rsa.pub | ssh " + usuari + "@" + lloc + " 'cat >> .ssh/authorized_keys'")

    print("Fet, ja pots accedir sense contrasenya al usuari " + usuari + " del servidor ssh\n")

#MENU

def menu_ssh(): 
    while True:
        time.sleep(2)
        os.system("clear")
        print ("Manage SSH\n")
        print ("\t1.- SSH installation status")
        print ("\t2.- Install SSH ")
        print ("\t3.- SSH Service status ")
        print ("\t4.- Start/Stop/Restart SSH ")
        print ("\t5.- Date generation keys ")
        print ("\t6.- Show the actual ssh welcome message ")
        print ("\t7.- Change the ssh welcome message ")
        print ("\t8.- Show ssh default port ")
        print ("\t9.- Show Failed attempts to login with ssh ")
        print ("\t10.- - ")
        print ("\t11.- Change default ssh port ")
        print ("\t12.- Change the number of failed attempts allowed on ssh connection ")
        print ("\t13.- Access to the server without password ")
        print ("\t14.- Exit")
    
        optionMenu = input("\nSelect any option: ")
    
        if optionMenu == "1":
            installation_status()

        elif optionMenu == "2":
            install_ssh()

        elif optionMenu == "3":
            service_status()

        elif optionMenu == "4":
            change_service_status()

        elif optionMenu == "5":
            date_generate_keys()
        
        elif optionMenu == "6":
            print_ssh_welcomemsg()
            
        elif optionMenu == "7":
            change_ssh_welcomemsg()
            
        elif optionMenu == "8":
            default_port()
           
        elif optionMenu == "9":
            print_failed_attempts()
            
        #elif optionMenu == "10":
            #canviar_missatge()

        elif optionMenu == "11":
            canviar_port()
           
        elif optionMenu == "12":
            change_password_attempts()
            
        elif optionMenu == "13":
            accedir_sense_contrasenya()
        
        elif optionMenu == "14":
            print("\nBye :)")
            break
        
        else:
            print ("")
            input("Please select the correct option......\npress any key to continue")
