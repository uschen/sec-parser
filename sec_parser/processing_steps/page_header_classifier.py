from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sec_parser.processing_steps.abstract_classes.abstract_elementwise_processing_step import (
    AbstractElementwiseProcessingStep,
    ElementProcessingContext,
)
from sec_parser.semantic_elements.highlighted_text_element import (
    HighlightedTextElement,
    TextStyle,
)
from sec_parser.semantic_elements.semantic_elements import (
    PageHeaderElement,
    PageBreakElement,
)

from functools import reduce

if TYPE_CHECKING:  # pragma: no cover
    from sec_parser.semantic_elements.abstract_semantic_element import (
        AbstractSemanticElement,
    )


@dataclass(frozen=True)
class PageHeaderCandidate:
    TEXT_LENGTH_THRESHOLD = 100
    OCCURRENCE_THRESHOLD = 5
    MOST_COMMON_CANDIDATE_LIMIT = None
    text: str
    style: TextStyle | None


@dataclass(frozen=True)
class PageHeaderByDistanceToPagebreakCandidate:
    TEXT_LENGTH_THRESHOLD = 20
    DISTANCE_THRESHOLD = 5
    OCCURRENCE_THRESHOLD = 5
    MOST_COMMON_CANDIDATE_LIMIT = 5

    style: TextStyle
    distance_to_pre_page_break: int


class PageHeaderClassifier(AbstractElementwiseProcessingStep):
    _NUM_ITERATIONS = 2

    def __init__(
        self,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__(
            types_to_process=types_to_process,
            types_to_exclude=types_to_exclude,
        )
        self._element_to_page_header_candidate: dict[
            AbstractSemanticElement,
            PageHeaderCandidate,
        ] = {}
        self._candidate_count: Counter[PageHeaderCandidate] = Counter()
        self._most_common_candidates: dict[PageHeaderCandidate, int] | None = None

    def _process_element(
        self,
        element: AbstractSemanticElement,
        context: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        if context.iteration == 0:
            self._find_page_header_candidates(element)
            return element
        if context.iteration == 1:
            return self._classify_elements(element)
        msg = f"Invalid iteration: {context.iteration}"
        raise ValueError(msg)

    def _find_page_header_candidates(self, element: AbstractSemanticElement) -> None:
        if len(element.text) > PageHeaderCandidate.TEXT_LENGTH_THRESHOLD:
            return
        style = element.style if isinstance(element, HighlightedTextElement) else None
        candidate = PageHeaderCandidate(element.text, style)
        self._element_to_page_header_candidate[element] = candidate
        self._candidate_count[candidate] += 1

    def _classify_elements(
        self,
        element: AbstractSemanticElement,
    ) -> AbstractSemanticElement:
        most_common_candidates = self._get_most_common_candidates()
        if len(most_common_candidates) == 0:
            return element
        candidate = self._element_to_page_header_candidate.get(element)
        if candidate not in most_common_candidates:
            return element

        element.processing_log.add_item(
            message=f"Matches one of the most common candidates: {candidate}",
            log_origin=self.__class__.__name__,
        )
        return PageHeaderElement.create_from_element(
            element,
            log_origin=self.__class__.__name__,
        )

    def _get_most_common_candidates(self) -> dict[PageHeaderCandidate, int]:
        if self._most_common_candidates is None:
            self._most_common_candidates = {
                candidate: count
                for candidate, count in self._candidate_count.most_common(
                    PageHeaderCandidate.MOST_COMMON_CANDIDATE_LIMIT,
                )
                if count >= PageHeaderCandidate.OCCURRENCE_THRESHOLD
            }
        return self._most_common_candidates


class PageHeaderByDistanceToPagebreakClassifier(AbstractElementwiseProcessingStep):
    _NUM_ITERATIONS = 2

    def __init__(
        self,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__(
            types_to_process=types_to_process,
            types_to_exclude=types_to_exclude,
        )
        self._element_to_page_header_by_distance_candidate: dict[
            AbstractSemanticElement,
            PageHeaderByDistanceToPagebreakCandidate,
        ] = {}
        self._candidate_by_pagebreak_distance_count: Counter[
            PageHeaderByDistanceToPagebreakCandidate
        ] = Counter()

        self._most_common_by_pagebreak_candidates: (
            dict[PageHeaderByDistanceToPagebreakCandidate, int] | None
        ) = None

    def _process(
        self,
        elements: list[AbstractSemanticElement],
    ) -> list[AbstractSemanticElement]:
        def sum_if_page_break_element(res: int, e: AbstractSemanticElement) -> int:
            if isinstance(e, PageBreakElement):
                return res + 1
            return res

        page_break_count = reduce(sum_if_page_break_element, elements, 0)
        # print("page_break_count", page_break_count)
        for iteration in range(self._NUM_ITERATIONS):
            context = ElementProcessingContext(
                iteration=iteration,
                elements=elements,
            )
            context.page_break_count = page_break_count
            self._process_recursively(elements, _context=context, is_inner=False)
        return elements

    def _process_element(
        self,
        element: AbstractSemanticElement,
        context: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        if context.iteration == 0:
            self._find_distance_to_pagebreak_candidates(element, context)
            return element
        if context.iteration == 1:
            return self._classify_elements(element, context)
        msg = f"Invalid iteration: {context.iteration}"
        raise ValueError(msg)

    def _find_distance_to_pagebreak_candidates(
        self,
        element: AbstractSemanticElement,
        _context: ElementProcessingContext,
    ) -> None:
        if len(element.text) > PageHeaderCandidate.TEXT_LENGTH_THRESHOLD:
            return
        styles_metrics = element.html_tag.get_text_styles_metrics()
        style: TextStyle = TextStyle.from_style_and_text(styles_metrics, element.text)
        distance = _context.distant_to_previous_pagebreak_element(element=element)
        if distance is None:
            return
        if distance > PageHeaderByDistanceToPagebreakCandidate.DISTANCE_THRESHOLD:
            return
        candidate = PageHeaderByDistanceToPagebreakCandidate(style, distance)
        self._element_to_page_header_by_distance_candidate[element] = candidate
        self._candidate_by_pagebreak_distance_count[candidate] += 1

    def _classify_elements(
        self,
        element: AbstractSemanticElement,
        _context: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        most_common_candidates = self._get_most_common_candidates(_context)
        if len(most_common_candidates) == 0:
            return element
        candidate = self._element_to_page_header_by_distance_candidate.get(element)
        if candidate not in most_common_candidates:
            return element

        element.processing_log.add_item(
            message=f"Matches one of the most common by_distance candidates: {candidate}",
            log_origin=self.__class__.__name__,
        )

        # print("remove: ", "count", candidate, element.text)
        return PageHeaderElement.create_from_element(
            element,
            log_origin=self.__class__.__name__,
        )

    def _get_most_common_candidates(
        self,
        _context: ElementProcessingContext,
    ) -> dict[PageHeaderByDistanceToPagebreakCandidate, int]:
        def candidate_filter(count: int) -> bool:
            if count < PageHeaderByDistanceToPagebreakCandidate.OCCURRENCE_THRESHOLD:
                return False
            if _context.page_break_count is not None and _context.page_break_count > 0:
                return count / _context.page_break_count > 0.7

        if self._most_common_by_pagebreak_candidates is None:
            self._most_common_by_pagebreak_candidates = {
                candidate: count
                for candidate, count in self._candidate_by_pagebreak_distance_count.most_common(
                    PageHeaderByDistanceToPagebreakCandidate.MOST_COMMON_CANDIDATE_LIMIT,
                )
                if candidate_filter(count)
            }
        return self._most_common_by_pagebreak_candidates
