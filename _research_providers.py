import requests, xml.etree.ElementTree as ET, json, re

def check_sitemap(url):
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            ns = {"ns":"http://www.sitemaps.org/schemas/sitemap/0.9"}
            locs = root.findall(".//ns:loc", ns) or root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc") or root.findall(".//loc")
            urls = [l.text.strip() for l in locs if l.text]
            return r.status_code, len(urls), urls[:5]
        return r.status_code, 0, []
    except Exception as e:
        return str(e), 0, []

results = {}

# IBM SkillsBuild
status, count, samples = check_sitemap("https://skillsbuild.org/sitemap.xml")
print(f"IBM SkillsBuild: {status}, {count} URLs")
if samples: results['ibm_skillsbuild'] = {'sitemap_count': count, 'urls': samples[:5]}

# Great Learning
status, count, samples = check_sitemap("https://www.mygreatlearning.com/sitemap.xml")
print(f"Great Learning: {status}, {count} URLs")
if samples: results['greatlearning'] = {'sitemap_count': count, 'urls': samples[:5]}

# Harvard CS50
try:
    r = requests.get("https://cs50.harvard.edu/courses/", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
    print(f"CS50 courses page: {r.status_code}, {len(r.text)} bytes")
    courses = re.findall(r'<a[^>]*href="(/courses/[^"]*)"[^>]*>([^<]+)</a>', r.text)
    print(f"  Found {len(courses)} course links")
    if courses: results['cs50'] = {'courses': len(courses), 'samples': courses[:5]}
except Exception as e:
    print(f"CS50: Error - {e}")

# Full Stack Open
status, count, samples = check_sitemap("https://fullstackopen.com/sitemap.xml")
print(f"Full Stack Open: {status}, {count} URLs")
if samples: results['fullstackopen'] = {'sitemap_count': count, 'urls': samples[:5]}

# Simplilearn
status, count, samples = check_sitemap("https://www.simplilearn.com/sitemap.xml")
print(f"Simplilearn: {status}, {count} URLs")
if samples: results['simplilearn'] = {'sitemap_count': count, 'urls': samples[:5]}

# UpGrad
status, count, samples = check_sitemap("https://www.upgrad.com/sitemap.xml")
print(f"UpGrad: {status}, {count} URLs")
if samples: results['upgrad'] = {'sitemap_count': count, 'urls': samples[:5]}

# MDN Learn
r = requests.get("https://developer.mozilla.org/sitemap.xml", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
print(f"MDN sitemap.xml: {r.status_code}")
if r.status_code == 200:
    root = ET.fromstring(r.content)
    ns = {"ns":"http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = root.findall(".//ns:loc", ns)
    learn_sitemaps = [l.text.strip() for l in locs if l.text and '/en-US/docs/Learn' in l.text]
    print(f"  Found {len(learn_sitemaps)} Learn sitemaps")
    if learn_sitemaps:
        results['mdn'] = {'learn_sitemaps': len(learn_sitemaps), 'samples': learn_sitemaps[:3]}
        # Check first learn sitemap
        status, count, samples = check_sitemap(learn_sitemaps[0])
        print(f"  First learn sitemap: {status}, {count} URLs")
        if samples: results['mdn']['url_samples'] = samples[:5]

# Salesforce Trailhead
status, count, samples = check_sitemap("https://trailhead.salesforce.com/sitemap.xml")
print(f"Trailhead sitemap: {status}, {count} URLs")
if samples: results['trailhead'] = {'sitemap_count': count, 'urls': samples[:5]}

# Also try content sitemap
status, count, samples = check_sitemap("https://trailhead.salesforce.com/content_sitemap.xml")
print(f"Trailhead content_sitemap: {status}, {count} URLs")
if samples: results['trailhead_content'] = {'sitemap_count': count, 'urls': samples[:5]}

print("\n\n=== SUMMARY ===")
for k, v in results.items():
    print(f"{k}: {json.dumps(v, indent=2)}")
