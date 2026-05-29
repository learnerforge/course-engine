"""
Scraper for roadmap.sh — extracts learning resources from all 74 roadmaps + 5 best-practices.
Sources data from GitHub repo: nilbuild/developer-roadmap
"""
import csv, json, os, re, sys, time
import requests
from datetime import datetime, timezone

COLS = ["raw_id","provider_id","provider_name","source_url","raw_title","raw_url",
        "raw_description","raw_category","raw_subcategory","raw_tags","raw_duration",
        "raw_level","raw_language","raw_certificate_info","raw_badge_info",
        "raw_price_info","raw_rating","raw_reviews_count","raw_enrollment_count",
        "raw_image_url","raw_instructors","raw_json","scraped_at","status","error_message"]

BASE = "https://raw.githubusercontent.com/nilbuild/developer-roadmap/master/src/data"
REPO_API = "https://api.github.com/repos/nilbuild/developer-roadmap/contents/src/data"
UA = {"User-Agent": "Mozilla/5.0"}
utc_now = lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def fetch(url):
    r = requests.get(url, timeout=30, headers=UA)
    if r.status_code == 200:
        return r
    return None

def get_roadmap_dirs():
    """Fetch all roadmap and best-practices directory names."""
    dirs = []
    for prefix in ("roadmaps", "best-practices"):
        r = fetch(f"{REPO_API}/{prefix}")
        if r:
            for item in r.json():
                if item["type"] == "dir":
                    dirs.append((prefix, item["name"]))
    return dirs

def get_content_files(prefix, name):
    """Get list of content markdown files for a roadmap using GitHub API."""
    r = fetch(f"{REPO_API}/{prefix}/{name}/content")
    if not r:
        return []
    try:
        files = []
        for item in r.json():
            if item["type"] == "dir" and item["name"] == "content":
                content_r = fetch(item["url"])
                if content_r:
                    for sub in content_r.json():
                        if sub["name"].endswith(".md"):
                            files.append(sub["name"])
                break
        return files
    except Exception as e:
        print(f"  Error listing content for {prefix}/{name}: {e}")
        return []

def parse_resources_from_md(text):
    """Extract [@type@title](url) resource links from markdown content."""
    pattern = r'\[\s*@(\w+)@\s*([^\]]*?)\s*\]\s*\(([^)]+)\)'
    resources = []
    for match in re.finditer(pattern, text):
        rtype = match.group(1).lower()
        title = match.group(2).strip()
        url = match.group(3).strip()
        resources.append({"type": rtype, "title": title, "url": url})
    return resources

def get_roadmap_md(prefix, name):
    """Get metadata from the markdown frontmatter file."""
    r = fetch(f"{BASE}/{prefix}/{name}/{name}.md")
    if r:
        return r.text
    return ""

