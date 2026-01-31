#!/usr/bin/env python3
"""
Variety Enforcement Demonstration

This script demonstrates variety enforcement rules with visual examples
of both valid and invalid component configurations.
"""

import json
from typing import List, Dict


def create_component(component_type: str, component_id: str) -> Dict:
    """Create a simple component specification."""
    return {
        'type': component_type,
        'id': component_id,
        'props': {}
    }


def validate_variety(components: List[Dict]) -> Dict:
    """
    Validate component variety (Python implementation matching TypeScript).

    Rules:
    1. Minimum 4 unique component types
    2. No more than 2 consecutive components of same type
    """
    if not components:
        return {
            'valid': False,
            'unique_types_count': 0,
            'max_consecutive_same_type': 0,
            'violations': ['No components provided']
        }

    # Count unique types
    component_types = [c['type'] for c in components]
    unique_types = set(component_types)
    unique_count = len(unique_types)

    # Find max consecutive
    max_consecutive = 1
    current_consecutive = 1

    for i in range(1, len(component_types)):
        if component_types[i] == component_types[i-1]:
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            current_consecutive = 1

    # Validation
    meets_min_types = unique_count >= 4
    meets_no_consecutive = max_consecutive <= 2

    violations = []
    if not meets_min_types:
        violations.append(f'Only {unique_count} unique type(s), minimum required is 4')
    if not meets_no_consecutive:
        violations.append(f'Found {max_consecutive} consecutive same type, maximum allowed is 2')

    # Component distribution
    distribution = {}
    for t in unique_types:
        distribution[t] = component_types.count(t)

    return {
        'valid': meets_min_types and meets_no_consecutive,
        'unique_types_count': unique_count,
        'max_consecutive_same_type': max_consecutive,
        'meets_min_types': meets_min_types,
        'meets_no_consecutive': meets_no_consecutive,
        'violations': violations,
        'component_type_distribution': distribution
    }


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def print_components(components: List[Dict]):
    """Print component list with visual indicators."""
    for i, comp in enumerate(components):
        # Check consecutive
        consecutive_marker = ""
        if i > 0 and comp['type'] == components[i-1]['type']:
            consecutive_marker = "  ← consecutive"
            if i > 1 and comp['type'] == components[i-2]['type']:
                consecutive_marker = "  ← 3+ consecutive ⚠️"

        print(f"  {i+1}. {comp['type']:<30} (id: {comp['id']}){consecutive_marker}")


def print_validation_result(result: Dict):
    """Print validation result with colors."""
    status = "✅ VALID" if result['valid'] else "❌ INVALID"
    print(f"\n{status}\n")

    print(f"Unique Types: {result['unique_types_count']} (min: 4) - ", end="")
    print("✅" if result['meets_min_types'] else "❌")

    print(f"Max Consecutive: {result['max_consecutive_same_type']} (max: 2) - ", end="")
    print("✅" if result['meets_no_consecutive'] else "❌")

    if result['violations']:
        print("\nViolations:")
        for v in result['violations']:
            print(f"  ⚠️  {v}")

    if 'component_type_distribution' in result:
        print("\nComponent Distribution:")
        for comp_type, count in sorted(result['component_type_distribution'].items(),
                                       key=lambda x: x[1], reverse=True):
            print(f"  {comp_type}: {count}")


def demo_valid_case_1():
    """Demo: Valid case with good variety."""
    print_section("Example 1: VALID - Good Variety (4+ types, no 3+ consecutive)")

    components = [
        create_component('a2ui.TLDR', 'tldr-1'),
        create_component('a2ui.StatCard', 'stat-1'),
        create_component('a2ui.HeadlineCard', 'headline-1'),
        create_component('a2ui.VideoCard', 'video-1'),
        create_component('a2ui.StatCard', 'stat-2'),
    ]

    print_components(components)
    result = validate_variety(components)
    print_validation_result(result)


