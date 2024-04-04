"""
The processing_steps subpackage provides a collection of steps
designed to work with parser engines from the parsing_engine
subpackage. These steps carry out specific tasks such as
section identification, title parsing, and text extraction, etc.
"""

from sec_parser.processing_steps.abstract_classes.abstract_elementwise_processing_step import (
    AbstractElementwiseProcessingStep,
)
from sec_parser.processing_steps.abstract_classes.abstract_processing_step import (
    AbstractProcessingStep,
)
from sec_parser.processing_steps.individual_semantic_element_extractor.text_element_premerger import (
    TextElementPreMerger,
)
from sec_parser.processing_steps.empty_element_classifier import EmptyElementClassifier
from sec_parser.processing_steps.image_classifier import ImageClassifier
from sec_parser.processing_steps.individual_semantic_element_extractor.individual_semantic_element_extractor import (
    IndividualSemanticElementExtractor,
)
from sec_parser.processing_steps.supplementary_text_classifier import (
    SupplementaryTextClassifier,
)
from sec_parser.processing_steps.table_classifier import TableClassifier
from sec_parser.processing_steps.text_classifier import TextClassifier
from sec_parser.processing_steps.title_classifier import TitleClassifier
from sec_parser.processing_steps.top_section_manager_for_10q import (
    TopSectionManagerFor10Q,
)
from sec_parser.processing_steps.top_section_manager_for_10k import (
    TopSectionManagerFor10K,
)

__all__ = [
    "AbstractProcessingStep",
    "AbstractElementwiseProcessingStep",
    "TextElementPreMerger",
    "TextClassifier",
    "TitleClassifier",
    "ImageClassifier",
    "TableClassifier",
    "IndividualSemanticElementExtractor",
    "SupplementaryTextClassifier",
    "EmptyElementClassifier",
    "TopSectionManagerFor10Q",
    "TopSectionManagerFor10K",
]
