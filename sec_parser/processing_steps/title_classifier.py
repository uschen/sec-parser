from __future__ import annotations

from typing import TYPE_CHECKING

from sec_parser.processing_steps.abstract_classes.abstract_elementwise_processing_step import (
    AbstractElementwiseProcessingStep,
    ElementProcessingContext,
)
from sec_parser.semantic_elements.highlighted_text_element import (
    HighlightedTextElement,
    TextStyle,
)
from sec_parser.semantic_elements.title_element import TitleElement

if TYPE_CHECKING:  # pragma: no cover
    from sec_parser.semantic_elements.abstract_semantic_element import (
        AbstractSemanticElement,
    )
from functools import cmp_to_key


def sort_text_style(x: TextStyle, y: TextStyle) -> int:
    ## Text larger is higher
    # if x._font_size - y._font_size != 0:
    #     return x._font_size - y._font_size
    if x.centered - y.centered != 0:
        return x.centered - y.centered
    if x.is_all_uppercase - y.is_all_uppercase != 0:
        return x.is_all_uppercase - y.is_all_uppercase
    if x.bold_with_font_weight - y.bold_with_font_weight != 0:
        return x.bold_with_font_weight - y.bold_with_font_weight
    return 0


class TitleClassifier(AbstractElementwiseProcessingStep):
    """
    TitleClassifier elements into TitleElement instances by scanning a list
    of semantic elements and replacing suitable candidates.

    The "_unique_styles_by_order" tuple:
    ====================================
    - Represents an ordered set of unique styles found in the document.
    - Preserves the order of insertion, which determines the hierarchical
      level of each style.
    - Assumes that earlier "highlight" styles correspond to higher level paragraph
      or section headings.
    """

    def __init__(
        self,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__(
            types_to_process=types_to_process,
            types_to_exclude=types_to_exclude,
        )

        self._unique_styles_by_order: dict[str, tuple[TextStyle, ...]] = {}

    def _add_unique_style(self, section_id: str, style: TextStyle) -> None:
        """Add a new unique style if not already present."""
        if not section_id in self._unique_styles_by_order:
            self._unique_styles_by_order[section_id] = ()
        if style not in self._unique_styles_by_order[section_id]:
            # if style.centered:
            #     self._unique_styles_by_order = tuple(
            #         dict.fromkeys([style, *self._unique_styles_by_order]).keys(),
            #     )
            # else:
            #     self._unique_styles_by_order = tuple(
            #         dict.fromkeys([*self._unique_styles_by_order, style]).keys(),
            #     )
            sorted_dict = tuple([*self._unique_styles_by_order[section_id], style])
            sorted_dict = sorted(
                sorted_dict,
                key=cmp_to_key(sort_text_style),
                reverse=True,
            )
            self._unique_styles_by_order[section_id] = sorted_dict
            # print(f"----{section_id}----")
            # for k in sorted_dict:
            #     print(k)
            # print(sorted_dict)
            # self._unique_styles_by_order = tuple(
            #     dict.fromkeys([*self._unique_styles_by_order, style]).keys(),
            # )

    def _process_element(
        self,
        element: AbstractSemanticElement,
        _context: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        """Process each element and convert to TitleElement if necessary."""
        if not isinstance(element, HighlightedTextElement):
            return element
        # print(element.style)
        # Ensure the style is tracked
        self._add_unique_style(_context.section_id, element.style)

        level = self._unique_styles_by_order[_context.section_id].index(element.style)
        return TitleElement.create_from_element(
            element,
            level=level + 1 if element.ix_continuation else level,
            log_origin=self.__class__.__name__,
        )
