"""
Tests for A2UI Generator Module.

Comprehensive test suite for a2ui_generator.py covering:
- A2UIComponent model validation
- ID generation and uniqueness
- Component generation functions
- Component emission to AG-UI format
- Error handling for invalid types
- Batch component generation
"""

import pytest
import json
from pydantic import ValidationError
from a2ui_generator import (
    A2UIComponent,
    generate_id,
    reset_id_counter,
    generate_component,
    emit_components,
    validate_component_props,
    generate_components_batch,
    VALID_COMPONENT_TYPES,
)


class TestA2UIComponentModel:
    """Test suite for A2UIComponent Pydantic model."""

    def test_valid_component_creation(self):
        """Test creating a valid A2UI component."""
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

        assert component.type == "a2ui.StatCard"
        assert component.id == "stat-1"
        assert component.props["value"] == "$196B"
        assert component.props["label"] == "AI Market Size"
        assert component.children is None

    def test_component_with_children(self):
        """Test creating a component with children (layout component)."""
        component = A2UIComponent(
            type="a2ui.Section",
            id="section-1",
            props={"title": "Overview"},
            children=["stat-1", "stat-2", "video-1"]
        )

        assert component.type == "a2ui.Section"
        assert component.children == ["stat-1", "stat-2", "video-1"]

    def test_component_with_nested_children(self):
        """Test creating a component with nested children structure (Tabs/Accordion)."""
        component = A2UIComponent(
            type="a2ui.Tabs",
            id="tabs-1",
            props={
                "tabs": [
                    {"id": "overview", "label": "Overview"},
                    {"id": "details", "label": "Details"}
                ]
            },
            children={
                "overview": ["summary-1"],
                "details": ["table-1", "chart-1"]
            }
        )

        assert component.type == "a2ui.Tabs"
        assert isinstance(component.children, dict)
        assert component.children["overview"] == ["summary-1"]
        assert component.children["details"] == ["table-1", "chart-1"]

    def test_invalid_component_type_format(self):
        """Test that component type must start with 'a2ui.'"""
        with pytest.raises(ValidationError) as exc_info:
            A2UIComponent(
                type="StatCard",  # Missing "a2ui." prefix
                id="stat-1",
                props={"value": "100"}
            )

        # Check that validation error occurred for the type field
        assert "type" in str(exc_info.value)
        assert "pattern" in str(exc_info.value).lower()

    def test_invalid_component_type_pattern(self):
        """Test that component type must follow PascalCase after 'a2ui.'"""
        with pytest.raises(ValidationError):
            A2UIComponent(
                type="a2ui.stat_card",  # Should be PascalCase
                id="stat-1",
                props={"value": "100"}
            )

    def test_empty_id_validation(self):
        """Test that component ID cannot be empty."""
        with pytest.raises(ValidationError) as exc_info:
            A2UIComponent(
                type="a2ui.StatCard",
                id="",
                props={"value": "100"}
            )

        assert "cannot be empty" in str(exc_info.value)

    def test_component_serialization(self):
        """Test that component can be serialized to dict/JSON."""
        component = A2UIComponent(
            type="a2ui.VideoCard",
            id="video-1",
            props={
                "videoId": "dQw4w9WgXcQ",
                "platform": "youtube",
                "title": "Demo Video"
            }
        )

        # Serialize to dict
        component_dict = component.model_dump()
        assert component_dict["type"] == "a2ui.VideoCard"
        assert component_dict["id"] == "video-1"
        assert component_dict["props"]["videoId"] == "dQw4w9WgXcQ"

        # Serialize to JSON
        json_str = component.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["type"] == "a2ui.VideoCard"

    def test_component_exclude_none(self):
        """Test that None values can be excluded from serialization."""
        component = A2UIComponent(
            type="a2ui.StatCard",
            id="stat-1",
            props={"value": "100"}
        )

        # Exclude None values (children should not be in output)
        component_dict = component.model_dump(exclude_none=True)
        assert "children" not in component_dict


