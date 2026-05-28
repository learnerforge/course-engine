import requests, json, re

r = requests.get('https://openstax.org/subjects', timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
html = r.text

# Look for __NEXT_DATA__ 
m = re.search(r'id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    print(json.dumps(data, indent=2)[:3000])
else:
    print("No __NEXT_DATA__ found")
    # Look for any JSON in script tags
    for s in re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL):
        if '__NEXT_DATA__' in s:
            print("Found in inline:", s[:500])

# Also check for books listing page
r2 = requests.get('https://openstax.org/', timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
m2 = re.search(r'id="__NEXT_DATA__"[^>]*>(.*?)</script>', r2.text, re.DOTALL)
if m2:
    data2 = json.loads(m2.group(1))
    props = data2.get('props', {}).get('pageProps', {})
    print("\nPageProps keys:", list(props.keys())[:20])
    if 'books' in props:
        print("Books:", len(props['books']))
        for b in props['books'][:3]:
            print(json.dumps(b, indent=2)[:300])
