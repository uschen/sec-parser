"""
The semantic_elements subpackage provides abstractions
for meaningful units in SEC EDGAR documents. It converts
raw HTML elements into representations that carry
semantic significance.
"""

from sec_parser.semantic_elements.abstract_semantic_element import (
    AbstractLevelElement,
    AbstractSemanticElement,
    InvalidLevelError,
)
from sec_parser.semantic_elements.composite_semantic_element import (
    CompositeSemanticElement,
)
from sec_parser.semantic_elements.semantic_elements import (
    EmptyElement,
    ImageElement,
    IrrelevantElement,
    NotYetClassifiedElement,
    PageHeaderElement,
    PageNumberElement,
    SupplementaryText,
    TextElement,
)
from sec_parser.semantic_elements.highlighted_text_element import HighlightedTextElement
from sec_parser.semantic_elements.table_element.table_element import TableElement
from sec_parser.semantic_elements.table_element.table_of_contents_element import (
    TableOfContentsElement,
)
from sec_parser.semantic_elements.title_element import TitleElement
from sec_parser.semantic_elements.top_section_title import TopSectionTitle

__all__ = [
    "AbstractSemanticElement",
    "AbstractLevelElement",
    "NotYetClassifiedElement",
    "TopSectionTitle",
    "TextElement",
    "TitleElement",
    "InvalidLevelError",
    "IrrelevantElement",
    "ImageElement",
    "TableElement",
    "TableOfContentsElement",
    "EmptyElement",
    "CompositeSemanticElement",
    "SupplementaryText",
    "PageHeaderElement",
    "PageNumberElement",
    "HighlightedTextElement",
]
