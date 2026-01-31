"""
Demo script for Tag & Badge Generators.

Demonstrates all 5 tag and badge component generators with various
configurations and use cases.
"""

import json
from a2ui_generator import (
    reset_id_counter,
    generate_tag,
    generate_badge,
    generate_category_tag,
    generate_status_indicator,
    generate_priority_badge,
)


def demo_tags():
    """Demonstrate tag component generation."""
    print("\n" + "="*70)
    print("TAG COMPONENT DEMOS")
    print("="*70)

    # Basic default tag
    tag1 = generate_tag(label="JavaScript")
    print("\n1. Basic Default Tag:")
    print(json.dumps(tag1.model_dump(), indent=2))

    # Primary tag with icon
    tag2 = generate_tag(
        label="Featured",
        type="primary",
        icon="star"
    )
    print("\n2. Primary Tag with Icon:")
    print(json.dumps(tag2.model_dump(), indent=2))

    # Success tag
    tag3 = generate_tag(
        label="Completed",
        type="success",
        icon="check"
    )
    print("\n3. Success Tag with Icon:")
    print(json.dumps(tag3.model_dump(), indent=2))

    # Removable tag
    tag4 = generate_tag(
        label="Filter: Python",
        type="info",
        removable=True
    )
    print("\n4. Removable Info Tag:")
    print(json.dumps(tag4.model_dump(), indent=2))

    # Warning tag
    tag5 = generate_tag(
        label="Deprecated",
        type="warning",
        icon="alert"
    )
    print("\n5. Warning Tag:")
    print(json.dumps(tag5.model_dump(), indent=2))

    # Error tag
    tag6 = generate_tag(
        label="Breaking Change",
        type="error"
    )
    print("\n6. Error Tag:")
    print(json.dumps(tag6.model_dump(), indent=2))


def demo_badges():
    """Demonstrate badge component generation."""
    print("\n" + "="*70)
    print("BADGE COMPONENT DEMOS")
    print("="*70)

    # Basic badge
    badge1 = generate_badge(label="Notifications", count=5)
    print("\n1. Basic Badge with Count:")
    print(json.dumps(badge1.model_dump(), indent=2))

    # Primary small badge
    badge2 = generate_badge(
        label="Unread",
        count=23,
        style="primary",
        size="small"
    )
    print("\n2. Primary Small Badge:")
    print(json.dumps(badge2.model_dump(), indent=2))

    # Warning badge
    badge3 = generate_badge(
        label="Pending",
        count=3,
        style="warning",
        size="medium"
    )
    print("\n3. Warning Badge:")
    print(json.dumps(badge3.model_dump(), indent=2))

    # Large success badge
    badge4 = generate_badge(
        label="Completed",
        count=100,
        style="success",
        size="large"
    )
    print("\n4. Large Success Badge:")
    print(json.dumps(badge4.model_dump(), indent=2))

    # Error badge
    badge5 = generate_badge(
        label="Failed",
        count=2,
        style="error"
    )
    print("\n5. Error Badge:")
    print(json.dumps(badge5.model_dump(), indent=2))

    # Zero count badge
    badge6 = generate_badge(
        label="Issues",
        count=0,
        style="success"
    )
    print("\n6. Zero Count Badge:")
    print(json.dumps(badge6.model_dump(), indent=2))


def demo_category_tags():
    """Demonstrate category tag component generation."""
    print("\n" + "="*70)
    print("CATEGORY TAG COMPONENT DEMOS")
    print("="*70)

    # Basic category tag
    cat1 = generate_category_tag(name="Technology")
    print("\n1. Basic Category Tag:")
    print(json.dumps(cat1.model_dump(), indent=2))

    # Category with semantic color
    cat2 = generate_category_tag(
        name="AI & ML",
        color="blue"
    )
    print("\n2. Category with Semantic Color:")
    print(json.dumps(cat2.model_dump(), indent=2))

    # Category with icon and color
    cat3 = generate_category_tag(
        name="Science",
        color="purple",
        icon="flask"
    )
    print("\n3. Category with Icon and Color:")
    print(json.dumps(cat3.model_dump(), indent=2))

    # Category with hex color
    cat4 = generate_category_tag(
        name="Business",
        color="#10B981"
    )
    print("\n4. Category with Hex Color:")
    print(json.dumps(cat4.model_dump(), indent=2))

    # Category with icon only
    cat5 = generate_category_tag(
        name="Education",
        icon="book"
    )
    print("\n5. Category with Icon Only:")
    print(json.dumps(cat5.model_dump(), indent=2))

    # Category with short hex color
    cat6 = generate_category_tag(
        name="Design",
        color="#F59",
        icon="palette"
    )
    print("\n6. Category with Short Hex Color:")
    print(json.dumps(cat6.model_dump(), indent=2))


