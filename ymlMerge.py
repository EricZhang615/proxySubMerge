from ruamel import yaml
import re

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def merge_yaml(template, sub1, sub2, rules):
    if template['proxies'] is None:
        template['proxies'] = []
    # template['proxies'] = template['proxies'] + sub1['proxies'] + sub2['proxies']
    template['proxies'] = template['proxies'] + sub1['proxies']

    for i in range(len(template['proxy-groups'])):
        if template['proxy-groups'][i]['name'] == 'Dash':
            template['proxy-groups'][i]['proxies'] += proxy_group_dash(template['proxies'])
        if template['proxy-groups'][i]['name'] == 'Proxies':
            template['proxy-groups'][i]['proxies'] += proxy_group_proxies(template['proxies'])
        if template['proxy-groups'][i]['name'] == 'HK':
            template['proxy-groups'][i]['proxies'] = proxy_group_hk(template['proxies'])
        if template['proxy-groups'][i]['name'] == 'JP':
            template['proxy-groups'][i]['proxies'] = proxy_group_jp(template['proxies'])
        if template['proxy-groups'][i]['name'] == 'SG':
            template['proxy-groups'][i]['proxies'] = proxy_group_sg(template['proxies'])
        if template['proxy-groups'][i]['name'] == 'TW':
            template['proxy-groups'][i]['proxies'] = proxy_group_tw(template['proxies'])
        if template['proxy-groups'][i]['name'] == 'US':
            template['proxy-groups'][i]['proxies'] = proxy_group_us(template['proxies'])
        if template['proxy-groups'][i]['name'] == 'CN':
            template['proxy-groups'][i]['proxies'] += proxy_group_cn(template['proxies'])

    if template['rules'] is None:
        template['rules'] = []
    template['rules'] += rules['rules']

    template['rule-providers'] = rules['rule-providers']

    return template

def proxy_group_dash(proxy_list):
    res = []
    for p in proxy_list:
        if re.match(r'^.*(日本|香港) - 高端.*', p['name']):
            res += [p['name']]
    return res

def proxy_group_proxies(proxy_list):
    res = []
    for p in proxy_list:
        if re.match(r'^((.* - .*)|(.{5}(?!(香港|日本|新加坡|台湾|美国)).{3,}IEPL.*))', p['name']):
            res += [p['name']]
    return res

def proxy_group_hk(proxy_list):
    res = []
    for p in proxy_list:
        if re.match(r'^.*香港.*IEPL.*', p['name']):
            res += [p['name']]
    return res

def proxy_group_jp(proxy_list):
    res = []
    for p in proxy_list:
        if re.match(r'^.*日本.*IEPL.*', p['name']):
            res += [p['name']]
    return res

def proxy_group_sg(proxy_list):
    res = []
    for p in proxy_list:
        if re.match(r'^.*新加坡.*IEPL.*', p['name']):
            res += [p['name']]
    return res

def proxy_group_tw(proxy_list):
    res = []
    for p in proxy_list:
        if re.match(r'^.*台湾.*IEPL.*', p['name']):
            res += [p['name']]
    return res

def proxy_group_us(proxy_list):
    res = []
    for p in proxy_list:
        if re.match(r'^.*美国.*IEPL.*', p['name']):
            res += [p['name']]
    return res

def proxy_group_cn(proxy_list):
    res = []
    for p in proxy_list:
        if re.match(r'^.*China.*', p['name']):
            res += [p['name']]
    return res


def save_yaml(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, indent=2, Dumper=yaml.RoundTripDumper)

if __name__ == '__main__':
    template = load_yaml('template.yml')
    sub1 = load_yaml('1669819809781.yml')
    sub2 = load_yaml('1605442802675.yml')
    rules = load_yaml('rules.yml')
    merge_yaml(template, sub1, sub2, rules)
    save_yaml('merged.yml', template)