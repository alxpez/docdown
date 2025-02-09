ANALYZE_CONTENT_PROMPT = """
Analyze the following HTML content from a documentation webpage.

Context from the initial page:
{{initial_context}}

---

Instructions:

1.  **Extract Main Documentation Content:** Identify and extract the core documentation content, focusing on highly relevant information in the context of the initial page's topic (described above). Exclude generic elements like site-wide navigation, headers, footers, sidebars, and advertisements, unless they are integral to the documentation itself.  Format the extracted content in Markdown, preserving headings, lists, code blocks, and other relevant formatting. **Ensure that any relative URLs within the main content are converted to absolute URLs using the base URL of the current page: {{initial_url}}.**

2.  **Identify Closely Related Documentation Links with Reasoning (FROM MAIN CONTENT ONLY):**  Carefully examine the hyperlinks **ONLY within the Main Documentation Content** you extracted in step 1.  Do **not** consider links from website headers, footers, sidebars, navigation menus, or any other areas outside of the main content.

    From these links within the main content, identify URLs that link to *other documentation pages within the *same website* that are *highly and directly related* to the *topic of the initial page* (described in the 'Context from the initial page' section). Focus on links that navigate to conceptually similar or immediately next/previous topics *within the scope of the initial page's topic*.

    For each related link you identify, provide a *brief reason* (one short sentence) explaining *why* you consider it closely related to the *initial page's topic* and why it's relevant *within the main documentation content*.

    Return the related links as a list of `RelatedLink` objects. Each `RelatedLink` object should have two fields: `url` and `reason`. The `url` should be the relative URL found in the HTML, and `reason` should be the sentence explaining the relevance to the *initial page's topic*.  Exclude any links that are not highly relevant documentation pages or are outside the scope of the initial page's topic (e.g., links to general site navigation, external sites, etc.).  **Ensure all identified related links are extracted solely from the Main Documentation Content.**

3.  **Suggest Filename:** Suggest a concise filename (without extension, and use underscores instead of spaces) suitable for a Markdown file that summarizes the documentation content.
"""

SUMMARIZE_CONTENT_PROMPT = """
Summarize the following documentation content to provide a broader and more specific context for identifying related documentation pages.

Specifically:
1.  Identify the **main topic** of the documentation content.
2.  List the **key sub-topics or themes** discussed in the content.
3.  Keep the summary concise, aiming for **2-3 sentences** that capture the essence and scope of the documentation.

Content to summarize:
---
{{content}}
---
Concise Summary (2-3 sentences):
"""

SUGGEST_FILENAME_PROMPT = "Suggest a concise filename (without extension, and use underscores instead of spaces) suitable for a Markdown file that summarizes the documentation content below:\n\n{{content}}"