import requests

def fetch_yml(url, file_name):
    r = requests.get(url)

    with open(file_name+'.yml', 'wb') as f:
        f.write(r.content)

if __name__ == '__main__':
    pass