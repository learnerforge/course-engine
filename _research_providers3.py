import requests, xml.etree.ElementTree as ET, json, re, gzip, io

# IBM SkillsBuild - check explore pages for course listings
for path in ['/adult-learners/explore-learning', '/adult-learners', '/students', '/adult-learners/digital-credentials']:
    r = requests.get(f"https://skillsbuild.org{path}", timeout=15, headers={"User-Agent":"Mozilla/5.0"})
    print(f"IBM {path}: {r.status_code}, {len(r.text)} bytes")
    # Find course/program links
    links = re.findall(r'href=["\']([^"\']*skillsbuild[^"\']*course[^"\']*)["\']|href=["\']([^"\']*/learn[^"\']*)["\']', r.text)
    if links: print(f"  Found {len(links)} course/learn links")
    # Find JSON data
    scripts = re.findall(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>', r.text, re.DOTALL)
    for s in scripts[:2]:
        print(f"  JSON script: {s[:200]}")

# Great Learning - check a sample course page
r = requests.get("https://www.mygreatlearning.com/academy/learn-for-free/courses/excel-for-beginners", timeout=15, headers={"User-Agent":"Mozilla/5.0"})
print(f"\nGreat Learning sample course: {r.status_code}")
h1 = re.search(r'<h1[^>]*>(.*?)</h1>', r.text)
if h1: print(f"  Title: {h1.group(1)}")
desc = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', r.text)
if desc: print(f"  Description: {desc.group(1)[:200]}")

# Great Learning - get all course URLs from academy sitemap
r = requests.get("https://www.mygreatlearning.com/gl_academy_sitemap.xml", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
urls = [l.text.strip() for l in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if l.text]
course_urls = [u for u in urls if '/learn-for-free/courses/' in u]
print(f"\nGreat Learning free courses: {len(course_urls)}")
for u in course_urls[:5]: print(f"  {u}")

# Full Stack Open - detailed breakdown
r = requests.get("https://fullstackopen.com/sitemap.xml", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
urls = [l.text.strip() for l in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if l.text]
en = [u for u in urls if '/en/' in u]
# Filter to only part pages (not every subsection)
parts = sorted(set(u.rsplit('/en/',1)[-1].split('/')[0] for u in en if '/en/' in u))
print(f"\nFull Stack Open EN parts: {parts}")

# MDN - check gzipped en-us sitemap for learn pages
r = requests.get("https://developer.mozilla.org/sitemaps/en-us/sitemap.xml.gz", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
gz = gzip.GzipFile(fileobj=io.BytesIO(r.content))
content = gz.read().decode('utf-8')
root = ET.fromstring(content)
urls = [l.text.strip() for l in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if l.text]
learn_urls = [u for u in urls if '/docs/Learn/' in u]
print(f"\nMDN en-us total: {len(urls)}, Learn: {len(learn_urls)}")
# Further filter to get just the top-level learn modules
learn_toplevel = sorted(set(u.rsplit('/docs/Learn/',1)[-1].split('/')[0] for u in learn_urls if '/docs/Learn/' in u))
print(f"  Top-level Learn modules: {learn_toplevel[:20]}")
# Get unique course-like pages (not sub-articles)
learn_modules = sorted(set('/'.join(u.split('/')[:8]) for u in learn_urls if '/docs/Learn/' in u))
print(f"  Module-level pages: {len(learn_modules)}")
for u in learn_modules[:5]: print(f"    {u}")

# Trailhead - classify content types
r = requests.get("https://trailhead.salesforce.com/content_sitemap.xml", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
urls = [l.text.strip() for l in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if l.text]
types = {}
for u in urls:
    parts = u.split('/')
    for i, p in enumerate(parts):
        if p in ('modules', 'projects', 'trails', 'superbadges'):
            types[p] = types.get(p, 0) + 1
            break
print(f"\nTrailhead content types: {json.dumps(types)}")
print(f"Total content URLs: {len(urls)}")
