from urllib.parse import urlparse
from typing import Optional, Tuple, List
from lib.scraper import scrape_html
from lib.gemini import analyze_content_with_gemini, summarize_content_with_gemini

def process_url(url, args, page_headings, scraped_urls, initial_context=None) -> Tuple[Optional[str], List[str], Optional[str]]:
    """Processes a single URL, analyzes content with Gemini, and handles output, including reasoning for related links and initial context."""
    print(f"\n🔎 [PROCESSING URL]: {url}")
    if url in scraped_urls:
        return None, [], None

    html_content = scrape_html(url)
    scraped_urls.add(url)

    if html_content:
        main_content_prompt = args.prompt if args.prompt else None

        gemini_analysis_response = analyze_content_with_gemini(html_content, url, initial_context, main_content_prompt)

        if gemini_analysis_response:
            page_heading_text = gemini_analysis_response.suggested_filename if gemini_analysis_response.suggested_filename else urlparse(url).path.strip('/').replace('/', '_') or "Page_Content"
            page_heading = f"# {page_heading_text.replace('_', ' ').title()}\n\n"
            page_headings[url] = page_heading_text

            output_content = page_heading + gemini_analysis_response.markdown_content + "\n---\n"

            related_links_to_process = []
            if args.crawl_related:
                for link in gemini_analysis_response.related_links: 
                    if link.url not in scraped_urls:
                        related_links_to_process.append(link.url)
                        reason = gemini_analysis_response.related_links_reasoning.get(link.url, "No reason provided.")
                        print(f"\n\t- 🔗 [RELATED]: {link.url}\n\t- 💭 {reason}")

            current_page_context = None
            if initial_context is None:
                current_page_context = summarize_content_with_gemini(gemini_analysis_response.markdown_content)
                print(f"\n💬 [INITIAL CONTEXT] Generated from {url}:\n{current_page_context}")

            return output_content, related_links_to_process, current_page_context
        else:
            return None, [], None
    else:
        return None, [], None