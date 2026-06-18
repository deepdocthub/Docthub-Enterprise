# playwright_link_xpath_report.py
# Run:
#   pip install playwright
#   playwright install
#   python playwright_link_xpath_report.py

import csv
import json
from playwright.sync_api import sync_playwright

TARGET_URL = "https://www.docthub.com/"

TARGET_LINKS = [
    "https://www.docthub.com/",
    "",
    "",
    "https://jobs.docthub.com/",
    "https://courses.docthub.com/",
    "https://events.docthub.com/",
    "https://jobs.docthub.com/browse-jobs",
    "https://jobs.docthub.com/all-jobs?pageNumber=1&pageSize=50&isFacet=true&categories=4",
    "https://jobs.docthub.com/top-healthcare-companies",
    "https://www.docthub.com/resume-builder",
    "https://www.docthub.com/healthcare-career-app",
    "https://courses.docthub.com/browse-healthcare-courses",
    "https://courses.docthub.com/all-courses?pageNumber=1&pageSize=10&isFacet=true&route=&qualifications=153&qualifications=496&qualifications=1079&qualifications=1127",
    "https://courses.docthub.com/fellowships?pageNumber=1&pageSize=10&isFacet=true",
    "https://www.docthub.com/resume-builder",
    "https://www.docthub.com/healthcare-career-app",
    "https://events.docthub.com/",
    "https://events.docthub.com/meet-ups",
    "https://events.docthub.com/conference",
    "https://events.docthub.com/workshop",
    "https://events.docthub.com/continuing-medical-education-cme",
    "https://events.docthub.com/webinar",
    "https://www.docthub.com/healthcare-career-app",
    "https://www.docthub.com/logbook",
    "https://www.docthub.com/resume-builder",
    "https://www.docthub.com/healthcare-career-app",
    "https://www.docthub.com/recruiter",
    "https://www.docthub.com/institute",
    "https://www.docthub.com/event-organizer",
    "https://www.docthub.com/membership-management",
    "https://auth.docthub.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26scope%3Dopenid%2520profile%2520email%26code_challenge%3D4ULtSAoUUZxLQ1nchb7dC2oJtJ0fPWOQrxi6YbpQ3cQ%26code_challenge_method%3DS256%26redirect_uri%3Dhttps%253A%252F%252Fdev.dochub.in%252F%20api%252Fauth%252Fcallback%252Fdoct-branding%26client_id%3Ddoct.branding.app",
    "https://courses.docthub.com/",
    "https://play.google.com/store/apps/details?id=com.docthub.app",
    "https://apps.apple.com/in/app/docthub-health-career-app/id1625281489",
    "https://www.docthub.com/about-us",
    "https://www.docthub.com/about-us",
    "https://www.docthub.com/media-releases",
    "https://www.docthub.com/media-releases/company-milestones?id=1&type=category",
    "https://www.docthub.com/media-releases/news-coverage?id=6&type=category",
    "https://jobs.docthub.com/",
    "https://courses.docthub.com/",
    "https://events.docthub.com/",
    "",
    "https://www.docthub.com/enterprise-solutions",
    "https://www.facebook.com/docthub/",
    "https://twitter.com/docthub",
    "https://www.linkedin.com/company/docthub2017/",
    "https://www.instagram.com/docthub/",
    "https://www.youtube.com/c/Docthub1/videos",
    "https://play.google.com/store/search?q=docthub&c=apps&hl=en",
    "https://apps.apple.com/in/app/docthub-healthcare-career-app/id1625281489",
    "https://jobs.docthub.com/",
    "https://courses.docthub.com/",
    "https://events.docthub.com/",
    "https://docthub.com/healthcare-career-app",
    "https://jobs.docthub.com/drop-your-resume",
    "https://docthub.com/explore-courses-after-12th",
    "https://docthub.com/logbook",
    "https://docthub.com/resume-builder",
    "https://docthub.com/healthcare-career-app",
    "https://news.docthub.com/",
    "https://docthub.com/course-pages",
    "https://docthub.com/jobrole-pages",
    "https://docthub.com/recruiter",
    "https://docthub.com/institute",
    "https://docthub.com/event-organizer",
    "https://docthub.com/membership-management",
    "https://docthub.com/qr-check-in-app",
    "https://docthub.com/enterprise-solutions",
    "",
    "https://enterprise.docthub.com/en/register",
    "https://docthub.com/about-us",
    "https://docthub.com/media-releases",
    "https://blogs.docthub.com/",
    "https://docthub.com/contact-us",
    "https://docthub.com/",
    "https://docthub.com/terms-conditions",
    "https://docthub.com/privacy-policy",
    "https://docthub.com/cookies-policy",
    "https://docthub.com/payment-policy",
    "https://docthub.com/disclaimer-policy",
    "https://enterprise.docthub.com/enterprise-terms-conditions",
    "https://enterprise.docthub.com/enterprise-privacy-policy",
    "https://enterprise.docthub.com/enterprise-payment-policy",
]


