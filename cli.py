import argparse
from dotenv import load_dotenv
from typing import List, Set, Dict, Optional, Tuple
from lib.processor import process_url
from lib.gemini import suggest_filename_with_gemini

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description='Web Scraper with Gemini API for Documentation.')
    parser.add_argument('url', type=str, help='The starting URL to scrape.')
    parser.add_argument('-r', '--crawl-related', action='store_true', help='Crawl and analyze related links found on the page.')
    parser.add_argument('-d', '--crawl-depth', type=int, default=1, help='Maximum depth to crawl related links (default: 1).')
    parser.add_argument('-p', '--prompt', type=str, help='Optional custom prompt for Gemini content extraction.')
    parser.add_argument('-o', '--output', type=str, default="documentation_output.md", help='Output Markdown filename (default: documentation_output.md).')

    args = parser.parse_args()

    output_markdown_content: List[str] = []
    urls_to_process: List[Tuple[str, int]] = [(args.url, 0)]
    scraped_urls: Set[str] = set()
    page_headings: Dict[str, str] = {}
    initial_context_summary: Optional[str] = None

    filename_suggested = False
    suggested_filename_base = "documentation_output"

    while urls_to_process:
        current_url, current_depth = urls_to_process.pop(0)
        page_content_md, related_links, current_page_context = process_url(current_url, args, page_headings, scraped_urls, initial_context_summary)

        if page_content_md:
            if not filename_suggested:
                first_page_content_snippet = page_content_md[:500] if page_content_md else ""
                suggested_filename_base = suggest_filename_with_gemini(first_page_content_snippet)
                if not suggested_filename_base:
                    suggested_filename_base = "documentation_output"
                if args.output == "documentation_output.md":
                    args.output = f"{suggested_filename_base}.md"
                filename_suggested = True

            output_markdown_content.append(page_content_md)
            if args.crawl_related and current_depth < args.crawl_depth:
                for linked_url in related_links:
                    if linked_url not in scraped_urls:
                        urls_to_process.append((linked_url, current_depth + 1))

            if initial_context_summary is None and current_page_context:
                initial_context_summary = current_page_context

    final_output = "\n".join(output_markdown_content)

    output_dir = "output"
    import os
    os.makedirs(output_dir, exist_ok=True)

    output_filepath = os.path.join(output_dir, args.output)

    with open(output_filepath, 'w', encoding='utf-8') as outfile:
        outfile.writelines(final_output)
    print(f"\n📄 [DONE] Docs saved to: {output_filepath}")


if __name__ == "__main__":
    main()