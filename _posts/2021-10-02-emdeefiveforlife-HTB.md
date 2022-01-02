```bash
#!/bin/bash

getw=$(curl -s --cookie "PHPSESSID=f8oau3r713ir774pq8cclaiqn6" 'http://188.166.173.208:31644/' | grep -Po '[\w]{20}')
echo $getw
md5=$(echo -n $getw | md5sum | sed 's/ .*$//')
echo $md5
getr=$(curl -s  --cookie "PHPSESSID=f8oau3r713ir774pq8cclaiqn6" -d "hash=$md5" 'http://188.166.173.208:31644/')
echo $getr
```