def extract_metadata_from_md(text):
    """Extract title and description from markdown frontmatter."""
    title = name.replace("-", " ").title()
    desc = ""
    # Try to extract from YAML frontmatter
    fm_match = re.search(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        for line in fm.split('\n'):
            if line.startswith('title:'):
                title = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith('description:'):
                desc = line.split(':', 1)[1].strip().strip('"\'')
    if not desc:
        # Take first paragraph as description
        para = re.search(r'\n\n([^#\n][^\n]+)', text)
        if para:
            desc = para.group(1).strip()[:500]
    return title, desc

def get_roadmap_json(prefix, name):
    """Get the React Flow JSON for topic extraction."""
    r = fetch(f"{BASE}/{prefix}/{name}/{name}.json")
    if r:
        try:
            return r.json()
        except:
            pass
    return None

def extract_topics_from_json(data):
    """Extract topic/subtopic labels and any embedded resource links from JSON."""
    topics = []
    if not data or "nodes" not in data:
        return topics
    for node in data["nodes"]:
        nd = node.get("data", {})
        label = nd.get("label", "").strip()
        if not label:
            continue
        ntype = node.get("type", "")
        if ntype not in ("topic", "subtopic", "title"):
            continue
        # Extract inline resources if any
        resources = nd.get("resources", [])
        if isinstance(resources, list):
            for res in resources:
                if isinstance(res, dict) and res.get("url"):
                    topics.append({
                        "label": label,
                        "type": ntype,
                        "res_title": res.get("title", "").strip(),
                        "res_url": res.get("url", "").strip(),
                    })
    return topics

# === Main Scraper ===
print("Fetching roadmap directories...")
dirs = get_roadmap_dirs()
print(f"  Found {len(dirs)} directories")

records = []
seen_urls = set()
total_content_files = 0
total_topic_labels = 0

for prefix, name in dirs:
    roadmap_label = name.replace("-", " ").title()
    md_text = get_roadmap_md(prefix, name)
    meta_title, meta_desc = extract_metadata_from_md(md_text)

    # Method 1: Get resources from content markdown files
    content_files = get_content_files(prefix, name)
    total_content_files += len(content_files)

    for cf in content_files:
        topic_name = cf.split("@")[0].replace("-", " ").title()
        r = fetch(f"{BASE}/{prefix}/{name}/content/{cf}")
        if not r:
            continue
        resources = parse_resources_from_md(r.text)
        for res in resources:
            url = res["url"]
            if url in seen_urls:
                continue
            seen_urls.add(url)
            records.append({
                "raw_id": f"roadmap_{prefix}_{name}_{hash(url)%1000000:06d}",
                "provider_id": "roadmap_sh",
                "provider_name": "Roadmap.sh",
                "source_url": f"{BASE}/{prefix}/{name}/{name}.json",
                "raw_title": res["title"][:500] or f"{meta_title}: {topic_name}",
                "raw_url": url,
                "raw_description": f"Resource for '{topic_name}' in {meta_title} roadmap",
                "raw_category": meta_title[:100],
                "raw_subcategory": topic_name[:100],
                "raw_tags": json.dumps([prefix, res["type"], name]),
                "raw_duration": "",
                "raw_level": "",
                "raw_language": "English",
                "raw_certificate_info": "",
                "raw_badge_info": "",
                "raw_price_info": "free" if res["type"] in ("official", "article", "website") else "unknown",
                "raw_rating": "",
                "raw_reviews_count": "",
                "raw_enrollment_count": "",
                "raw_image_url": "",
                "raw_instructors": "",
                "raw_json": json.dumps({"roadmap": name, "resource_type": res["type"], "topic": topic_name}),
                "scraped_at": utc_now(),
                "status": "active",
                "error_message": "",
            })

    # Method 2: Get topics from JSON with inline resources
    jdata = get_roadmap_json(prefix, name)
    topics = extract_topics_from_json(jdata)
    total_topic_labels += len(topics)

    for t in topics:
        url = t["res_url"]
        if url in seen_urls:
            continue
        seen_urls.add(url)
        records.append({
            "raw_id": f"roadmap_{prefix}_{name}_{hash(url)%1000000:06d}",
            "provider_id": "roadmap_sh",
            "provider_name": "Roadmap.sh",
            "source_url": f"{BASE}/{prefix}/{name}/{name}.json",
            "raw_title": t["res_title"][:500] or t["label"],
            "raw_url": url,
            "raw_description": f"Topic '{t['label']}' ({t['type']}) in {meta_title} roadmap",
            "raw_category": meta_title[:100],
            "raw_subcategory": t["label"][:100],
            "raw_tags": json.dumps([prefix, "json_inline", name]),
            "raw_duration": "",
            "raw_level": "",
            "raw_language": "English",
            "raw_certificate_info": "",
            "raw_badge_info": "",
            "raw_price_info": "unknown",
            "raw_rating": "",
            "raw_reviews_count": "",
            "raw_enrollment_count": "",
            "raw_image_url": "",
            "raw_instructors": "",
            "raw_json": json.dumps({"roadmap": name, "source": "json", "topic": t["label"]}),
            "scraped_at": utc_now(),
            "status": "active",
            "error_message": "",
        })

    if len(dirs) > 0 and (len(records) % 500 < 50 or True):
        print(f"  {prefix}/{name}: {len(content_files)} content files, {len(topics)} topics, {len(records)} total records so far")

# Deduplicate by URL within our own records
print(f"\nTotal raw records: {len(records)}")
print(f"Content files processed: {total_content_files}")
print(f"JSON topic resources: {total_topic_labels}")

# Write output
os.makedirs("data/raw", exist_ok=True)
with open("data/raw/roadmap_sh_raw.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(records)

print(f"Saved {len(records)} records to data/raw/roadmap_sh_raw.csv")
