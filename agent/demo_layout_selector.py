"""
Layout Selector Visual Demo - Interactive demonstration of layout selection.

This script creates visual examples of layout selection for different content
types and shows the decision-making process with rich terminal output.
"""

import asyncio
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.layout import Layout as RichLayout
from rich import box
from content_analyzer import ContentAnalysis
from layout_selector import select_layout, LayoutDecision


console = Console()


def create_sample_content() -> list[tuple[str, ContentAnalysis]]:
    """Create sample content analyses for different document types."""
    samples = []

    # Sample 1: Python Tutorial (code-heavy)
    samples.append((
        "Python Tutorial - Machine Learning Basics",
        ContentAnalysis(
            title="Machine Learning with Python: A Complete Guide",
            document_type="tutorial",
            sections=[
                "Introduction",
                "Installing Dependencies",
                "Loading Data",
                "Training a Model",
                "Evaluating Results",
                "Deploying the Model"
            ],
            code_blocks=[
                {"language": "python", "code": "import pandas as pd"},
                {"language": "python", "code": "df = pd.read_csv('data.csv')"},
                {"language": "python", "code": "from sklearn.model_selection import train_test_split"},
                {"language": "python", "code": "X_train, X_test = train_test_split(X, y)"},
                {"language": "python", "code": "model = RandomForestClassifier()"},
                {"language": "python", "code": "model.fit(X_train, y_train)"},
                {"language": "python", "code": "predictions = model.predict(X_test)"},
            ],
            tables=[],
            links=["https://scikit-learn.org", "https://pandas.pydata.org"],
            youtube_links=["https://youtube.com/watch?v=ml-tutorial"],
            github_links=["https://github.com/user/ml-tutorial"],
            entities={
                "technologies": ["Python", "Pandas", "Scikit-learn"],
                "tools": ["Jupyter"],
                "languages": ["Python"],
                "concepts": ["Machine Learning", "Random Forest"]
            }
        )
    ))

    # Sample 2: Research Paper (table-heavy)
    samples.append((
        "Research Paper - Performance Comparison",
        ContentAnalysis(
            title="Comparative Analysis of Deep Learning Frameworks",
            document_type="research",
            sections=[
                "Abstract",
                "Introduction",
                "Methodology",
                "Experimental Setup",
                "Results",
                "Discussion",
                "Conclusion",
                "References"
            ],
            code_blocks=[
                {"language": "python", "code": "import tensorflow as tf"},
                {"language": "python", "code": "import torch"}
            ],
            tables=[
                {
                    "headers": ["Framework", "Training Time", "Accuracy"],
                    "rows": [
                        ["TensorFlow", "45.2s", "94.3%"],
                        ["PyTorch", "42.1s", "94.8%"],
                        ["JAX", "38.9s", "94.5%"]
                    ],
                    "row_count": 3
                },
                {
                    "headers": ["Model", "Parameters", "Memory Usage"],
                    "rows": [
                        ["ResNet-50", "25M", "2.1GB"],
                        ["VGG-16", "138M", "5.4GB"]
                    ],
                    "row_count": 2
                },
                {
                    "headers": ["Dataset", "Size", "Classes"],
                    "rows": [
                        ["ImageNet", "1.2M", "1000"],
                        ["CIFAR-10", "60K", "10"]
                    ],
                    "row_count": 2
                }
            ],
            links=["https://arxiv.org/paper123"],
            youtube_links=[],
            github_links=["https://github.com/research/benchmark"],
            entities={
                "technologies": ["TensorFlow", "PyTorch"],
                "tools": [],
                "languages": ["Python"],
                "concepts": ["Deep Learning", "Performance Analysis"]
            }
        )
    ))

    # Sample 3: News Article (media-rich)
    samples.append((
        "Tech News Article",
        ContentAnalysis(
            title="OpenAI Announces GPT-5: The Future of AI is Here",
            document_type="article",
            sections=[
                "Breaking News",
                "Key Features",
                "Industry Impact",
                "Expert Opinions",
                "What's Next"
            ],
            code_blocks=[],
            tables=[],
            links=[
                "https://openai.com/gpt5",
                "https://techcrunch.com/article",
                "https://theverge.com/story",
                "https://wired.com/news",
                "https://arstechnica.com/analysis"
            ],
            youtube_links=[
                "https://youtube.com/watch?v=demo1",
                "https://youtube.com/watch?v=demo2",
                "https://youtube.com/watch?v=interview1",
                "https://youtube.com/watch?v=analysis1"
            ],
            github_links=["https://github.com/openai/gpt5-examples"],
            entities={
                "technologies": ["OpenAI", "GPT-5"],
                "tools": [],
                "languages": [],
                "concepts": ["AI", "Large Language Models"]
            }
        )
    ))

    # Sample 4: API Documentation (section-heavy)
    samples.append((
        "API Reference Documentation",
        ContentAnalysis(
            title="REST API Documentation - v2.0",
            document_type="technical_doc",
            sections=[
                "Overview",
                "Authentication",
                "Rate Limiting",
                "Endpoints",
                "GET /users",
                "POST /users",
                "GET /users/{id}",
                "PUT /users/{id}",
                "DELETE /users/{id}",
                "GET /posts",
                "POST /posts",
                "Error Handling",
                "Status Codes",
                "Examples",
                "SDKs"
            ],
            code_blocks=[
                {"language": "bash", "code": "curl -X GET https://api.example.com/users"},
                {"language": "python", "code": "response = requests.get('https://api.example.com/users')"},
                {"language": "javascript", "code": "const response = await fetch('/users')"}
            ],
            tables=[
                {
                    "headers": ["Endpoint", "Method", "Description"],
                    "rows": [
                        ["/users", "GET", "List all users"],
                        ["/users", "POST", "Create user"]
                    ],
                    "row_count": 2
                }
            ],
            links=["https://api.example.com/docs"],
            youtube_links=[],
            github_links=["https://github.com/company/api-sdk"],
            entities={
                "technologies": ["REST", "API"],
                "tools": ["curl", "Postman"],
                "languages": ["Python", "JavaScript"],
                "concepts": ["Authentication", "Rate Limiting"]
            }
        )
    ))

    # Sample 5: Quick Notes (minimal content)
    samples.append((
        "Quick Meeting Notes",
        ContentAnalysis(
            title="Team Standup - January 30, 2026",
            document_type="notes",
            sections=[
                "Attendees",
                "Key Points",
                "Action Items",
                "Next Steps"
            ],
            code_blocks=[],
            tables=[],
            links=["https://jira.company.com/PROJ-123"],
            youtube_links=[],
            github_links=["https://github.com/team/project"],
            entities={
                "technologies": [],
                "tools": ["Jira", "GitHub"],
                "languages": [],
                "concepts": ["Sprint Planning", "Code Review"]
            }
        )
    ))

    return samples


