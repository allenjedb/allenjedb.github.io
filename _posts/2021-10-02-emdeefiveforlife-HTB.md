<code>#!/bin/bash

<code>md5=$(curl -s --cookie "PHPSESSID=f8oau3r713ir774pq8cclaiqn6" 'http://188.166.173.208:31644/' | grep -Po '[\w]{20}')</code>
<code>echo $md5</code>
<code>target=$(echo -n $md5 | md5sum | sed 's/ .*$//')</code>
<code>echo $target</code>
<code>html=$(curl -s  --cookie "PHPSESSID=f8oau3r713ir774pq8cclaiqn6" -d "hash=$target" 'http://188.166.173.208:31644/')</code>
<code>echo $html</code>