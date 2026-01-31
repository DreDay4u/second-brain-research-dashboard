#!/usr/bin/env python3
"""
Demo script for summary component generators.

This script demonstrates all 4 summary generators with long-form content:
- TLDR
- KeyTakeaways
- ExecutiveSummary
- TableOfContents
"""

import json
from a2ui_generator import (
    generate_tldr,
    generate_key_takeaways,
    generate_executive_summary,
    generate_table_of_contents,
    reset_id_counter,
)


def demo_summary_generators():
    """Demonstrate all summary component generators with long-form content."""
    reset_id_counter()

    print("=" * 80)
    print("SUMMARY COMPONENT GENERATORS DEMO")
    print("=" * 80)
    print()

    # Generate TLDR
    print("1. TLDR (Too Long; Didn't Read)")
    print("-" * 80)
    tldr = generate_tldr(
        "AI market expected to reach $196B by 2030, driven by enterprise adoption, "
        "cloud infrastructure investments, and breakthrough innovations in transformer models."
    )
    print(f"Type: {tldr.type}")
    print(f"ID: {tldr.id}")
    print(f"Content: {tldr.props['content']}")
    print(f"Max Length: {tldr.props['maxLength']}")
    print()

    # Generate Key Takeaways
    print("2. Key Takeaways")
    print("-" * 80)
    takeaways = generate_key_takeaways(
        items=[
            "AI adoption increasing across all industries with 73% of Fortune 500 companies implementing solutions",
            "Cloud infrastructure critical for AI deployment enabling rapid scaling",
            "Data quality remains the biggest challenge requiring governance frameworks",
            "Pre-training on large corpora followed by fine-tuning is the dominant paradigm",
            "Transformer architecture revolutionized NLP through self-attention mechanisms"
        ],
        category="insights",
        icon="lightbulb"
    )
    print(f"Type: {takeaways.type}")
    print(f"ID: {takeaways.id}")
    print(f"Category: {takeaways.props['category']}")
    print(f"Icon: {takeaways.props['icon']}")
    print(f"Items ({len(takeaways.props['items'])}):")
    for i, item in enumerate(takeaways.props['items'], 1):
        print(f"  {i}. {item}")
    print()

    # Generate Executive Summary
    print("3. Executive Summary")
    print("-" * 80)
    exec_summary = generate_executive_summary(
        title="Annual AI Market Report 2024",
        summary=(
            "The AI market showed unprecedented growth in 2024, with enterprise adoption "
            "reaching 73% among Fortune 500 companies. Cloud infrastructure investments "
            "enabled rapid AI deployment, while data quality emerged as the primary challenge. "
            "Organizations invested heavily in building internal AI expertise and governance "
            "frameworks. Transformer architecture continued to revolutionize natural language "
            "processing through self-attention mechanisms, enabling parallel processing and "
            "outperforming traditional recurrent neural networks. Pre-training on massive text "
            "corpora followed by task-specific fine-tuning has become the dominant paradigm, "
            "achieving state-of-the-art results across benchmarks."
        ),
        key_metrics={
            "Market Size": "$196B",
            "Growth Rate": "+23%",
            "Enterprise Adoption": "73%",
            "Performance Gain": "+15%",
            "Training Speed": "3x faster"
        },
        recommendations=[
            "Invest in AI infrastructure and cloud capabilities",
            "Prioritize data quality initiatives and governance",
            "Build internal AI expertise through training programs",
            "Adopt transformer-based models for NLP tasks",
            "Implement robust monitoring and evaluation frameworks"
        ]
    )
    print(f"Type: {exec_summary.type}")
    print(f"ID: {exec_summary.id}")
    print(f"Title: {exec_summary.props['title']}")
    print(f"Summary Length: {len(exec_summary.props['summary'])} characters")
    print(f"Summary: {exec_summary.props['summary'][:200]}...")
    print(f"\nKey Metrics ({len(exec_summary.props['keyMetrics'])}):")
    for metric, value in exec_summary.props['keyMetrics'].items():
        print(f"  - {metric}: {value}")
    print(f"\nRecommendations ({len(exec_summary.props['recommendations'])}):")
    for i, rec in enumerate(exec_summary.props['recommendations'], 1):
        print(f"  {i}. {rec}")
    print()

    # Generate Table of Contents
    print("4. Table of Contents")
    print("-" * 80)
    toc = generate_table_of_contents(
        items=[
            {"title": "Executive Summary", "anchor": "exec-summary", "level": 0},

            {"title": "1. Introduction", "anchor": "introduction", "level": 0},
            {"title": "1.1 Background", "anchor": "background", "level": 1},
            {"title": "1.1.1 Historical Context", "anchor": "history", "level": 2},
            {"title": "1.1.2 Current State", "anchor": "current", "level": 2},
            {"title": "1.2 Objectives", "anchor": "objectives", "level": 1},

            {"title": "2. Market Overview", "anchor": "market-overview", "level": 0},
            {"title": "2.1 Market Size & Growth", "anchor": "market-size", "level": 1},
            {"title": "2.2 Key Trends", "anchor": "trends", "level": 1},
            {"title": "2.2.1 Enterprise Adoption", "anchor": "enterprise", "level": 2},
            {"title": "2.2.2 Technology Innovations", "anchor": "innovations", "level": 2},

            {"title": "3. Technical Analysis", "anchor": "technical", "level": 0},
            {"title": "3.1 Transformer Architecture", "anchor": "transformers", "level": 1},
            {"title": "3.1.1 Self-Attention Mechanism", "anchor": "attention", "level": 2},
            {"title": "3.1.2 Multi-Head Attention", "anchor": "multi-head", "level": 2},
            {"title": "3.2 Training Paradigms", "anchor": "training", "level": 1},
            {"title": "3.2.1 Pre-training", "anchor": "pretraining", "level": 2},
            {"title": "3.2.2 Fine-tuning", "anchor": "finetuning", "level": 2},

            {"title": "4. Challenges & Opportunities", "anchor": "challenges", "level": 0},
            {"title": "4.1 Data Quality", "anchor": "data-quality", "level": 1},
            {"title": "4.2 Infrastructure Requirements", "anchor": "infrastructure", "level": 1},
            {"title": "4.3 Governance & Ethics", "anchor": "governance", "level": 1},

            {"title": "5. Recommendations", "anchor": "recommendations", "level": 0},
            {"title": "6. Conclusion", "anchor": "conclusion", "level": 0},
        ],
        include_page_numbers=False
    )
    print(f"Type: {toc.type}")
    print(f"ID: {toc.id}")
    print(f"Include Page Numbers: {toc.props['includePageNumbers']}")
    print(f"Items ({len(toc.props['items'])}):")
    for item in toc.props['items']:
        indent = "  " * item['level']
        anchor = f" (#{item['anchor']})" if 'anchor' in item else ""
        print(f"{indent}- {item['title']}{anchor}")
    print()

    # Summary statistics
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"Total components generated: 4")
    print(f"  - TLDR: 1")
    print(f"  - KeyTakeaways: 1 (with {len(takeaways.props['items'])} items)")
    print(f"  - ExecutiveSummary: 1 (with {len(exec_summary.props['keyMetrics'])} metrics, "
          f"{len(exec_summary.props['recommendations'])} recommendations)")
    print(f"  - TableOfContents: 1 (with {len(toc.props['items'])} sections)")
    print()

    # Export as JSON
    components = [tldr, takeaways, exec_summary, toc]
    output = {
        "components": [comp.model_dump(exclude_none=True) for comp in components],
        "stats": {
            "total_components": len(components),
            "tldr_length": len(tldr.props['content']),
            "takeaways_count": len(takeaways.props['items']),
            "exec_summary_length": len(exec_summary.props['summary']),
            "toc_sections": len(toc.props['items']),
        }
    }

    print("JSON Output:")
    print("-" * 80)
    print(json.dumps(output, indent=2))
    print()

    return components


if __name__ == "__main__":
    components = demo_summary_generators()
    print(f"\n✅ Successfully generated {len(components)} summary components!")
