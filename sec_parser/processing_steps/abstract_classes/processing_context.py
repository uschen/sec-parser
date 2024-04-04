from dataclasses import dataclass

from sec_parser.semantic_elements.semantic_elements import (
    AbstractSemanticElement,
    PageBreakElement,
)


@dataclass
class ElementProcessingContext:
    """
    The ElementProcessingContext class is designed to provide context information
    for elementwise processing steps.
    """

    iteration: int
    elements: list[AbstractSemanticElement]

    element_index: int = None
    section_id: str = None

    def distant_to_previous_pagebreak_element(
        self, element: AbstractSemanticElement
    ) -> int | None:
        if not self.element_index:
            return
        if self.element_index == 0:
            return None
        for x in range(self.element_index - 1, 0, -1):
            if isinstance(self.elements[x], PageBreakElement):
                return self.element_index - x
        return None
