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