def normalize_url(url: str) -> str:
    if url.startswith(("mailto:", "tel:")):
        return url
    return url.rstrip("/")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Opening: {TARGET_URL}")
        page.goto(TARGET_URL, wait_until="networkidle")

        anchor_data = page.eval_on_selector_all(
            "a[href]",
            """
            (anchors) => {
                function getXPath(el) {
                    if (!el || el.nodeType !== 1) return null;

                    if (el.id) return `//*[@id="${el.id}"]`;

                    const parts = [];
                    while (el && el.nodeType === 1) {
                        let index = 1;
                        let sibling = el.previousElementSibling;

                        while (sibling) {
                            if (sibling.tagName === el.tagName) index++;
                            sibling = sibling.previousElementSibling;
                        }

                        parts.unshift(`${el.tagName.toLowerCase()}[${index}]`);
                        el = el.parentElement;
                    }

                    return "/" + parts.join("/");
                }

                return anchors.map((a, domIndex) => {
                    const rawHref = a.getAttribute("href") || "";
                    const fullHref =
                        rawHref.startsWith("mailto:") || rawHref.startsWith("tel:")
                            ? rawHref
                            : new URL(rawHref, location.origin).href;

                    return {
                        domIndex,
                        text: (a.innerText || "").trim(),
                        href: fullHref,
                        xpath: getXPath(a),
                        target: a.getAttribute("target") || "",
                        rel: a.getAttribute("rel") || ""
                    };
                });
            }
            """
        )

        normalized_map = {}
        for item in anchor_data:
            key = normalize_url(item["href"])
            normalized_map.setdefault(key, []).append(item)

        rows = []

        for list_index, url in enumerate(TARGET_LINKS):
            normalized = normalize_url(url)
            matches = normalized_map.get(normalized, [])

            if not matches:
                rows.append({
                    "listIndex": list_index,
                    "targetUrl": url,
                    "found": "NO",
                    "matchCount": 0,
                    "domIndex": "",
                    "linkText": "",
                    "href": "",
                    "xpath": "",
                    "target": "",
                    "rel": ""
                })
                continue

            for match in matches:
                rows.append({
                    "listIndex": list_index,
                    "targetUrl": url,
                    "found": "YES",
                    "matchCount": len(matches),
                    "domIndex": match["domIndex"],
                    "linkText": match["text"] or "(no text)",
                    "href": match["href"],
                    "xpath": match["xpath"],
                    "target": match["target"],
                    "rel": match["rel"]
                })

        csv_headers = [
            "listIndex",
            "targetUrl",
            "found",
            "matchCount",
            "domIndex",
            "linkText",
            "href",
            "xpath",
            "target",
            "rel"
        ]

        with open("link-xpath-report.csv", "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            writer.writeheader()
            writer.writerows(rows)

        with open("link-xpath-report.json", "w", encoding="utf-8") as json_file:
            json.dump(rows, json_file, indent=2, ensure_ascii=False)

        print("Done:")
        print(" - link-xpath-report.csv")
        print(" - link-xpath-report.json")

        browser.close()


if __name__ == "__main__":
    main()