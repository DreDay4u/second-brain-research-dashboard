"""
Test Layout Selector - Comprehensive tests for layout selection logic.

Tests rule-based selection, document type mapping, fallback logic,
and LLM-based selection with various content types.
"""

import asyncio
from content_analyzer import ContentAnalysis
from layout_selector import (
    select_layout,
    LayoutDecision,
    _apply_rule_based_selection,
    _get_layout_from_document_type,
    LAYOUT_MAPPINGS
)


def test_layout_decision_model():
    """Test LayoutDecision Pydantic model validation."""
    print("\n=== Test 1: LayoutDecision Model ===")

    # Test valid model
    decision = LayoutDecision(
        layout_type='instructional_layout',
        confidence=0.9,
        reasoning='Test reasoning',
        alternative_layouts=['data_layout', 'reference_layout'],
        component_suggestions=['CodeBlock', 'StepList']
    )

    print(f"✓ Layout Type: {decision.layout_type}")
    print(f"✓ Confidence: {decision.confidence}")
    print(f"✓ Reasoning: {decision.reasoning}")
    print(f"✓ Alternatives: {decision.alternative_layouts}")
    print(f"✓ Components: {decision.component_suggestions}")

    # Test confidence bounds
    try:
        invalid = LayoutDecision(
            layout_type='test',
            confidence=1.5,  # Invalid: > 1.0
            reasoning='Test'
        )
        print("✗ Confidence validation failed - should reject > 1.0")
    except ValueError:
        print("✓ Confidence validation working (rejects > 1.0)")

    print("\n✅ LayoutDecision model tests passed")


def test_rule_based_selection():
    """Test rule-based layout selection logic."""
    print("\n=== Test 2: Rule-Based Selection ===")

    # Test 1: Code-heavy content (>5 code blocks)
    print("\nTest 2.1: Code-heavy content")
    code_heavy = ContentAnalysis(
        title="Python Tutorial",
        document_type="tutorial",
        code_blocks=[{'language': 'python', 'code': 'print("hello")'}] * 6,
        tables=[],
        sections=['Intro', 'Setup', 'Code'],
        links=[],
        youtube_links=[],
        github_links=[]
    )
    decision = _apply_rule_based_selection(code_heavy)
    print(f"  Layout: {decision.layout_type if decision else 'None'}")
    print(f"  Confidence: {decision.confidence if decision else 'N/A'}")
    print(f"  Reasoning: {decision.reasoning if decision else 'N/A'}")
    assert decision is not None, "Should select instructional_layout"
    assert decision.layout_type == 'instructional_layout'
    assert decision.confidence >= 0.8
    print("  ✓ Correctly identified code-heavy content")

    # Test 2: Table-heavy content (>2 tables)
    print("\nTest 2.2: Table-heavy content")
    table_heavy = ContentAnalysis(
        title="Research Data",
        document_type="research",
        code_blocks=[],
        tables=[
            {'headers': ['A', 'B'], 'rows': [['1', '2']], 'row_count': 1},
            {'headers': ['C', 'D'], 'rows': [['3', '4']], 'row_count': 1},
            {'headers': ['E', 'F'], 'rows': [['5', '6']], 'row_count': 1}
        ],
        sections=['Abstract', 'Results'],
        links=[],
        youtube_links=[],
        github_links=[]
    )
    decision = _apply_rule_based_selection(table_heavy)
    print(f"  Layout: {decision.layout_type if decision else 'None'}")
    print(f"  Reasoning: {decision.reasoning if decision else 'N/A'}")
    assert decision is not None, "Should select data_layout"
    assert decision.layout_type == 'data_layout'
    print("  ✓ Correctly identified table-heavy content")

    # Test 3: Media-rich content (>3 media links)
    print("\nTest 2.3: Media-rich content")
    media_rich = ContentAnalysis(
        title="Video Overview",
        document_type="overview",
        code_blocks=[],
        tables=[],
        sections=['Intro', 'Videos'],
        links=['https://example.com'] * 5,
        youtube_links=['https://youtube.com/watch?v=abc123'] * 4,
        github_links=[]
    )
    decision = _apply_rule_based_selection(media_rich)
    print(f"  Layout: {decision.layout_type if decision else 'None'}")
    print(f"  Reasoning: {decision.reasoning if decision else 'N/A'}")
    assert decision is not None, "Should select media_layout"
    assert decision.layout_type == 'media_layout'
    print("  ✓ Correctly identified media-rich content")

    # Test 4: Section-heavy content (>10 sections)
    print("\nTest 2.4: Section-heavy content")
    section_heavy = ContentAnalysis(
        title="API Documentation",
        document_type="technical_doc",
        code_blocks=[],
        tables=[],
        sections=[f'Section {i}' for i in range(12)],
        links=[],
        youtube_links=[],
        github_links=[]
    )
    decision = _apply_rule_based_selection(section_heavy)
    print(f"  Layout: {decision.layout_type if decision else 'None'}")
    print(f"  Reasoning: {decision.reasoning if decision else 'N/A'}")
    assert decision is not None, "Should select reference_layout"
    assert decision.layout_type == 'reference_layout'
    print("  ✓ Correctly identified section-heavy content")

    # Test 5: No rules match (should return None)
    print("\nTest 2.5: No clear rule match")
    simple_content = ContentAnalysis(
        title="Simple Article",
        document_type="article",
        code_blocks=[],
        tables=[],
        sections=['Intro', 'Body', 'Conclusion'],
        links=['https://example.com'],
        youtube_links=[],
        github_links=[]
    )
    decision = _apply_rule_based_selection(simple_content)
    print(f"  Layout: {decision.layout_type if decision else 'None (expected)'}")
    assert decision is None, "Should return None for simple content"
    print("  ✓ Correctly returns None when no rule matches")

    print("\n✅ Rule-based selection tests passed")


