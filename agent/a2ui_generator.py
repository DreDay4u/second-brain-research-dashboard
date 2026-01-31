"""
A2UI Generator Module - Base infrastructure for A2UI component generation.

This module provides foundational functions for generating A2UI (Agent-to-UI) components
that comply with the A2UI v0.8 protocol specification. It includes the base component model,
ID generation, component emission, and factory functions.

A2UI Protocol Compliance:
- All components must have: type, id, props
- Type format: "a2ui.ComponentName" (e.g., "a2ui.StatCard")
- IDs must be unique within a component tree
- Props are component-specific key-value pairs
- Optional children field for layout components
"""

import uuid
import json
from typing import Any, AsyncGenerator
from pydantic import BaseModel, Field, field_validator


class A2UIComponent(BaseModel):
    """
    Pydantic model for A2UI component specification.

    Represents a single UI component in the A2UI protocol format.
    All components must conform to this structure for proper rendering.

    Attributes:
        type: Component type identifier (e.g., "a2ui.StatCard", "a2ui.VideoCard")
        id: Unique identifier for this component instance
        props: Component-specific properties as a dictionary
        children: Optional list of child component IDs or nested structure for layouts

    Example:
        ```python
        component = A2UIComponent(
            type="a2ui.StatCard",
            id="stat-1",
            props={
                "value": "$196B",
                "label": "AI Market Size",
                "trend": "up",
                "trendValue": "+23%"
            }
        )
        ```
    """

    type: str = Field(
        description="A2UI component type (must start with 'a2ui.')",
        pattern=r"^a2ui\.[A-Z][a-zA-Z0-9]*$"
    )

    id: str = Field(
        description="Unique component identifier (kebab-case recommended)"
    )

    props: dict[str, Any] = Field(
        default_factory=dict,
        description="Component properties (component-specific)"
    )

    children: list[str] | dict[str, list[str]] | None = Field(
        default=None,
        description="Child component IDs (for layout components) or nested structure (for tabs/accordion)"
    )

    @field_validator('type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validate that type follows a2ui.ComponentName format."""
        if not v.startswith('a2ui.'):
            raise ValueError(f"Component type must start with 'a2ui.', got: {v}")
        return v

    @field_validator('id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate that ID is non-empty."""
        if not v or not v.strip():
            raise ValueError("Component ID cannot be empty")
        return v.strip()


# Component type registry - maps component types to validation rules
VALID_COMPONENT_TYPES = {
    # News & Trends
    "a2ui.HeadlineCard",
    "a2ui.TrendIndicator",
    "a2ui.TimelineEvent",
    "a2ui.NewsTicker",

    # Media
    "a2ui.VideoCard",
    "a2ui.ImageCard",
    "a2ui.PlaylistCard",
    "a2ui.PodcastCard",

    # Data & Statistics
    "a2ui.StatCard",
    "a2ui.MetricRow",
    "a2ui.ProgressRing",
    "a2ui.ComparisonBar",
    "a2ui.DataTable",
    "a2ui.MiniChart",

    # Lists & Rankings
    "a2ui.RankedItem",
    "a2ui.ChecklistItem",
    "a2ui.ProConItem",
    "a2ui.BulletPoint",

    # Resources & Links
    "a2ui.LinkCard",
    "a2ui.ToolCard",
    "a2ui.BookCard",
    "a2ui.RepoCard",

    # People & Entities
    "a2ui.ProfileCard",
    "a2ui.CompanyCard",
    "a2ui.QuoteCard",
    "a2ui.ExpertTip",

    # Summary & Overview
    "a2ui.TLDR",
    "a2ui.KeyTakeaways",
    "a2ui.ExecutiveSummary",
    "a2ui.TableOfContents",

    # Comparison
    "a2ui.ComparisonTable",
    "a2ui.VsCard",
    "a2ui.FeatureMatrix",
    "a2ui.PricingTable",

    # Instructional
    "a2ui.StepCard",
    "a2ui.CodeBlock",
    "a2ui.CalloutCard",
    "a2ui.CommandCard",

    # Layout
    "a2ui.Section",
    "a2ui.Grid",
    "a2ui.Columns",
    "a2ui.Tabs",
    "a2ui.Accordion",
    "a2ui.Carousel",
    "a2ui.Sidebar",

    # Tags & Categories
    "a2ui.TagCloud",
    "a2ui.CategoryBadge",
    "a2ui.DifficultyBadge",
}


# ID counter for sequential IDs within a session
_id_counter = 0


def generate_id(component_type: str, prefix: str | None = None) -> str:
    """
    Generate a unique component ID.

    Creates unique IDs using either a prefix-based counter or UUID fallback.
    IDs follow kebab-case convention for consistency.

    Strategies:
    1. If prefix provided: "{prefix}-{counter}" (e.g., "stat-1", "video-2")
    2. If no prefix: extract from component type + counter (e.g., "stat-card-1")
    3. Fallback: UUID4 for guaranteed uniqueness

    Args:
        component_type: A2UI component type (e.g., "a2ui.StatCard")
        prefix: Optional custom prefix for the ID (e.g., "stat", "video")

    Returns:
        Unique component ID string

    Examples:
        >>> generate_id("a2ui.StatCard", "stat")
        "stat-1"
        >>> generate_id("a2ui.VideoCard")
        "video-card-1"
        >>> generate_id("a2ui.Section", "intro")
        "intro-1"
    """
    global _id_counter
    _id_counter += 1

    if prefix:
        return f"{prefix}-{_id_counter}"

    # Extract component name from type (a2ui.StatCard -> stat-card)
    if component_type.startswith("a2ui."):
        # Convert PascalCase to kebab-case
        name = component_type[5:]  # Remove "a2ui."
        # Insert hyphens before capital letters and convert to lowercase
        kebab_name = ''.join(['-' + c.lower() if c.isupper() else c for c in name]).lstrip('-')
        return f"{kebab_name}-{_id_counter}"

    # Fallback to UUID
    return f"component-{uuid.uuid4().hex[:8]}"


def reset_id_counter():
    """
    Reset the global ID counter.

    Useful for testing or when starting a new component generation session.
    This ensures IDs start from 1 again.
    """
    global _id_counter
    _id_counter = 0


def generate_component(
    component_type: str,
    props: dict[str, Any],
    component_id: str | None = None,
    children: list[str] | dict[str, list[str]] | None = None
) -> A2UIComponent:
    """
    Generate a base A2UI component with validation.

    Factory function for creating A2UI components with automatic ID generation
    and type validation. Ensures all components conform to A2UI protocol.

    Args:
        component_type: A2UI component type (must be in VALID_COMPONENT_TYPES)
        props: Component properties dictionary
        component_id: Optional custom ID (auto-generated if not provided)
        children: Optional child component IDs for layout components

    Returns:
        A2UIComponent instance ready for emission

    Raises:
        ValueError: If component_type is not valid
        ValidationError: If props don't meet component requirements

    Examples:
        >>> component = generate_component(
        ...     "a2ui.StatCard",
        ...     {"value": "$196B", "label": "Market Size", "trend": "up"}
        ... )
        >>> component.type
        "a2ui.StatCard"
        >>> component.id
        "stat-card-1"
    """
    # Validate component type
    if component_type not in VALID_COMPONENT_TYPES:
        raise ValueError(
            f"Invalid component type: {component_type}. "
            f"Must be one of: {', '.join(sorted(VALID_COMPONENT_TYPES))}"
        )

    # Generate ID if not provided
    if component_id is None:
        component_id = generate_id(component_type)

    # Create and validate component
    component = A2UIComponent(
        type=component_type,
        id=component_id,
        props=props,
        children=children
    )

    return component


async def emit_components(
    components: list[A2UIComponent],
    stream_format: str = "ag-ui"
) -> AsyncGenerator[str, None]:
    """
    Emit A2UI components in AG-UI streaming format.

    Converts A2UI components to Server-Sent Events (SSE) format for streaming
    to the frontend via the AG-UI protocol. Each component is sent as a separate
    event with proper SSE formatting.

    AG-UI Protocol Format:
    - Each event starts with "data: "
    - JSON payload contains component definition
    - Events separated by double newlines
    - Compatible with EventSource API on frontend

    Args:
        components: List of A2UIComponent instances to emit
        stream_format: Output format ("ag-ui" for SSE, "json" for plain JSON)

    Yields:
        Formatted event strings ready for SSE streaming

    Examples:
        >>> components = [
        ...     generate_component("a2ui.StatCard", {"value": "100", "label": "Users"}),
        ...     generate_component("a2ui.StatCard", {"value": "50", "label": "Active"})
        ... ]
        >>> async for event in emit_components(components):
        ...     print(event)
        data: {"type": "a2ui.StatCard", "id": "stat-card-1", ...}

        data: {"type": "a2ui.StatCard", "id": "stat-card-2", ...}
    """
    for component in components:
        # Convert component to dict for JSON serialization
        component_dict = component.model_dump(exclude_none=True)

        if stream_format == "ag-ui":
            # AG-UI SSE format: "data: {json}\n\n"
            json_str = json.dumps(component_dict)
            yield f"data: {json_str}\n\n"
        elif stream_format == "json":
            # Plain JSON (for testing or alternative protocols)
            yield json.dumps(component_dict) + "\n"
        else:
            raise ValueError(f"Unknown stream format: {stream_format}")


def validate_component_props(component_type: str, props: dict[str, Any]) -> bool:
    """
    Validate that component props contain required fields.

    Basic validation for common component types. Checks that required
    properties are present in the props dictionary.

    Note: This is a basic validator. Full validation should be handled
    by component-specific generator functions.

    Args:
        component_type: A2UI component type
        props: Component properties to validate

    Returns:
        True if props are valid, raises ValueError otherwise

    Raises:
        ValueError: If required props are missing
    """
    # Define required props for common components
    required_props = {
        "a2ui.StatCard": ["value", "label"],
        "a2ui.VideoCard": ["videoId", "platform"],
        "a2ui.HeadlineCard": ["title"],
        "a2ui.RankedItem": ["rank", "title"],
        "a2ui.CodeBlock": ["code", "language"],
        "a2ui.Section": ["title"],
        "a2ui.Grid": ["columns"],
        "a2ui.TLDR": ["summary"],
    }

    if component_type in required_props:
        missing = [prop for prop in required_props[component_type] if prop not in props]
        if missing:
            raise ValueError(
                f"{component_type} missing required props: {', '.join(missing)}"
            )

    return True


# Helper function for bulk component generation
def generate_components_batch(
    component_specs: list[tuple[str, dict[str, Any]]]
) -> list[A2UIComponent]:
    """
    Generate multiple components from specifications.

    Convenience function for creating many components at once from a list
    of (type, props) tuples.

    Args:
        component_specs: List of (component_type, props) tuples

    Returns:
        List of generated A2UIComponent instances

    Examples:
        >>> specs = [
        ...     ("a2ui.StatCard", {"value": "100", "label": "Users"}),
        ...     ("a2ui.StatCard", {"value": "50", "label": "Active"}),
        ...     ("a2ui.VideoCard", {"videoId": "abc123", "platform": "youtube"})
        ... ]
        >>> components = generate_components_batch(specs)
        >>> len(components)
        3
    """
    components = []
    for component_type, props in component_specs:
        component = generate_component(component_type, props)
        components.append(component)
    return components


# Export public API
__all__ = [
    "A2UIComponent",
    "generate_id",
    "reset_id_counter",
    "generate_component",
    "emit_components",
    "validate_component_props",
    "generate_components_batch",
    "VALID_COMPONENT_TYPES",
]
