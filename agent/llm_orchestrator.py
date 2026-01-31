"""
LLM Orchestrator - Actual LLM-powered dashboard generation using OpenRouter.

This module replaces the heuristic-based orchestrate_dashboard with real LLM calls
using OpenRouter API to intelligently select and generate A2UI components based
on the content analysis.
"""

import os
import json
import re
from typing import AsyncGenerator
import httpx
from dotenv import load_dotenv

from a2ui_generator import (
    A2UIComponent,
    generate_component,
    generate_id,
    reset_id_counter,
    VALID_COMPONENT_TYPES,
    # Component generators
    generate_tldr,
    generate_key_takeaways,
    generate_stat_card,
    generate_code_block,
    generate_step_card,
    generate_callout_card,
    generate_video_card,
    generate_repo_card,
    generate_link_card,
    generate_data_table,
    generate_headline_card,
    generate_table_of_contents,
    generate_quote_card,
    generate_comparison_table,
    generate_checklist_item,
    generate_bullet_point,
    generate_section,
    generate_grid,
    generate_expert_tip,
    generate_tag,
    generate_badge,
)
from content_analyzer import parse_markdown, ContentAnalysis, _classify_heuristic
from prompts import (
    format_content_analysis_prompt,
    format_layout_selection_prompt,
    format_component_selection_prompt,
    validate_component_variety,
)

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-haiku-4.5")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


async def call_llm(prompt: str, system_prompt: str = "") -> str:
    """
    Call OpenRouter LLM API with the given prompt.

    Args:
        prompt: The user prompt to send
        system_prompt: Optional system prompt

    Returns:
        The LLM response text
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not set in environment")

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:3010",
                "X-Title": "Second Brain Research Dashboard",
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 4000,
            }
        )

        if response.status_code != 200:
            error_text = response.text
            print(f"[LLM ERROR] Status {response.status_code}: {error_text}")
            raise Exception(f"LLM API error: {response.status_code} - {error_text}")

        result = response.json()
        return result["choices"][0]["message"]["content"]


def extract_json_from_response(response: str) -> dict:
    """
    Extract JSON from LLM response, handling markdown code blocks.

    Args:
        response: Raw LLM response text

    Returns:
        Parsed JSON dictionary
    """
    # Try to find JSON in code blocks first
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', response)
    if json_match:
        json_str = json_match.group(1).strip()
    else:
        # Try to find raw JSON
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = response

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"[JSON PARSE ERROR] {e}")
        print(f"[RAW RESPONSE] {response[:500]}...")
        return {}


async def analyze_content_with_llm(markdown_content: str) -> dict:
    """
    Use LLM to analyze markdown content and classify it.

    Args:
        markdown_content: Raw markdown content

    Returns:
        Content analysis dictionary
    """
    system_prompt = """You are an expert content analyst. Analyze documents and return structured JSON.
Always respond with valid JSON only, no additional text."""

    prompt = format_content_analysis_prompt(markdown_content)

    print("[LLM] Analyzing content...")
    response = await call_llm(prompt, system_prompt)
    result = extract_json_from_response(response)

    # Provide defaults if parsing failed
    if not result:
        parsed = parse_markdown(markdown_content)
        result = {
            "document_type": _classify_heuristic(markdown_content, parsed),
            "title": parsed.get("title", "Untitled"),
            "entities": {"technologies": [], "tools": [], "languages": [], "concepts": []},
            "confidence": 0.5,
            "reasoning": "Fallback to heuristic analysis"
        }

    print(f"[LLM] Content analyzed: {result.get('document_type', 'unknown')}")
    return result


async def select_layout_with_llm(content_analysis: dict) -> dict:
    """
    Use LLM to select optimal layout based on content analysis.

    Args:
        content_analysis: Content analysis results

    Returns:
        Layout selection dictionary
    """
    system_prompt = """You are an expert UI/UX designer. Select optimal layouts and return structured JSON.
Always respond with valid JSON only, no additional text."""

    prompt = format_layout_selection_prompt(content_analysis)

    print("[LLM] Selecting layout...")
    response = await call_llm(prompt, system_prompt)
    result = extract_json_from_response(response)

    # Provide defaults if parsing failed
    if not result or "layout_type" not in result:
        result = {
            "layout_type": "summary_layout",
            "confidence": 0.5,
            "reasoning": "Default layout selection",
            "alternative_layouts": ["list_layout", "news_layout"],
            "component_suggestions": ["TLDR", "KeyTakeaways", "StatCard", "CalloutCard"]
        }

    print(f"[LLM] Layout selected: {result.get('layout_type', 'unknown')}")
    return result


async def select_components_with_llm(
    content_analysis: dict,
    layout_decision: dict,
    markdown_content: str
) -> list[dict]:
    """
    Use LLM to select and configure A2UI components.

    Args:
        content_analysis: Content analysis results
        layout_decision: Layout selection results
        markdown_content: Original markdown for context

    Returns:
        List of component specifications
    """
    system_prompt = """You are an expert A2UI component architect. Generate diverse dashboard components.