def display_content_summary(name: str, content: ContentAnalysis):
    """Display a summary of the content being analyzed."""
    summary_table = Table(title=f"Content: {name}", box=box.ROUNDED)
    summary_table.add_column("Property", style="cyan")
    summary_table.add_column("Value", style="white")

    summary_table.add_row("Title", content.title)
    summary_table.add_row("Type", content.document_type)
    summary_table.add_row("Sections", str(len(content.sections)))
    summary_table.add_row("Code Blocks", str(len(content.code_blocks)))
    summary_table.add_row("Tables", str(len(content.tables)))
    summary_table.add_row("Links", str(len(content.links)))
    summary_table.add_row("YouTube Links", str(len(content.youtube_links)))
    summary_table.add_row("GitHub Links", str(len(content.github_links)))

    console.print(summary_table)


def display_layout_decision(decision: LayoutDecision):
    """Display the layout decision with rich formatting."""
    # Create decision panel
    decision_content = f"""
[bold cyan]Layout Type:[/bold cyan] {decision.layout_type}
[bold green]Confidence:[/bold green] {decision.confidence:.2%}
[bold yellow]Reasoning:[/bold yellow] {decision.reasoning}
    """

    console.print(Panel(
        decision_content.strip(),
        title="Layout Decision",
        border_style="green",
        box=box.DOUBLE
    ))

    # Components table
    if decision.component_suggestions:
        components_table = Table(title="Suggested A2UI Components", box=box.SIMPLE)
        components_table.add_column("Component", style="magenta")
        components_table.add_column("Purpose", style="white")

        component_purposes = {
            "CodeBlock": "Display code snippets with syntax highlighting",
            "StepList": "Show sequential tutorial steps",
            "ProgressTracker": "Track completion progress",
            "DataTable": "Display tabular data",
            "StatCard": "Highlight key statistics",
            "ComparisonChart": "Compare data visually",
            "Hero": "Create engaging header section",
            "ImageGallery": "Display multiple images",
            "Quote": "Highlight important quotes",
            "OrderedList": "Show numbered steps",
            "Checklist": "Interactive task list",
            "KeyPoints": "Summarize main points",
            "TagCloud": "Display categorized tags",
            "ApiTable": "API endpoint reference",
            "TabbedContent": "Organize content in tabs",
            "SideNav": "Navigation sidebar",
            "MediaEmbed": "Embed videos and media",
            "Card": "Flexible content container",
            "Timeline": "Display chronological events",
            "Highlight": "Emphasize key information",
            "CollapsibleSection": "Expandable content sections",
            "Citation": "Reference citations",
            "Graph": "Data visualization",
            "RelatedLinks": "Related content links",
            "ShareButtons": "Social sharing",
            "Accordion": "Collapsible sections",
            "CalloutBox": "Important notices",
            "QuickReference": "Quick lookup table",
            "MiniCard": "Compact information card",
            "SearchBar": "Search functionality"
        }

        for component in decision.component_suggestions[:5]:
            purpose = component_purposes.get(component, "Custom component")
            components_table.add_row(component, purpose)

        console.print(components_table)

    # Alternatives
    if decision.alternative_layouts:
        console.print(f"\n[dim]Alternative layouts: {', '.join(decision.alternative_layouts[:3])}[/dim]")


