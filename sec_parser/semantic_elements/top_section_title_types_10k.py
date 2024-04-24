from dataclasses import dataclass
from sec_parser.semantic_elements.top_section_title_types import TopSectionType

# @dataclass(frozen=True)
# class TopSectionIn10K:
#     identifier: str
#     title: str
#     order: int
#     level: int = 0


InvalidTopSectionIn10K = TopSectionType(
    identifier="invalid",
    title="Invalid",
    order=-1,
    level=1,
)

ALL_10K_SECTIONS = (
    TopSectionType(
        identifier="part1",
        title="Financial Information",
        order=0,
        level=0,
    ),
    TopSectionType(
        identifier="part1item1",
        title="Financial Statements",
        order=1,
        level=1,
    ),
    TopSectionType(
        identifier="part1item1a",
        title="Risk Factors",
        order=2,
        level=1,
    ),
    TopSectionType(
        identifier="part1item1b",
        title="Risk Factors",
        order=3,
        level=1,
    ),
    TopSectionType(
        identifier="part1item1c",
        title="Cybersecurity",
        order=4,
        level=1,
    ),
    TopSectionType(
        identifier="part1item2",
        title="Properties",
        order=5,
        level=1,
    ),
    TopSectionType(
        identifier="part1item3",
        title="Legal Proceedings",
        order=6,
        level=1,
    ),
    TopSectionType(
        identifier="part1item4",
        title="Submission of Matters to a Vote",
        order=7,
        level=1,
    ),
    TopSectionType(
        identifier="part1item4a",
        title="Executive Officers of the Registrant",
        order=8,
        level=1,
    ),
    TopSectionType(
        identifier="part2",
        title="Other Information",
        order=9,
        level=0,
    ),
    TopSectionType(
        identifier="part2item5",
        title="Market for Registrant's Common Eqeuity, Related Stockholder Matters and Issuer Purchases of Equity Securities",
        order=10,
        level=1,
    ),
    TopSectionType(
        identifier="part2item6",
        title="Selected Financial Data",
        order=11,
        level=1,
    ),
    TopSectionType(
        identifier="part2item7",
        title="Management's Discussion and Analysis of Financial Condition and Results of Operations",
        order=12,
        level=1,
    ),
    TopSectionType(
        identifier="part2item7a",
        title="Quantitative and Qualitative Disclosures about Market Risk",
        order=13,
        level=1,
    ),
    TopSectionType(
        identifier="part2item8",
        title="Financial Statements and Supplementary Data",
        order=14,
        level=1,
    ),
    TopSectionType(
        identifier="part2item9",
        title="Changes in and Disagreements With Accountants on Accounting and Financial Disclosure",
        order=15,
        level=1,
    ),
    TopSectionType(
        identifier="part2item9a",
        title="Controls and Procedures",
        order=16,
        level=1,
    ),
    TopSectionType(
        identifier="part2item9b",
        title="Other Information",
        order=17,
        level=1,
    ),
    TopSectionType(
        identifier="part2item9c",
        title="Disclosure Regarding Foreign Jurisdictions that Prevent Inspections",
        order=18,
        level=1,
    ),
    TopSectionType(
        identifier="part3",
        title="Other Information",
        order=19,
        level=0,
    ),
    TopSectionType(
        identifier="part3item10",
        title="Directors and Executive Officers of the Registrant",
        order=20,
        level=1,
    ),
    TopSectionType(
        identifier="part3item11",
        title="Executive Compensation",
        order=21,
        level=1,
    ),
    TopSectionType(
        identifier="part3item12",
        title="Security Ownership of Certain Beneficial Owners and Management",
        order=22,
        level=1,
    ),
    TopSectionType(
        identifier="part3item13",
        title="Certain Relationships and Related Transactions",
        order=23,
        level=1,
    ),
    TopSectionType(
        identifier="part3item14",
        title="Principal Accountant Fees and Services",
        order=24,
        level=1,
    ),
    TopSectionType(
        identifier="part4",
        title="",
        order=25,
        level=0,
    ),
    TopSectionType(
        identifier="part4item15",
        title="Exhibit and Financial Statement Schedules.",
        order=26,
        level=1,
    ),
    TopSectionType(
        identifier="part4item16",
        title="Form 10-K Summary",
        order=27,
        level=1,
    ),
)

IDENTIFIER_TO_10K_SECTION = {
    section.identifier: section for section in ALL_10K_SECTIONS
}


TopSectionType = TopSectionType