CRITICAL: You MUST return valid JSON with a "components" array containing component specifications.
Each component needs: component_type, priority, and props with actual data from the document.
Ensure variety: at least 4 different component types, never 3+ consecutive same type."""

    prompt = format_component_selection_prompt(content_analysis, layout_decision)

    # Add actual content snippets for the LLM to use
    prompt += f"""

## Actual Document Content (use this to populate component props)

{markdown_content[:3000]}

Remember: Extract REAL data from the document above to populate component props.
Return JSON with "components" array."""

    print("[LLM] Selecting components...")
    response = await call_llm(prompt, system_prompt)
    result = extract_json_from_response(response)

    components = result.get("components", [])

    if not components:
        print("[LLM] No components returned, using fallback")
        # Fallback components
        components = [
            {
                "component_type": "TLDR",
                "priority": "high",
                "props": {"content": content_analysis.get("title", "Document Summary"), "max_length": 200}
            },
            {
                "component_type": "KeyTakeaways",
                "priority": "high",
                "props": {"items": content_analysis.get("sections", ["Key point 1", "Key point 2"])[:5]}
            },
            {
                "component_type": "CalloutCard",
                "priority": "medium",
                "props": {"type": "info", "title": "About This Document", "content": f"Type: {content_analysis.get('document_type', 'article')}"}
            },
            {
                "component_type": "Badge",
                "priority": "low",
                "props": {"label": content_analysis.get("document_type", "article").title(), "count": 1}
            }
        ]

    # Validate variety
    variety = validate_component_variety(components)
    print(f"[LLM] Components selected: {len(components)}, unique types: {variety['unique_types_count']}")

    return components


def build_a2ui_component(spec: dict, content_analysis: dict) -> A2UIComponent | None:
    """
    Build an A2UIComponent from a specification dictionary.

    Args:
        spec: Component specification from LLM
        content_analysis: Content analysis for fallback data

    Returns:
        A2UIComponent instance or None if invalid
    """
    component_type = spec.get("component_type", "")
    props = spec.get("props", {})

    try:
        # Map component types to generator functions
        if component_type == "TLDR":
            content = props.get("content", "Summary of the document")
            if len(content) > 300:
                content = content[:297] + "..."
            return generate_tldr(content=content, max_length=props.get("max_length", 200))

        elif component_type == "KeyTakeaways":
            items = props.get("items", ["Key takeaway 1", "Key takeaway 2"])
            if not items:
                items = ["Key takeaway 1", "Key takeaway 2"]
            return generate_key_takeaways(items=items[:5])

        elif component_type == "StatCard":
            return generate_stat_card(
                title=props.get("label", props.get("title", "Metric")),
                value=str(props.get("value", "N/A")),
                change_type=props.get("trend", "neutral"),
                change_value=props.get("trendValue", props.get("change_value"))
            )

        elif component_type == "CodeBlock":
            code = props.get("code", "// Code example")
            if not code or not code.strip():
                return None
            return generate_code_block(
                code=code,
                language=props.get("language", "text")
            )

        elif component_type == "StepCard":
            return generate_step_card(
                step_number=props.get("step_number", props.get("number", 1)),
                title=props.get("title", "Step"),
                description=props.get("description", "Step description")
            )

        elif component_type == "CalloutCard":
            return generate_callout_card(
                type=props.get("type", "info"),
                title=props.get("title", "Note"),
                content=props.get("content", "Important information")
            )

        elif component_type == "VideoCard":
            video_url = props.get("video_url", props.get("url", ""))
            if not video_url:
                return None
            return generate_video_card(
                video_url=video_url,
                title=props.get("title", "Video"),
                description=props.get("description", "")
            )

        elif component_type == "RepoCard":
            return generate_repo_card(
                name=props.get("name", "Repository"),
                owner=props.get("owner"),
                repo_url=props.get("repo_url", props.get("url", "https://github.com"))
            )

        elif component_type == "LinkCard":
            url = props.get("url", "")
            if not url:
                return None
            return generate_link_card(
                url=url,
                title=props.get("title", "Resource")
            )

        elif component_type == "DataTable":
            headers = props.get("headers", ["Column 1", "Column 2"])
            rows = props.get("rows", [["Data 1", "Data 2"]])
            if not headers or not rows:
                return None
            return generate_data_table(headers=headers, rows=rows)

        elif component_type == "HeadlineCard":
            return generate_headline_card(
                headline=props.get("headline", props.get("title", "Headline")),
                subheadline=props.get("subheadline", props.get("subtitle")),
                source=props.get("source"),
                timestamp=props.get("timestamp")
            )

        elif component_type == "TableOfContents":
            items = props.get("items", [])
            if not items:
                sections = content_analysis.get("sections", [])
                items = [{"title": s, "anchor": f"#{s.lower().replace(' ', '-')}"} for s in sections[:8]]
            if not items:
                return None
            return generate_table_of_contents(items=items)

        elif component_type == "QuoteCard":
            return generate_quote_card(
                quote=props.get("quote", props.get("text", "Quote text")),
                author=props.get("author", "Unknown"),
                source=props.get("source")
            )

        elif component_type == "ChecklistItem":
            return generate_checklist_item(
                text=props.get("text", "Checklist item"),
                completed=props.get("completed", False)
            )

        elif component_type == "BulletPoint":
            return generate_bullet_point(
                text=props.get("text", "Bullet point")
            )

        elif component_type == "ExpertTip":
            return generate_expert_tip(
                tip=props.get("tip", props.get("content", "Expert tip")),
                expert=props.get("expert", props.get("author", "Expert")),
                category=props.get("category")
            )

        elif component_type == "Badge":
            return generate_badge(
                label=props.get("label", "Badge"),
                count=props.get("count", 1)
            )

        elif component_type == "Tag":
            return generate_tag(
                label=props.get("label", "Tag"),
                type=props.get("type", "default")
            )

        elif component_type == "Section":
            # Sections need special handling for children
            title = props.get("title", "Section")
            children = props.get("children", [])
            if not children:
                children = ["placeholder"]
            return generate_section(title=title, content=children)

        elif component_type == "ComparisonTable":
            items = props.get("items", [])
            features = props.get("features", [])
            if not items or not features:
                return None
            return generate_comparison_table(items=items, features=features)

        else:
            # Generic fallback - create a callout with the data
            print(f"[COMPONENT] Unknown type '{component_type}', using CalloutCard fallback")
            return generate_callout_card(
                type="info",
                title=component_type,
                content=json.dumps(props, indent=2)[:200] if props else "Component data"
            )

    except Exception as e:
        print(f"[COMPONENT ERROR] Failed to build {component_type}: {e}")
        return None


async def orchestrate_dashboard_with_llm(markdown_content: str) -> AsyncGenerator[A2UIComponent, None]:
    """
    Main orchestration function that uses LLM to generate dashboard components.

    This is the async generator version that yields components one at a time
    for streaming via SSE.

    Args:
        markdown_content: Raw markdown content to transform

    Yields:
        A2UIComponent instances
    """
    # Reset ID counter for fresh component IDs
    reset_id_counter()

    print("\n" + "="*60)
    print("[ORCHESTRATOR] Starting LLM-powered dashboard generation")
    print("="*60)

    # Step 1: Parse markdown structure (fast, no LLM)
    parsed = parse_markdown(markdown_content)
    print(f"[PARSE] Title: {parsed.get('title', 'Untitled')}")
    print(f"[PARSE] Sections: {len(parsed.get('sections', []))}")
    print(f"[PARSE] Code blocks: {len(parsed.get('code_blocks', []))}")

    # Step 2: Analyze content with LLM
    content_analysis = await analyze_content_with_llm(markdown_content)

    # Merge parsed data with LLM analysis
    full_analysis = {
        **content_analysis,
        "sections": parsed.get("sections", []),
        "code_blocks": parsed.get("code_blocks", []),
        "tables": parsed.get("tables", []),
        "links": parsed.get("all_links", []),
        "youtube_links": parsed.get("youtube_links", []),
        "github_links": parsed.get("github_links", []),
    }

    # Step 3: Select layout with LLM
    layout_decision = await select_layout_with_llm(full_analysis)

    # Step 4: Select components with LLM
    component_specs = await select_components_with_llm(
        full_analysis,
        layout_decision,
        markdown_content
    )

    # Step 5: Build and yield A2UI components
    print(f"\n[BUILD] Building {len(component_specs)} components...")

    components_built = 0
    component_types_used = set()

    for spec in component_specs:
        component = build_a2ui_component(spec, full_analysis)
        if component:
            components_built += 1
            component_types_used.add(component.type)
            print(f"[YIELD] Component {components_built}: {component.type} (id={component.id})")
            yield component

    print(f"\n[COMPLETE] Generated {components_built} components with {len(component_types_used)} unique types")
    print("="*60 + "\n")


async def orchestrate_dashboard_with_llm_list(markdown_content: str) -> list[A2UIComponent]:
    """
    Synchronous list version that collects all components.

    Args:
        markdown_content: Raw markdown content

    Returns:
        List of A2UIComponent instances
    """
    components = []
    async for component in orchestrate_dashboard_with_llm(markdown_content):
        components.append(component)
    return components
