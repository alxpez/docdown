import os
import re
import instructor
import google.generativeai as genai
from typing import Optional
from urllib.parse import urljoin
from models import ContentAnalysisResponse, RelatedLink
from prompts import ANALYZE_CONTENT_PROMPT, SUMMARIZE_CONTENT_PROMPT, SUGGEST_FILENAME_PROMPT
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("Error: Gemini API key not found. Please set GEMINI_API_KEY environment variable.")
    exit()

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
}

flash_model = instructor.from_gemini(
    client=genai.GenerativeModel(model_name="gemini-2.0-flash"),
    safety_settings=safety_settings,
    mode=instructor.Mode.GEMINI_JSON,
)

# mini_model = instructor.from_gemini(
#     client=genai.GenerativeModel(model_name="gemini-2.0-flash-lite-preview-02-05"),
#     safety_settings=safety_settings,
#     mode=instructor.Mode.GEMINI_JSON,
# )


def analyze_content_with_gemini(html_content, initial_url, initial_context=None, prompt_text=None) -> Optional[ContentAnalysisResponse]:
    """
    Analyzes HTML content using Gemini API and instructor to extract main content and related links,
    now considering the initial context.
    Returns a ContentAnalysisResponse object directly.
    """
    effective_prompt = prompt_text if prompt_text else ANALYZE_CONTENT_PROMPT
    context_section = f"Initial Page Topic Context: {initial_context}" if initial_context else "No initial context provided. Please infer context from the current page."
    final_prompt = effective_prompt.replace("{{initial_context}}", context_section).replace("{{initial_url}}", initial_url) + "\n\n" + html_content

    try:
        analysis_response = flash_model.messages.create(
            response_model=ContentAnalysisResponse,
            messages=[
                {"role": "system", "content": "You are a helpful documentation analysis tool focused on gathering content related to a specific initial documentation topic."},
                {"role": "user", "content": final_prompt},
            ],
        )

        absolute_related_links = []
        related_links_reasoning = {}
        for link_data in analysis_response.related_links:
            absolute_url = urljoin(initial_url, link_data.url)
            absolute_related_links.append(absolute_url)
            related_links_reasoning[absolute_url] = link_data.reason

        analysis_response.related_links = [RelatedLink(url=url, reason=analysis_response.related_links_reasoning[url]) for url in absolute_related_links]
        analysis_response.related_links_reasoning = related_links_reasoning

        return analysis_response

    except Exception as e:
        print(f"❌ [ERROR] analyzing content:\n{e}")
        return None


def summarize_content_with_gemini(content):
    """Summarizes content using Gemini API to get an initial context - now more detailed."""
    if not content:
        return "No content to summarize for initial context."

    prompt = SUMMARIZE_CONTENT_PROMPT.replace("{{content}}", content)
    prompt_parts = [prompt]

    try:
        response = flash_model.generate_content(prompt_parts)
        response.resolve()
        summary = response.text.strip()
        return summary
    except Exception as e:
        print(f"❌ [ERROR] summary generation:\n{e}")
        return "Error generating summary."


def suggest_filename_with_gemini(content):
    """Suggests a filename using Gemini API based on content."""
    if not content:
        return "documentation_summary"

    prompt = SUGGEST_FILENAME_PROMPT.replace("{{content}}", content)
    prompt_parts = [prompt]

    try:
        response = flash_model.generate_content(prompt_parts)
        response.resolve()
        filename = response.text.strip().replace(" ", "_")
        filename = re.sub(r'[^a-zA-Z0-9_]', '', filename)
        if not filename:
            return "documentation_summary"
        return filename
    except Exception as e:
        print(f"❌ [ERROR] Filename suggestion:\n{e}")
        return "documentation_summary"