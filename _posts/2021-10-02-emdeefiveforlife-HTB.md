<code>#!/bin/bash

<code>getw=$(curl -s --cookie "PHPSESSID=f8oau3r713ir774pq8cclaiqn6" 'http://188.166.173.208:31644/' | grep -Po '[\w]{20}')</code>
<code>echo $getw</code>
<code>md5=$(echo -n $getw | md5sum | sed 's/ .*$//')</code>
<code>echo $md5</code>
<code>getr=$(curl -s  --cookie "PHPSESSID=f8oau3r713ir774pq8cclaiqn6" -d "hash=$md5" 'http://188.166.173.208:31644/')</code>
<code>echo $getr</code>