def test_document_type_mapping():
    """Test document type to layout mapping."""
    print("\n=== Test 3: Document Type Mapping ===")

    # Test all mappings
    for doc_type, expected in LAYOUT_MAPPINGS.items():
        print(f"\nTest 3.{list(LAYOUT_MAPPINGS.keys()).index(doc_type) + 1}: {doc_type}")
        content = ContentAnalysis(
            title=f"Test {doc_type}",
            document_type=doc_type,
            code_blocks=[],
            tables=[],
            sections=['Section 1'],
            links=[],
            youtube_links=[],
            github_links=[]
        )
        decision = _get_layout_from_document_type(content)
        print(f"  Expected layout: {expected['layout']}")
        print(f"  Actual layout: {decision.layout_type}")
        print(f"  Components: {decision.component_suggestions}")
        assert decision.layout_type == expected['layout'], f"Should map {doc_type} to {expected['layout']}"
        assert set(decision.component_suggestions) == set(expected['components']), "Components should match"
        print(f"  ✓ Correctly mapped {doc_type} → {expected['layout']}")

    # Test unknown document type
    print("\nTest 3.8: Unknown document type")
    unknown = ContentAnalysis(
        title="Unknown Content",
        document_type="unknown_type",
        code_blocks=[],
        tables=[],
        sections=['Section 1'],
        links=[],
        youtube_links=[],
        github_links=[]
    )
    decision = _get_layout_from_document_type(unknown)
    print(f"  Layout: {decision.layout_type}")
    print(f"  Reasoning: {decision.reasoning}")
    assert decision.layout_type == 'summary_layout', "Should fallback to summary_layout"
    assert decision.confidence < 0.75, "Should have lower confidence for unknown type"
    print("  ✓ Correctly handles unknown document type")

    print("\n✅ Document type mapping tests passed")


