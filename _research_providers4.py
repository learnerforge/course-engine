import requests, xml.etree.ElementTree as ET, json, re

# IBM SkillsBuild - extract course data from JSON-LD
r = requests.get("https://skillsbuild.org/adult-learners/explore-learning", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
scripts = re.findall(r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.DOTALL)
if scripts:
    data = json.loads(scripts[0])
    print("IBM SkillsBuild NEXT_DATA keys:", list(data.keys()))
    # Navigate the structure
    props = data.get('props', {}).get('pageProps', {})
    print("pageProps keys:", list(props.keys()))
    # Look for course-related data
    for k, v in props.items():
        if isinstance(v, dict):
            print(f"  {k}: {list(v.keys())[:10]}")
        elif isinstance(v, list):
            print(f"  {k}: list of {len(v)}")
        else:
            sv = str(v)[:100]
            print(f"  {k}: {sv}")

# Also try /api/courses or similar
for path in ['/api/courses', '/api/explore', '/graphql', '/api/content']:
    try:
        r = requests.get(f"https://skillsbuild.org{path}", timeout=10, headers={"User-Agent":"Mozilla/5.0"})
        print(f"\n{path}: {r.status_code} - {r.text[:200]}")
    except: pass

# MDN - handle non-gz sitemap
r = requests.get("https://developer.mozilla.org/sitemaps/en-us/sitemap.xml.gz", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
print(f"\nMDN sitemap content-type: {r.headers.get('content-type')}")
print(f"  First bytes: {r.content[:50]}")
# It's just .xml without gzip
root = ET.fromstring(r.content)
urls = [l.text.strip() for l in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if l.text]
print(f"  Total: {len(urls)}")
learn_urls = [u for u in urls if '/docs/Learn/' in u]
print(f"  Learn: {len(learn_urls)}")
# Get unique module pages
modules = set(u.rsplit('/docs/Learn/',1)[-1].split('/')[0] for u in learn_urls)
print(f"  Unique modules: {len(modules)}: {sorted(modules)[:30]}")

# CS50 - try Harvard Extension or CS50-specific
for url in ["https://pll.harvard.edu/course/cs50s-introduction-computer-science", 
            "https://www.edx.org/search?q=cs50",
            "https://cs50.harvard.edu/x/2025/"]:
    r = requests.get(url, timeout=15, headers={"User-Agent":"Mozilla/5.0"})
    print(f"\n{url}: {r.status_code}")
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', r.text)
    if h1: print(f"  Title: {h1.group(1)[:100]}")
