import requests, xml.etree.ElementTree as ET, json, re

def count_by_pattern(urls, patterns):
    counts = {}
    for p in patterns:
        counts[p] = sum(1 for u in urls if p in u)
    return counts

# IBM SkillsBuild - filter for course-like URLs
r = requests.get("https://skillsbuild.org/sitemap.xml", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"ns":"http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [l.text.strip() for l in root.findall(".//ns:loc", ns) if l.text]
print(f"IBM SkillsBuild total: {len(urls)}")
print(f"  Patterns: {count_by_pattern(urls, ['/course/', '/learn/', '/explore', '/adult-learners', '/educators', '/youth', '/students'])}")

# Great Learning - check academy sitemap
r = requests.get("https://www.mygreatlearning.com/gl_academy_sitemap.xml", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"ns":"http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [l.text.strip() for l in root.findall(".//ns:loc", ns) if l.text]
print(f"\nGreat Learning academy: {len(urls)} URLs")
print(f"  Patterns: {count_by_pattern(urls, ['/academy/', '/course/', '/learn/'])}")
for u in urls[:3]: print(f"  Sample: {u}")

# CS50 - check different URL patterns
for url in ["https://cs50.harvard.edu/colleges/", "https://cs50.harvard.edu/", "https://pll.harvard.edu/course/cs50"]:
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent":"Mozilla/5.0"})
        courses = re.findall(r'<a[^>]*href="([^"]*cs50[^"]*)"[^>]*>([^<]+)</a>', r.text, re.I)
        if courses: print(f"\nCS50 {url}: {len(courses)} course links")
    except: pass

# Try CS50 sitemap  
r = requests.get("https://cs50.harvard.edu/sitemap.xml", timeout=15, headers={"User-Agent":"Mozilla/5.0"})
print(f"\nCS50 sitemap.xml: {r.status_code}")
if r.status_code == 200:
    root = ET.fromstring(r.content)
    urls = [l.text.strip() for l in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if l.text]
    print(f"  {len(urls)} URLs")
    print(f"  Patterns: {count_by_pattern(urls, ['/course', '/lecture', '/pset'])}")
    for u in urls[:5]: print(f"    {u}")

# Full Stack Open - filter for English only
r = requests.get("https://fullstackopen.com/sitemap.xml", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"ns":"http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [l.text.strip() for l in root.findall(".//ns:loc", ns) if l.text]
en = [u for u in urls if '/en/' in u]
print(f"\nFull Stack Open total: {len(urls)}, English: {len(en)}, others: {len(urls)-len(en)}")
print(f"  Sample EN: {en[:5] if en else urls[:5]}")

# Simplilearn - filter for course pages
r = requests.get("https://www.simplilearn.com/sitemap.xml", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
urls = [l.text.strip() for l in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if l.text]
print(f"\nSimplilearn total: {len(urls)}")
# Course pages typically have certification-training or just the course name pattern
course_like = [u for u in urls if any(p in u for p in ['-training', '-course', '-certification', '/skill'])]
print(f"  Course-like: {len(course_like)}")
blog = [u for u in urls if '/blog/' in u or '/resources/' in u]
print(f"  Blog/resource: {len(blog)}")
for u in course_like[:5]: print(f"  {u}")

# UpGrad - filter for course-like pages
r = requests.get("https://www.upgrad.com/sitemap.xml", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
urls = [l.text.strip() for l in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if l.text]
print(f"\nUpGrad total: {len(urls)}")
course_like = [u for u in urls if any(p in u for p in ['/course/', '/program/', '-certification', '-training', '/degree'])]
blog = [u for u in urls if '/blog/' in u.lower()]
print(f"  Course-like: {len(course_like)}, Blog: {len(blog)}")
for u in course_like[:5]: print(f"  {u}")

# MDN - check different sitemap structure
r = requests.get("https://developer.mozilla.org/sitemap.xml", timeout=20, headers={"User-Agent":"Mozilla/5.0"})
print(f"\nMDN sitemap.xml status: {r.status_code}")
print(f"  First 500 chars: {r.text[:500]}")
# Check for sitemap index structure
root = ET.fromstring(r.content)
locs = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc") or root.findall(".//loc")
print(f"  Found {len(locs)} sitemap references")
for l in locs[:20]:
    print(f"    {l.text}")
