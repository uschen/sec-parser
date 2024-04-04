from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, cast

from sec_parser.exceptions import SecParserValueError

from sec_parser.processing_engine.html_tag import HtmlTag
from sec_parser.processing_steps.abstract_classes.abstract_elementwise_processing_step import (
    AbstractElementwiseProcessingStep,
)

from sec_parser.semantic_elements.semantic_elements import (
    AbstractSemanticElement,
)
from sec_parser.utils.bs4_.without_tags import clone_without_children
from sec_parser.semantic_elements.highlighted_text_element import (
    TextStyle,
)

if TYPE_CHECKING:  # pragma: no cover
    from sec_parser.processing_steps.abstract_classes.processing_context import (
        ElementProcessingContext,
    )
    from sec_parser.processing_engine.processing_log import LogItemOrigin, ProcessingLog


class TextPreMergedElement(AbstractSemanticElement):
    """Lets treat it as irrelevant for now."""

    _original_element: AbstractSemanticElement

    def __init__(
        self,
        html_tag: HtmlTag,
        original_element: AbstractSemanticElement | None,
        *,
        processing_log: ProcessingLog | None = None,
        log_origin: LogItemOrigin | None = None,
    ) -> None:
        super().__init__(html_tag, processing_log=processing_log, log_origin=None)
        if not original_element:
            msg = "original_html_tag cannot be None or empty."
            raise SecParserValueError(msg)
        self._original_element = original_element
        self.log_init(log_origin)

    @classmethod
    def create_from_element(
        cls,
        html_tag: HtmlTag,
        log_origin: LogItemOrigin,
        *,
        original_element: AbstractSemanticElement | None = None,
    ) -> TextPreMergedElement:
        return cls(
            html_tag,
            log_origin=log_origin,
            processing_log=original_element.processing_log,
            original_element=original_element,
        )


class TextElementPreMerger(AbstractElementwiseProcessingStep):
    """
    TextElementPreMerger is a processing step that merges adjacent text elements
    For example, <div><span>a</span><span>b</span></div> will be merged into
    into a single TextElement(<div><span>ab</span><div>).
    """

    def __init__(
        self,
        *,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__(
            types_to_process=types_to_process,
            types_to_exclude=types_to_exclude,
        )

    def _process_element(
        self,
        element: AbstractSemanticElement,
        _: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        if not element.contains_words():
            return element
        if not element.html_tag.has_tag_children():
            return element

        # handle only has 2 <span> case for now
        span_tags: list[HtmlTag] = []
        for child in element.html_tag.get_children():
            if child.name == "span":
                span_tags.append(child)
            elif not child.has_spans_as_desendants():
                return element
        if len(element.html_tag.get_children()) <= 1:
            return element

        span_tags = [
            tag for tag in element.html_tag.find_tags("span") if len(tag.text) > 0
        ]

        # check if all the same style
        current_style_attr = None
        current_span_tag: HtmlTag = None
        for tag in span_tags:
            current_span_tag = tag
            styles_metrics = element.html_tag.get_text_styles_metrics()
            style: TextStyle = TextStyle.from_style_and_text(
                styles_metrics, element.text
            )
            # style_attr = tag._bs4.attrs.get("style")
            if current_style_attr is None:
                current_style_attr = style
                continue
            if current_style_attr != style:
                return element
        if current_span_tag is None:
            return element

        # TODO: find all text node then get their common styles
        # just use the first span's style
        text = element.html_tag.text
        # print("merged new element for ", text)
        # first_tag = clone_without_children(span_tags[0]._bs4)
        first_tag = clone_without_children(current_span_tag._bs4)
        first_tag.string = text
        parent = clone_without_children(element.html_tag._bs4)
        parent.append(first_tag)
        new_element = TextPreMergedElement.create_from_element(
            HtmlTag(parent),
            log_origin=self.__class__.__name__,
            original_element=element,
        )
        return new_element