def demo_status_indicators():
    """Demonstrate status indicator component generation."""
    print("\n" + "="*70)
    print("STATUS INDICATOR COMPONENT DEMOS")
    print("="*70)

    # Success status
    status1 = generate_status_indicator(status="success")
    print("\n1. Success Status (no label):")
    print(json.dumps(status1.model_dump(), indent=2))

    # Success with custom label
    status2 = generate_status_indicator(
        status="success",
        label="Deployment Complete"
    )
    print("\n2. Success with Custom Label:")
    print(json.dumps(status2.model_dump(), indent=2))

    # Warning status
    status3 = generate_status_indicator(
        status="warning",
        label="Maintenance Mode"
    )
    print("\n3. Warning Status:")
    print(json.dumps(status3.model_dump(), indent=2))

    # Error status
    status4 = generate_status_indicator(
        status="error",
        label="Connection Failed"
    )
    print("\n4. Error Status:")
    print(json.dumps(status4.model_dump(), indent=2))

    # Info status
    status5 = generate_status_indicator(
        status="info",
        label="Processing"
    )
    print("\n5. Info Status:")
    print(json.dumps(status5.model_dump(), indent=2))

    # Loading status
    status6 = generate_status_indicator(
        status="loading",
        label="Fetching data..."
    )
    print("\n6. Loading Status:")
    print(json.dumps(status6.model_dump(), indent=2))


def demo_priority_badges():
    """Demonstrate priority badge component generation."""
    print("\n" + "="*70)
    print("PRIORITY BADGE COMPONENT DEMOS")
    print("="*70)

    # Low priority
    priority1 = generate_priority_badge(level="low")
    print("\n1. Low Priority (no label):")
    print(json.dumps(priority1.model_dump(), indent=2))

    # Medium priority with custom label
    priority2 = generate_priority_badge(
        level="medium",
        label="Normal Priority"
    )
    print("\n2. Medium Priority with Label:")
    print(json.dumps(priority2.model_dump(), indent=2))

    # High priority
    priority3 = generate_priority_badge(
        level="high",
        label="Urgent"
    )
    print("\n3. High Priority:")
    print(json.dumps(priority3.model_dump(), indent=2))

    # Critical priority
    priority4 = generate_priority_badge(
        level="critical",
        label="Critical - Act Now"
    )
    print("\n4. Critical Priority:")
    print(json.dumps(priority4.model_dump(), indent=2))

    # Low priority with custom label
    priority5 = generate_priority_badge(
        level="low",
        label="Nice to Have"
    )
    print("\n5. Low Priority with Custom Label:")
    print(json.dumps(priority5.model_dump(), indent=2))

    # Medium priority default
    priority6 = generate_priority_badge(level="medium")
    print("\n6. Medium Priority (default):")
    print(json.dumps(priority6.model_dump(), indent=2))


def main():
    """Run all tag and badge demos."""
    reset_id_counter()

    print("\n" + "="*70)
    print("A2UI TAG & BADGE GENERATORS - COMPREHENSIVE DEMO")
    print("="*70)
    print("\nDemonstrating all 5 tag and badge generator functions:")
    print("1. generate_tag() - Basic tag/label components")
    print("2. generate_badge() - Badges with count indicators")
    print("3. generate_category_tag() - Category tags with colors/icons")
    print("4. generate_status_indicator() - Status badges")
    print("5. generate_priority_badge() - Priority level badges")

    demo_tags()
    demo_badges()
    demo_category_tags()
    demo_status_indicators()
    demo_priority_badges()

    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("\nAll tag and badge generators demonstrated successfully!")
    print("Total components shown: 30 across 5 generator types")


if __name__ == "__main__":
    main()