def demo_valid_case_2():
    """Demo: Valid case with 2 consecutive allowed."""
    print_section("Example 2: VALID - 2 Consecutive Allowed")

    components = [
        create_component('a2ui.TLDR', 'tldr-1'),
        create_component('a2ui.StatCard', 'stat-1'),
        create_component('a2ui.StatCard', 'stat-2'),  # 2 consecutive - OK
        create_component('a2ui.HeadlineCard', 'headline-1'),
        create_component('a2ui.VideoCard', 'video-1'),
    ]

    print_components(components)
    result = validate_variety(components)
    print_validation_result(result)


def demo_invalid_insufficient_types():
    """Demo: Invalid - insufficient unique types."""
    print_section("Example 3: INVALID - Only 2 Unique Types (Need 4+)")

    components = [
        create_component('a2ui.StatCard', 's1'),
        create_component('a2ui.StatCard', 's2'),
        create_component('a2ui.HeadlineCard', 'h1'),
        create_component('a2ui.StatCard', 's3'),
    ]

    print_components(components)
    result = validate_variety(components)
    print_validation_result(result)


def demo_invalid_too_many_consecutive():
    """Demo: Invalid - too many consecutive."""
    print_section("Example 4: INVALID - 3 Consecutive Same Type")

    components = [
        create_component('a2ui.TLDR', 'tldr-1'),
        create_component('a2ui.StatCard', 's1'),
        create_component('a2ui.StatCard', 's2'),
        create_component('a2ui.StatCard', 's3'),  # 3rd consecutive - violation!
        create_component('a2ui.HeadlineCard', 'h1'),
        create_component('a2ui.VideoCard', 'v1'),
    ]

    print_components(components)
    result = validate_variety(components)
    print_validation_result(result)


def demo_invalid_both_violations():
    """Demo: Invalid - both rules violated."""
    print_section("Example 5: INVALID - Both Rules Violated")

    components = [
        create_component('a2ui.StatCard', 's1'),
        create_component('a2ui.StatCard', 's2'),
        create_component('a2ui.StatCard', 's3'),  # 3 consecutive
        create_component('a2ui.HeadlineCard', 'h1'),
        create_component('a2ui.StatCard', 's4'),
    ]

    print_components(components)
    result = validate_variety(components)
    print_validation_result(result)


def demo_excellent_variety():
    """Demo: Excellent variety with many types."""
    print_section("Example 6: EXCELLENT - High Variety (10 unique types)")

    components = [
        create_component('a2ui.TLDR', 'tldr-1'),
        create_component('a2ui.StatCard', 'stat-1'),
        create_component('a2ui.HeadlineCard', 'headline-1'),
        create_component('a2ui.VideoCard', 'video-1'),
        create_component('a2ui.ProfileCard', 'profile-1'),
        create_component('a2ui.CompanyCard', 'company-1'),
        create_component('a2ui.QuoteCard', 'quote-1'),
        create_component('a2ui.LinkCard', 'link-1'),
        create_component('a2ui.CodeBlock', 'code-1'),
        create_component('a2ui.TableOfContents', 'toc-1'),
    ]

    print_components(components)
    result = validate_variety(components)
    print_validation_result(result)


def demo_edge_case_boundary():
    """Demo: Edge case - exactly 4 types (boundary)."""
    print_section("Example 7: EDGE CASE - Exactly 4 Types (Boundary)")

    components = [
        create_component('a2ui.TLDR', 'tldr-1'),
        create_component('a2ui.StatCard', 'stat-1'),
        create_component('a2ui.HeadlineCard', 'headline-1'),
        create_component('a2ui.VideoCard', 'video-1'),
    ]

    print_components(components)
    result = validate_variety(components)
    print_validation_result(result)


