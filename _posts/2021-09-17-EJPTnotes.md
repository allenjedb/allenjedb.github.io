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
<h3>HTTPS</h3>

<ul>
<li>nc doesnt do https - use openssl instead </li>
<li></li>

</ul>

<h2 id="pivoting">Pivoting</h2>
<h3>Bash Simple Ping sweep</h3>
<code>for i in {1..255}; do (ping -c 1 192.168.1.${i} | grep "bytes from" &); done</code>
<h3>Bash Simple portscan</h3>
<code>for i in {1..65535}; do (echo > /dev/tcp/192.168.1.1/$i) >/dev/null 2>&1 && echo $i is open; done</code>
<h3>Proxy tools</h3>
<h4>Proxychains</h4>
<p>example to proxy a netcat</p>
<code>proxychains nc 172.16.0.10 23</code>
<p>notes:</p>
  <ul>
    <li>when using nmap w/ proxychains comment out proxy_dns inside the proxychains.conf file</li>
    <li>only tcp scan will work</li>
    <li>udp, syn and ping scan wont work - use -Pn</li>
  </ul>
<h4>Foxyproxy</h4>
<p>proxy for routing browser traffic</p>
<h3>SSH Tunneling / Port Forwarding</h3>
<h4>Port Forwarding - Local: From attacker to victim via SSH</h4>
<p>Attacker --ssh--> 172.16.0.5 --http--> 172.16.0.5</p>
<code>ssh -L 8000:172.16.0.10:80 user@172.16.0.5 -fN</code>
<ul>
  <li>-f = backgrounds shell immediately</li>
  <li>-N tells SSH that it doesn;t need to execute any commands - and just set up the connection</li>
</ul>
<p>Now we can access the webserver on 172.16.0.10 using our own box localhost:8000</p>
<h4>Proxies</h4>
<code>ssh -D 1337 user@172.16.0.5 -fN</code>
<p>Will open port 1337 on attacker's machine as a proxy to send data through the 172.16.0.5 network - useful when combined with proxy chains -  just make sure proxy chains conf is configured correctly</p>