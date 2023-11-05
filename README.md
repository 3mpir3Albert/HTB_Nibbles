# HTB_Nibbles
In this repository you will find the technical report of Nibbles, the exploit (pwned.py) to abuse the CVE-2015-6967 and an autopwn tool (autopwn.py) in case you want to resolve the machine in HackTheBox.
- Pwned.py tool: This file will help you to exploit CVE-2015-6967. If you want to run this exploit you will need to satisfy 3 requirements:
  - You will need to create a PHP file with a command to execute in the Nibbleblog server. For example:
      <?php
        system("whoami");
      ?>
  - In case you want to execute a reverse shell you will need to be listening in the same port as you specified in the PHP file.
  - Run the tool correctly: python3 pwned.py <base_url_nibbleblog> <nibbleblog_admin_user> <nibbleblog_admin_password>
