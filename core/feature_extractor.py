import re 
import json 
from urllib.parse import urlparse

with open ("D:/Phishgaurd AI/core/features.json", "r") as f :
    FEATURES=json.load(f)

def extract_features(url):
    parsed=urlparse(url)
    hostname=parsed.hostname or""
    path=parsed.path or ""
     
    def count (char):
       return url.count(char)
    
    features ={
        'length_url':len(url),
        'length_hostname':len(hostname),
        'ip': 1 if re.match(r'\d+\.\d+\.\d+\.\d+',hostname) else 0,
        'nb_dots':count('.'),
        'nb_hyphens':count('-'),
        'nb_at':count('@'),
        'nb_qm':count('?'),
        'nb_and':count('&'),
        'nb_dots':count('.'), 
        'nb_or':count('|'),
        'nb_eq':count('='),
        'nb_underscore':count('_'),
        'nb_tilde':count('~'),
        'nb_percent':count('%'),
        'nb_slash':count('/'),
        'nb_star':count('*'),
        'nb_colon':count(':'),
        'nb_comma':count(','),''
        'nb_semicolumn':count(';'),
        'nb_dollar':count('$'),
        'nb_space':count(' '),
        'nb_www':1 if'www'in url else 0,
        'nb_com':url.count('.com'),
        'nb_dslash':url.count('//'),
        'https_token':1 if parsed.scheme =='https' else 0 ,
        'ratio_digits_url': sum(c.isdigit() for c in url)/ len(url) if len(url)>0 else 0,
        'ratio_digits_host':sum(c.isdigit() for c in hostname) / len(hostname) if len(hostname)>0  else 0 ,
        'punycode':1 if 'xn--' in url else 0 ,
        'port': 1 if parsed.port else 0 ,
        'tld_in_path':1 if re.search(r'\.(com|org|net|gov|edu)',path) else 0,
        'tld_in_subdomain':1 if re.search(r'\.(com|org|net|gov|edu)',path) else 0,
        'nb_subdomains':hostname.count('.'),
        'shortening_service':1 if any (s in url  for s in ['bit.ly','tinyurl','goo.gl,t.co']) else 0,
        'path_extension':1 if re.search(r'\.\w{2,4}$',path)else 0
          }
    return[features[f] for f in FEATURES]
    