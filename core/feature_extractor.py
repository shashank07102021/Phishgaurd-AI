import re # re = regular expression , used for pattern matching in text 
import json #json =used to  read /write data files  
from urllib.parse import urlparse# urlparse splits a url into  parts like scheme ,hostname ,path 

#load the exact  feature list in the model  was trained on 
#this ensures we always comupute the same features  in the same order as training 
with open ("D:/Phishgaurd AI/core/features.json", "r") as f :
    FEATURES=json.load(f)

def extract_features(url):
    #split url into parts 
    #eg. https://google.com/search ->scheme = http ,hostname=google.com, path=/search 
    parsed=urlparse(url)
    hostname=parsed.hostname or""#  domain name only  , empty  string if its missing 
    path=parsed.path or ""#everything after the domain , empty string if its missing 
    #helper function  to count  how many times  a charector appears  in the full url  
    def count (char):
       return url.count(char)
    
    features ={
        #length Features 
        'length_url':len(url),#total charectors in url ,phishing  urls  tent to be longer
        'length_hostname':len(hostname),#length of domain only 
        #Ipcheck 
        #legitimate sites  uses domain names ,not in the raw ip like 192.168.1.1
        'ip': 1 if re.match(r'\d+\.\d+\.\d+\.\d+',hostname) else 0,
        #charector count features 
        #count how many times  each special charectors  appears in the url 
        #Phishing  Urls often  have unusual  amount of these charectors  
        'nb_dots':count('.'),
        'nb_hyphens':count('-'),
        'nb_at':count('@'),#@ in url  tricks browser e.g paypal.com@evil.com
        'nb_qm':count('?'),
        'nb_and':count('&'), 
        'nb_or':count('|'),
        'nb_eq':count('='),
        'nb_underscore':count('_'),
        'nb_tilde':count('~'),
        'nb_percent':count('%'),# used to encode /hide charectors 
        'nb_slash':count('/'),
        'nb_star':count('*'),
        'nb_colon':count(':'),
        'nb_comma':count(','),
        'nb_semicolumn':count(';'),
        'nb_dollar':count('$'),
        'nb_space':count(' '),#spaces in the url are always suspicious 
        #Domain features 
        'nb_www':1 if'www'in url else 0,
        'nb_com':url.count('.com'),#more than one  .com is suspicious  e.g. paypal.com.evil.com
        'nb_dslash':url.count('//'),#more than one // is suspicious 
        #https_token=does Url  use Https?
        #note: phishing sites also use https  now so this alone doesnt meant safe 
        'https_token':1 if parsed.scheme =='https' else 0 ,
        #ratio of digits to total url length - high digit  ratio is suspicious 
        'ratio_digits_url': sum(c.isdigit() for c in url)/ len(url) if len(url)>0 else 0,
        #same but only for  the hostname part 
        'ratio_digits_host':sum(c.isdigit() for c in hostname) / len(hostname) if len(hostname)>0  else 0 ,
        #punnycode:xn-- prefix is used  to fake charectors  in domain names 
        #e.g gOOgle.com  can look like  google.com  but uses as  cyrillic  charectors 
        'punycode':1 if 'xn--' in url else 0 ,
        #port : legitimate sites  rarely specify a port  e.g: evil.com:8080 
        'port': 1 if parsed.port else 0 ,
        #tld_in_Path: Domain extension  hiding in path e.g. evil.com/paypal.com/login
        'tld_in_path':1 if re.search(r'\.(com|org|net|gov|edu)',path) else 0,
        #tld_in_subdomain: domain  extension  in sub domain e.g paypal.com.evil.net 
        'tld_in_subdomain':1 if re.search(r'\.(com|org|net|gov|edu)',hostname) else 0,
        #number of subdomains  - more dots in hostnames means more subdomains 
        'nb_subdomains':hostname.count('.'),
        #shortening  services  hide the real destination  URL
        'shortening_service':1 if any (s in url  for s in ['bit.ly','tinyurl','goo.gl','t.co']) else 0,
        #path  end with  a file extension like .php .html,.exe
        'path_extension':1 if re.search(r'\.\w{2,4}$',path)else 0
          }
    #  return  featurs  values in exact  same order as  features.json 
    # this  prevent  silent  errors  when the model  make predictions 
    return[features[f] for f in FEATURES]
    