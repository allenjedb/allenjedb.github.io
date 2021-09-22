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
<h4>HTTP</h4>
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
<h4>HTTPS</h4>

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
<ul>
  <li>Proxychains</li>
  <li>Foxyproxy</li>
</ul>