def demo_real_world_research_paper():
    """Demo: Real-world research paper dashboard."""
    print_section("Example 8: REAL WORLD - Research Paper Dashboard")

    components = [
        create_component('a2ui.TLDR', 'tldr-ai-research'),
        create_component('a2ui.TableOfContents', 'toc-sections'),
        create_component('a2ui.StatCard', 'stat-accuracy'),
        create_component('a2ui.StatCard', 'stat-training-time'),
        create_component('a2ui.MiniChart', 'chart-convergence'),
        create_component('a2ui.KeyTakeaways', 'takeaways-findings'),
        create_component('a2ui.CodeBlock', 'code-optimizer'),
        create_component('a2ui.ComparisonTable', 'compare-algorithms'),
        create_component('a2ui.LinkCard', 'link-arxiv'),
    ]

    print("📊 AI Research Paper on Deep Learning Optimization\n")
    print_components(components)
    result = validate_variety(components)
    print_validation_result(result)


def demo_real_world_product_launch():
    """Demo: Real-world product launch dashboard."""
    print_section("Example 9: REAL WORLD - Product Launch Dashboard")

    components = [
        create_component('a2ui.ExecutiveSummary', 'exec-summary'),
        create_component('a2ui.StatCard', 'stat-revenue-goal'),
        create_component('a2ui.StatCard', 'stat-launch-budget'),
        create_component('a2ui.TimelineEvent', 'timeline-beta'),
        create_component('a2ui.TimelineEvent', 'timeline-launch'),
        create_component('a2ui.ProfileCard', 'profile-persona-it-director'),
        create_component('a2ui.ComparisonTable', 'pricing-tiers'),
        create_component('a2ui.DataTable', 'metrics-kpis'),
        create_component('a2ui.CalloutCard', 'callout-risks'),
    ]

    print("🚀 CloudSync Pro - Product Launch Plan\n")
    print_components(components)
    result = validate_variety(components)
    print_validation_result(result)


def print_summary():
    """Print summary of variety enforcement rules."""
    print_section("Variety Enforcement Rules Summary")

    print("Rule 1: Minimum Component Type Diversity")
    print("  • Requirement: At least 4 unique component types per dashboard")
    print("  • Rationale: Prevents monotonous single-dimension presentations")
    print("  • Example: ✅ TLDR, StatCard, HeadlineCard, VideoCard (4 types)")
    print("  • Example: ❌ StatCard, StatCard, HeadlineCard (only 2 types)\n")

    print("Rule 2: No Excessive Consecutive Repetition")
    print("  • Requirement: No more than 2 consecutive components of same type")
    print("  • Rationale: Prevents visual monotony and scanning fatigue")
    print("  • Example: ✅ StatCard, StatCard, HeadlineCard (2 consecutive OK)")
    print("  • Example: ❌ StatCard, StatCard, StatCard (3 consecutive violation!)\n")

    print("Benefits:")
    print("  ✓ More engaging dashboards")
    print("  ✓ Better information comprehension")
    print("  ✓ Professional, polished appearance")
    print("  ✓ Accommodates different learning styles")


def main():
    """Run all demonstrations."""
    print("\n" + "🎨 " * 40)
    print(" " * 20 + "VARIETY ENFORCEMENT DEMONSTRATION")
    print("🎨 " * 40 + "\n")

    print_summary()

    # Valid cases
    demo_valid_case_1()
    demo_valid_case_2()
    demo_excellent_variety()
    demo_edge_case_boundary()

    # Invalid cases
    demo_invalid_insufficient_types()
    demo_invalid_too_many_consecutive()
    demo_invalid_both_violations()

    # Real-world examples
    demo_real_world_research_paper()
    demo_real_world_product_launch()

    print_section("Demonstration Complete")
    print("✅ All examples demonstrated successfully!")
    print("\nFor more information, see:")
    print("  • Documentation: VARIETY_ENFORCEMENT_DOCUMENTATION.md")
    print("  • Test Suite: frontend/src/utils/__tests__/variety-enforcement.test.ts")
    print("  • Implementation: frontend/src/utils/variety-enforcement.ts\n")


if __name__ == '__main__':
    main()