async def test_select_layout_integration():
    """Test the main select_layout function integration."""
    print("\n=== Test 4: Select Layout Integration ===")

    # Test 1: High-confidence rule match (should skip LLM)
    print("\nTest 4.1: High-confidence rule match")
    code_heavy = ContentAnalysis(
        title="Python Tutorial",
        document_type="tutorial",
        code_blocks=[{'language': 'python', 'code': 'x = 1'}] * 7,
        tables=[],
        sections=['Intro', 'Setup'],
        links=[],
        youtube_links=[],
        github_links=[]
    )
    decision = await select_layout(code_heavy, agent=None)
    print(f"  Layout: {decision.layout_type}")
    print(f"  Confidence: {decision.confidence}")
    print(f"  Reasoning: {decision.reasoning}")
    assert decision.layout_type == 'instructional_layout'
    assert decision.confidence >= 0.85
    print("  ✓ High-confidence rule match works")

    # Test 2: Document type mapping (no strong rule)
    print("\nTest 4.2: Document type mapping")
    article = ContentAnalysis(
        title="News Article",
        document_type="article",
        code_blocks=[],
        tables=[],
        sections=['Headline', 'Body'],
        links=['https://example.com'],
        youtube_links=[],
        github_links=[]
    )
    decision = await select_layout(article, agent=None)
    print(f"  Layout: {decision.layout_type}")
    print(f"  Reasoning: {decision.reasoning}")
    assert decision.layout_type == 'news_layout'
    print("  ✓ Document type mapping works")

    # Test 3: Research content with tables
    print("\nTest 4.3: Research content")
    research = ContentAnalysis(
        title="Research Paper",
        document_type="research",
        code_blocks=[],
        tables=[{'headers': ['A'], 'rows': [['1']], 'row_count': 1}] * 3,
        sections=['Abstract', 'Methods', 'Results'],
        links=[],
        youtube_links=[],
        github_links=[]
    )
    decision = await select_layout(research, agent=None)
    print(f"  Layout: {decision.layout_type}")
    print(f"  Confidence: {decision.confidence}")
    assert decision.layout_type == 'data_layout'
    assert 'DataTable' in decision.component_suggestions
    print("  ✓ Research content correctly mapped")

    # Test 4: Technical documentation
    print("\nTest 4.4: Technical documentation")
    tech_doc = ContentAnalysis(
        title="API Reference",
        document_type="technical_doc",
        code_blocks=[{'language': 'python', 'code': 'api.call()'}],
        tables=[],
        sections=[f'Section {i}' for i in range(15)],
        links=[],
        youtube_links=[],
        github_links=[]
    )
    decision = await select_layout(tech_doc, agent=None)
    print(f"  Layout: {decision.layout_type}")
    print(f"  Components: {decision.component_suggestions[:3]}...")
    assert decision.layout_type == 'reference_layout'
    assert 'CodeBlock' in decision.component_suggestions
    print("  ✓ Technical documentation correctly mapped")

    # Test 5: Notes/summary content
    print("\nTest 4.5: Notes content")
    notes = ContentAnalysis(
        title="Quick Notes",
        document_type="notes",
        code_blocks=[],
        tables=[],
        sections=['Key Points', 'References'],
        links=['https://example.com'],
        youtube_links=[],
        github_links=[]
    )
    decision = await select_layout(notes, agent=None)
    print(f"  Layout: {decision.layout_type}")
    print(f"  Components: {decision.component_suggestions}")
    assert decision.layout_type == 'summary_layout'
    assert 'KeyPoints' in decision.component_suggestions
    print("  ✓ Notes content correctly mapped")

    print("\n✅ Select layout integration tests passed")