class TestGenerateID:
    """Test suite for generate_id() function."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_generate_id_with_prefix(self):
        """Test ID generation with custom prefix."""
        id1 = generate_id("a2ui.StatCard", prefix="stat")
        id2 = generate_id("a2ui.StatCard", prefix="stat")
        id3 = generate_id("a2ui.VideoCard", prefix="video")

        assert id1 == "stat-1"
        assert id2 == "stat-2"
        assert id3 == "video-3"

    def test_generate_id_without_prefix(self):
        """Test ID generation without prefix (extracts from component type)."""
        id1 = generate_id("a2ui.StatCard")
        id2 = generate_id("a2ui.VideoCard")
        id3 = generate_id("a2ui.HeadlineCard")

        assert id1 == "stat-card-1"
        assert id2 == "video-card-2"
        assert id3 == "headline-card-3"

    def test_generate_id_pascal_to_kebab(self):
        """Test PascalCase to kebab-case conversion."""
        reset_id_counter()

        id1 = generate_id("a2ui.TLDR")
        id2 = generate_id("a2ui.ExecutiveSummary")
        id3 = generate_id("a2ui.TableOfContents")

        assert id1 == "t-l-d-r-1"
        assert id2 == "executive-summary-2"
        assert id3 == "table-of-contents-3"

    def test_id_uniqueness(self):
        """Test that generated IDs are unique."""
        ids = set()
        for i in range(100):
            new_id = generate_id("a2ui.StatCard", prefix="stat")
            assert new_id not in ids
            ids.add(new_id)

        assert len(ids) == 100

    def test_reset_id_counter(self):
        """Test that reset_id_counter() resets the counter."""
        id1 = generate_id("a2ui.StatCard", prefix="stat")
        assert id1 == "stat-1"

        id2 = generate_id("a2ui.StatCard", prefix="stat")
        assert id2 == "stat-2"

        reset_id_counter()

        id3 = generate_id("a2ui.StatCard", prefix="stat")
        assert id3 == "stat-1"  # Counter reset


class TestGenerateComponent:
    """Test suite for generate_component() function."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_generate_valid_component(self):
        """Test generating a valid component."""
        component = generate_component(
            "a2ui.StatCard",
            props={"value": "$196B", "label": "Market Size", "trend": "up"}
        )

        assert isinstance(component, A2UIComponent)
        assert component.type == "a2ui.StatCard"
        assert component.id == "stat-card-1"
        assert component.props["value"] == "$196B"

    def test_generate_component_with_custom_id(self):
        """Test generating component with custom ID."""
        component = generate_component(
            "a2ui.VideoCard",
            props={"videoId": "abc123", "platform": "youtube"},
            component_id="custom-video-1"
        )

        assert component.id == "custom-video-1"

    def test_generate_component_with_children(self):
        """Test generating layout component with children."""
        component = generate_component(
            "a2ui.Section",
            props={"title": "Overview"},
            children=["stat-1", "stat-2"]
        )

        assert component.children == ["stat-1", "stat-2"]

    def test_generate_component_invalid_type(self):
        """Test that invalid component type raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            generate_component(
                "a2ui.InvalidComponent",
                props={"value": "test"}
            )

        assert "Invalid component type" in str(exc_info.value)
        assert "a2ui.InvalidComponent" in str(exc_info.value)

    def test_generate_component_auto_id_generation(self):
        """Test that components get sequential auto-generated IDs."""
        c1 = generate_component("a2ui.StatCard", props={"value": "1"})
        c2 = generate_component("a2ui.StatCard", props={"value": "2"})
        c3 = generate_component("a2ui.VideoCard", props={"videoId": "123", "platform": "youtube"})

        assert c1.id == "stat-card-1"
        assert c2.id == "stat-card-2"
        assert c3.id == "video-card-3"


class TestEmitComponents:
    """Test suite for emit_components() async function."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    @pytest.mark.asyncio
    async def test_emit_components_ag_ui_format(self):
        """Test emitting components in AG-UI SSE format."""
        components = [
            generate_component("a2ui.StatCard", props={"value": "100", "label": "Users"}),
            generate_component("a2ui.StatCard", props={"value": "50", "label": "Active"}),
        ]

        events = []
        async for event in emit_components(components, stream_format="ag-ui"):
            events.append(event)

        assert len(events) == 2
        assert events[0].startswith("data: ")
        assert events[0].endswith("\n\n")

        # Parse the JSON from the event
        json_str = events[0].replace("data: ", "").strip()
        data = json.loads(json_str)
        assert data["type"] == "a2ui.StatCard"
        assert data["id"] == "stat-card-1"
        assert data["props"]["value"] == "100"

    @pytest.mark.asyncio
    async def test_emit_components_json_format(self):
        """Test emitting components in plain JSON format."""
        components = [
            generate_component("a2ui.VideoCard", props={"videoId": "abc123", "platform": "youtube"}),
        ]

        events = []
        async for event in emit_components(components, stream_format="json"):
            events.append(event)

        assert len(events) == 1
        assert not event.startswith("data: ")  # No SSE formatting

        data = json.loads(events[0])
        assert data["type"] == "a2ui.VideoCard"
        assert data["props"]["videoId"] == "abc123"

    @pytest.mark.asyncio
    async def test_emit_components_invalid_format(self):
        """Test that invalid stream format raises ValueError."""
        components = [
            generate_component("a2ui.StatCard", props={"value": "100", "label": "Test"}),
        ]

        with pytest.raises(ValueError) as exc_info:
            async for event in emit_components(components, stream_format="invalid"):
                pass

        assert "Unknown stream format" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_emit_empty_components_list(self):
        """Test emitting empty list of components."""
        events = []
        async for event in emit_components([]):
            events.append(event)

        assert len(events) == 0

    @pytest.mark.asyncio
    async def test_emit_components_exclude_none(self):
        """Test that None values are excluded from emitted JSON."""
        component = generate_component(
            "a2ui.StatCard",
            props={"value": "100", "label": "Test"}
        )

        events = []
        async for event in emit_components([component]):
            events.append(event)

        json_str = events[0].replace("data: ", "").strip()
        data = json.loads(json_str)

        # children field should not be present (it's None)
        assert "children" not in data


