from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class RelatedLink(BaseModel):
    url: str
    reason: str

class ContentAnalysisResponse(BaseModel):
    markdown_content: str = Field(description="Markdown formatted main content of the page.")
    related_links: List[RelatedLink] = Field(default=[], description="List of related links with reasons, ONLY from the main content.")
    related_links_reasoning: Dict[str, str] = Field(default={}, description="Reasons why each link is considered related.")
    suggested_filename: Optional[str] = Field(default=None, description="Suggested filename for the content.")