async def test_component_suggestions():
    """Test that component suggestions are appropriate for each layout."""
    print("\n=== Test 5: Component Suggestions ===")

    test_cases = [
        ('tutorial', 'instructional_layout', ['CodeBlock', 'StepList']),
        ('research', 'data_layout', ['DataTable', 'StatCard']),
        ('article', 'news_layout', ['Hero', 'ImageGallery']),
        ('guide', 'list_layout', ['OrderedList', 'Checklist']),
        ('notes', 'summary_layout', ['KeyPoints', 'TagCloud']),
        ('technical_doc', 'reference_layout', ['CodeBlock', 'ApiTable']),
        ('overview', 'media_layout', ['Hero', 'MediaEmbed'])
    ]

    for i, (doc_type, expected_layout, expected_components) in enumerate(test_cases, 1):
        print(f"\nTest 5.{i}: {doc_type}")
        content = ContentAnalysis(
            title=f"Test {doc_type}",
            document_type=doc_type,
            code_blocks=[],
            tables=[],
            sections=['Section 1'],
            links=[],
            youtube_links=[],
            github_links=[]
        )
        decision = await select_layout(content, agent=None)
        print(f"  Layout: {decision.layout_type}")
        print(f"  Components: {decision.component_suggestions}")

        assert decision.layout_type == expected_layout
        for component in expected_components:
            assert component in decision.component_suggestions, f"{component} should be suggested"
        print(f"  ✓ Correct components for {doc_type}")

    print("\n✅ Component suggestions tests passed")


async def test_fallback_logic():
    """Test fallback logic and edge cases."""
    print("\n=== Test 6: Fallback Logic ===")

    # Test 1: Empty content
    print("\nTest 6.1: Empty content")
    empty = ContentAnalysis(
        title="Empty Document",
        document_type="article",
        code_blocks=[],
        tables=[],
        sections=[],
        links=[],
        youtube_links=[],
        github_links=[]
    )
    decision = await select_layout(empty, agent=None)
    print(f"  Layout: {decision.layout_type}")
    print(f"  Confidence: {decision.confidence}")
    assert decision.layout_type in ['news_layout', 'summary_layout']
    print("  ✓ Handles empty content")

    # Test 2: Mixed signals (code + tables)
    print("\nTest 6.2: Mixed signals")
    mixed = ContentAnalysis(
        title="Mixed Content",
        document_type="guide",
        code_blocks=[{'language': 'python', 'code': 'x = 1'}] * 6,
        tables=[{'headers': ['A'], 'rows': [['1']], 'row_count': 1}] * 3,
        sections=['Section 1', 'Section 2'],
        links=[],
        youtube_links=[],
        github_links=[]
    )
    decision = await select_layout(mixed, agent=None)
    print(f"  Layout: {decision.layout_type}")
    print(f"  Confidence: {decision.confidence}")
    print(f"  Reasoning: {decision.reasoning}")
    # Should pick the first matching rule (code blocks in this case)
    assert decision.layout_type == 'instructional_layout'
    assert decision.confidence >= 0.8
    print("  ✓ Handles mixed signals with priority")

    # Test 3: Alternative layouts present
    print("\nTest 6.3: Alternative layouts")
    content = ContentAnalysis(
        title="Test",
        document_type="article",
        code_blocks=[],
        tables=[],
        sections=['Section 1'],
        links=[],
        youtube_links=[],
        github_links=[]
    )
    decision = await select_layout(content, agent=None)
    print(f"  Primary layout: {decision.layout_type}")
    print(f"  Alternatives: {decision.alternative_layouts}")
    assert len(decision.alternative_layouts) > 0, "Should have alternative layouts"
    assert decision.layout_type not in decision.alternative_layouts, "Primary should not be in alternatives"
    print("  ✓ Alternative layouts provided")

    print("\n✅ Fallback logic tests passed")


async def run_all_tests():
    """Run all layout selector tests."""
    print("=" * 60)
    print("LAYOUT SELECTOR TEST SUITE")
    print("=" * 60)

    try:
        # Test 1: Model validation
        test_layout_decision_model()

        # Test 2: Rule-based selection
        test_rule_based_selection()

        # Test 3: Document type mapping
        test_document_type_mapping()

        # Test 4: Integration tests
        await test_select_layout_integration()

        # Test 5: Component suggestions
        await test_component_suggestions()

        # Test 6: Fallback logic
        await test_fallback_logic()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(run_all_tests())