class TestValidateComponentProps:
    """Test suite for validate_component_props() function."""

    def test_validate_stat_card_props(self):
        """Test validation of StatCard required props."""
        # Valid props
        assert validate_component_props(
            "a2ui.StatCard",
            {"value": "100", "label": "Users", "trend": "up"}
        ) is True

        # Missing required prop
        with pytest.raises(ValueError) as exc_info:
            validate_component_props("a2ui.StatCard", {"value": "100"})

        assert "missing required props" in str(exc_info.value)
        assert "label" in str(exc_info.value)

    def test_validate_video_card_props(self):
        """Test validation of VideoCard required props."""
        # Valid props
        assert validate_component_props(
            "a2ui.VideoCard",
            {"videoId": "abc123", "platform": "youtube", "title": "Demo"}
        ) is True

        # Missing required props
        with pytest.raises(ValueError) as exc_info:
            validate_component_props("a2ui.VideoCard", {"title": "Demo"})

        assert "videoId" in str(exc_info.value) or "platform" in str(exc_info.value)

    def test_validate_unknown_component_type(self):
        """Test validation of component type without required props defined."""
        # Should pass - no validation rules for this type
        assert validate_component_props(
            "a2ui.CustomComponent",
            {"any": "props"}
        ) is True


class TestGenerateComponentsBatch:
    """Test suite for generate_components_batch() function."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_batch_generation(self):
        """Test generating multiple components in batch."""
        specs = [
            ("a2ui.StatCard", {"value": "100", "label": "Users"}),
            ("a2ui.StatCard", {"value": "50", "label": "Active"}),
            ("a2ui.VideoCard", {"videoId": "abc123", "platform": "youtube"}),
        ]

        components = generate_components_batch(specs)

        assert len(components) == 3
        assert components[0].type == "a2ui.StatCard"
        assert components[0].id == "stat-card-1"
        assert components[1].type == "a2ui.StatCard"
        assert components[1].id == "stat-card-2"
        assert components[2].type == "a2ui.VideoCard"
        assert components[2].id == "video-card-3"

    def test_batch_generation_empty_list(self):
        """Test batch generation with empty list."""
        components = generate_components_batch([])
        assert len(components) == 0

    def test_batch_generation_invalid_type(self):
        """Test that batch generation raises error for invalid type."""
        specs = [
            ("a2ui.StatCard", {"value": "100", "label": "Users"}),
            ("a2ui.InvalidType", {"value": "test"}),
        ]

        with pytest.raises(ValueError):
            generate_components_batch(specs)


class TestComponentTypeRegistry:
    """Test suite for VALID_COMPONENT_TYPES registry."""

    def test_all_categories_present(self):
        """Test that all component categories are registered."""
        # Check for presence of components from each category
        categories = {
            "news": "a2ui.HeadlineCard",
            "media": "a2ui.VideoCard",
            "data": "a2ui.StatCard",
            "lists": "a2ui.RankedItem",
            "resources": "a2ui.LinkCard",
            "people": "a2ui.ProfileCard",
            "summary": "a2ui.TLDR",
            "comparison": "a2ui.ComparisonTable",
            "instructional": "a2ui.CodeBlock",
            "layout": "a2ui.Section",
            "tags": "a2ui.TagCloud",
        }

        for category, component_type in categories.items():
            assert component_type in VALID_COMPONENT_TYPES, f"Missing {category} component: {component_type}"

    def test_component_count(self):
        """Test that we have all expected component types."""
        # Based on app_spec.txt, we should have 40+ components
        assert len(VALID_COMPONENT_TYPES) >= 40


class TestIntegration:
    """Integration tests for complete component generation workflow."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """Test complete workflow from generation to emission."""
        # Step 1: Generate components
        components = [
            generate_component("a2ui.TLDR", props={
                "summary": "This is a test document",
                "bulletPoints": ["Point 1", "Point 2"]
            }),
            generate_component("a2ui.StatCard", props={
                "value": "$196B",
                "label": "Market Size",
                "trend": "up"
            }),
            generate_component("a2ui.VideoCard", props={
                "videoId": "dQw4w9WgXcQ",
                "platform": "youtube",
                "title": "Demo Video"
            }),
        ]

        # Step 2: Validate components
        assert len(components) == 3
        assert all(isinstance(c, A2UIComponent) for c in components)

        # Step 3: Emit components
        events = []
        async for event in emit_components(components):
            events.append(event)

        # Step 4: Verify emission
        assert len(events) == 3

        # Parse first event
        json_str = events[0].replace("data: ", "").strip()
        data = json.loads(json_str)
        assert data["type"] == "a2ui.TLDR"
        assert "bulletPoints" in data["props"]

    def test_component_id_uniqueness_across_types(self):
        """Test that IDs remain unique across different component types."""
        components = []
        for _ in range(10):
            components.append(generate_component("a2ui.StatCard", props={"value": "1", "label": "Test"}))
            components.append(generate_component("a2ui.VideoCard", props={"videoId": "123", "platform": "youtube"}))
            components.append(generate_component("a2ui.Section", props={"title": "Test"}))

        ids = [c.id for c in components]
        assert len(ids) == len(set(ids))  # All IDs are unique