async def demo_layout_selection():
    """Run interactive demo of layout selection."""
    console.clear()
    console.print(Panel.fit(
        "[bold blue]Layout Selector Demo[/bold blue]\n"
        "Demonstrating rule-based and LLM-powered layout selection",
        border_style="blue"
    ))
    console.print()

    samples = create_sample_content()

    for i, (name, content) in enumerate(samples, 1):
        console.print(f"\n[bold white]{'=' * 70}[/bold white]")
        console.print(f"[bold white]Example {i}/{len(samples)}[/bold white]\n")

        # Display content summary
        display_content_summary(name, content)
        console.print()

        # Select layout
        console.print("[dim]Analyzing content and selecting layout...[/dim]")
        decision = await select_layout(content, agent=None)

        # Display decision
        display_layout_decision(decision)

        # Show decision path
        if decision.confidence >= 0.85:
            console.print(f"\n[dim italic]Decision made using: High-confidence rule-based selection[/dim italic]")
        elif decision.confidence >= 0.75:
            console.print(f"\n[dim italic]Decision made using: Document type mapping[/dim italic]")
        else:
            console.print(f"\n[dim italic]Decision made using: Fallback logic[/dim italic]")

        if i < len(samples):
            console.print(f"\n[dim]Press Enter to continue...[/dim]", end="")
            # Auto-continue for demo
            await asyncio.sleep(0.5)
            console.print("\n")

    console.print(f"\n[bold white]{'=' * 70}[/bold white]")
    console.print("\n[bold green]✓ Demo completed successfully![/bold green]")
    console.print("\n[dim]Layout selector can handle:")
    console.print("  • Code-heavy tutorials → instructional_layout")
    console.print("  • Data/research papers → data_layout")
    console.print("  • News articles → news_layout")
    console.print("  • API documentation → reference_layout")
    console.print("  • Quick notes → summary_layout")
    console.print("  • And more with intelligent fallback logic[/dim]")


async def main():
    """Main entry point for demo."""
    try:
        await demo_layout_selection()
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        raise


if __name__ == "__main__":
    asyncio.run(main())
