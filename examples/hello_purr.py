import requests
client=requests.session()
authoentication_key='set me to the session token for your user'

client.headers["Authentication"]='Token '+authoentication_key

def add_urls(session,hashes,urls):
    d={
        'urls':urls,
        'sha2':hashes
    }
    json=d

def rm_urls(session,hashes,urls):
    d={
        'urls':urls,
        'sha2':hashes
    }
    r=session.post(json=d)

def counts_for_hash(session,hash):
    d={
        'hash':hash
    }
    r=session.get(json=d)
    return r.json()