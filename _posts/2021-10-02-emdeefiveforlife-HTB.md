<code>
#!/bin/bash

md5=$(curl -s --cookie "PHPSESSID=f8oau3r713ir774pq8cclaiqn6" 'http://188.166.173.208:31644/' | grep -Po '[\w]{20}')
echo $md5
target=$(echo -n $md5 | md5sum | sed 's/ .*$//')
echo $target
html=$(curl -s  --cookie "PHPSESSID=f8oau3r713ir774pq8cclaiqn6" -d "hash=$target" 'http://188.166.173.208:31644/')
echo $html
</code>