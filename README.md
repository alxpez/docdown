# DocDown

DocDown is a customizable web scraper designed to extract documentation content from any webpage. It scrapes HTML content, processes related links, and generates clean Markdown output (intended for adding it as LLMs context). This project is aimed at personal use. 

There are a bunch of scrapers out there, this is just a dirty solution that covers my personal use-cases.
I look forward to include more customization for choosing models (for example using smaller local models), but for now it's practically free for personal use given Gemini API's great rate limits.

## Features

- **Web Scraping**: Extracts HTML content from a specified URL.
- **Gemini API Integration**: Uses Gemini API’s `flash_model` to:
  - Extract primary documentation content.
  - Identify and analyze related documentation links.
  - Suggest a meaningful output filename based on content.
  - Generate an initial context summary to guide related link analysis.
- **Markdown Output**: Converts extracted content into a structured Markdown file.
- **Related Link Crawling (Optional)**: Crawls and analyzes links related to the main content, with a configurable depth.
- **URL Normalization**: Converts relative URLs to absolute URLs for consistency.
- **Customization**: Offers options for custom prompts and output filenames.

## Setup

1. **Clone the Repository & Set Up Environment**
   ```bash
   git clone https://github.com/yourusername/DocDown.git
   cd DocDown
   ```

2. **Configure Environment Variables**
   ```bash
   mv .env.template .env
   ```
   > Edit the .env file and set your `GEMINI_API_KEY`.

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
> Ideally Use a virtual environment to keep your dependencies isolated

## Usage

Run the script from the command line with the starting URL as an argument:

```bash
python cli.py <URL> [options]
```

### Arguments

-   `<URL>`: The starting URL for scraping. **Required**.


### Options

-   `-r` or `--crawl-related`: Enable crawling of related content links.
-   `-d <depth>` or `--crawl-depth <depth>`:  Set maximum crawl depth for related links. (Default: 1).
-   `-p "<prompt>"` or `--prompt "<prompt>"`:  Use a custom prompt for Gemini content extraction and analysis.
-   `-o <filename>` or `--output <filename>`: Specify the output Markdown filename. If not provided, a suggested filename based on page content is used.

### Examples

1.  **Basic Scraping**

    ```bash
    python cli.py https://example.com/documentation/getting-started
    ```
    This will save the scraped content to `documentation_output.md`.

2.  **Crawl Related Links (Depth 2) with Custom Output**

    ```bash
    python cli.py https://example.com/documentation/main-page -r -d 2 -o my_docs.md
    ```
    Crawls related links up to 2 levels deep and saves output as `my_docs.md`.

3.  **Using a Custom Prompt**

    ```bash
    python cli.py https://example.com/api-reference -p "Extract API endpoint documentation and examples."
    ```

## Output

DocDown generates a Markdown file that includes:

- A title header derived from the page content or URL.
- Main documentation content formatted in Markdown.
- Horizontal separators (`---`) between content sections when multiple pages are processed.
- Absolute URLs for all links within the documentation.
- Optional filename suggestions based on the extracted content.

## Contributing
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

For major changes, please open an issue first to discuss what you would like to change.

## Known Limitations & Future Improvements
- Content Extraction: The quality of extraction is dependent on the Gemini API and the prompt used.
- HTML Variability: Extraction performance may vary with different website structures.
- Asynchronous Processing: Future enhancements may include asynchronous processing for better performance.
- Additional API Support: Plans to support local models and additional APIs for customization.

## License
MIT

## Notes
- Be sure to comply with website scraping policies (robots.txt) and terms of service.
- This project is provided "as is" without any warranties.