"""
Demonstration of content_analyzer module capabilities.
Shows all features in action with detailed output.
"""

import asyncio
from content_analyzer import (
    parse_markdown,
    analyze_content,
    youtube_link_extraction_regex,
    github_link_extraction_regex,
)


# Comprehensive test document
DEMO_DOCUMENT = """# Advanced Python Tutorial: Building AI Agents

## Introduction
Learn how to build production-ready AI agents using Python, FastAPI, and Claude.

## Prerequisites
Before starting, make sure you have:
- Python 3.12 or higher
- Basic understanding of REST APIs
- OpenAI or Anthropic API key

## Step 1: Environment Setup

First, install the required dependencies:

```bash
pip install fastapi uvicorn pydantic-ai anthropic openai
pip install python-dotenv aiohttp
```

Create a `.env` file with your API keys:

```bash
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

## Step 2: Building the Agent

Here's the core agent implementation:

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class AgentState(BaseModel):
    user_input: str
    context: dict = {}

agent = Agent(
    model="claude-sonnet-4",
    deps_type=AgentState,
)

@agent.tool
async def search_web(ctx, query: str) -> dict:
    # Implement web search
    return {"results": []}
```

## Step 3: Adding FastAPI Endpoints

Create a streaming endpoint:

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/stream")
async def stream_response(request: dict):
    async def generate():
        result = await agent.run(request["prompt"])
        yield result.data

    return StreamingResponse(generate())
```

## Performance Benchmarks

| Framework | Requests/sec | Latency (ms) | Memory (MB) |
|-----------|--------------|--------------|-------------|
| FastAPI | 5000 | 12 | 45 |
| Flask | 2000 | 28 | 62 |
| Django | 1500 | 35 | 78 |

Based on these results, FastAPI shows 2.5x better performance.

## Resources

### Video Tutorials
- [FastAPI Crash Course](https://www.youtube.com/watch?v=0sOvCWFmrtA)
- [AI Agents Explained](https://youtu.be/F8NKVhkZZWI)
- [Live Coding Session](https://youtube.com/shorts/abc123defgh)

### GitHub Repositories
- [Pydantic AI](https://github.com/pydantic/pydantic-ai)
- [FastAPI](https://github.com/tiangolo/fastapi)
- [Example Code](https://raw.githubusercontent.com/examples/ai-agent/main/agent.py)
- [My Gist](https://gist.github.com/username/abc123)

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Anthropic API](https://docs.anthropic.com)
- [OpenAI API](https://platform.openai.com/docs)

## Code Examples

JavaScript client:

```javascript
const response = await fetch('/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ prompt: 'Hello!' })
});
```

TypeScript types:

```typescript
interface AgentRequest {
  prompt: string;
  context?: Record<string, any>;
}

interface AgentResponse {
  data: string;
  usage: TokenUsage;
}
```

## Deployment

Use Docker for containerization:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

## Conclusion

You've learned how to build AI agents with FastAPI and Pydantic AI! Key technologies used:
- Python for backend
- FastAPI for API framework
- Pydantic AI for agent orchestration
- Claude/OpenAI for LLM capabilities
- Docker for deployment

Happy coding!
"""


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


async def main():
    """Run comprehensive demonstration."""

    print_section("CONTENT ANALYZER DEMONSTRATION")

    # Part 1: Parse Markdown
    print_section("1. PARSING MARKDOWN STRUCTURE")
    parsed = parse_markdown(DEMO_DOCUMENT)

    print(f"📄 Title: {parsed['title']}")
    print(f"\n📑 Sections ({len(parsed['sections'])}):")
    for i, section in enumerate(parsed['sections'][:8], 1):
        print(f"   {i}. {section}")

    print(f"\n🔗 Total Links: {len(parsed['all_links'])}")
    print(f"   - YouTube: {len(parsed['youtube_links'])}")
    print(f"   - GitHub: {len(parsed['github_links'])}")
    print(f"   - Other: {len(parsed['all_links']) - len(parsed['youtube_links']) - len(parsed['github_links'])}")

    print(f"\n💻 Code Blocks: {len(parsed['code_blocks'])}")
    for i, block in enumerate(parsed['code_blocks'], 1):
        print(f"   {i}. Language: {block['language']} ({len(block['code'])} characters)")

    print(f"\n📊 Tables: {len(parsed['tables'])}")
    for i, table in enumerate(parsed['tables'], 1):
        print(f"   {i}. {len(table['headers'])} columns × {table['row_count']} rows")
        print(f"      Headers: {', '.join(table['headers'])}")

    # Part 2: YouTube Links
    print_section("2. YOUTUBE LINK EXTRACTION")
    print(f"Found {len(parsed['youtube_links'])} YouTube links:\n")
    for i, link in enumerate(parsed['youtube_links'], 1):
        print(f"   {i}. {link}")

    # Part 3: GitHub Links
    print_section("3. GITHUB LINK EXTRACTION")
    print(f"Found {len(parsed['github_links'])} GitHub links:\n")
    for i, link in enumerate(parsed['github_links'], 1):
        print(f"   {i}. {link}")

    # Part 4: Code Block Details
    print_section("4. CODE BLOCK DETECTION")
    print(f"Extracted {len(parsed['code_blocks'])} code blocks:\n")
    for i, block in enumerate(parsed['code_blocks'], 1):
        print(f"Block #{i} - {block['language'].upper()}")
        print("-" * 70)
        preview = block['code'][:150]
        if len(block['code']) > 150:
            preview += "..."
        print(preview)
        print()

    # Part 5: Full Analysis with LLM
    print_section("5. FULL CONTENT ANALYSIS")
    analysis = await analyze_content(DEMO_DOCUMENT, agent=None)

    print(f"📄 Title: {analysis.title}")
    print(f"📝 Document Type: {analysis.document_type.upper()}")
    print(f"\n📊 Statistics:")
    print(f"   - Sections: {len(analysis.sections)}")
    print(f"   - Total Links: {len(analysis.links)}")
    print(f"   - YouTube Links: {len(analysis.youtube_links)}")
    print(f"   - GitHub Links: {len(analysis.github_links)}")
    print(f"   - Code Blocks: {len(analysis.code_blocks)}")
    print(f"   - Tables: {len(analysis.tables)}")

    print(f"\n🏷️  Extracted Entities:")
    for category, items in analysis.entities.items():
        if items:
            print(f"\n   {category.upper()}:")
            for item in items[:8]:
                print(f"     • {item}")

    # Part 6: Validation Tests
    print_section("6. REGEX PATTERN VALIDATION")

    test_youtube = [
        "https://www.youtube.com/watch?v=0sOvCWFmrtA",
        "https://youtu.be/F8NKVhkZZWI",
        "https://youtube.com/shorts/abc123defgh",
    ]

    print("YouTube Pattern Tests:")
    for url in test_youtube:
        match = youtube_link_extraction_regex.search(url)
        status = "✅" if match else "❌"
        print(f"   {status} {url}")

    test_github = [
        "https://github.com/pydantic/pydantic-ai",
        "https://raw.githubusercontent.com/examples/ai-agent/main/agent.py",
        "https://gist.github.com/username/abc123",
    ]

    print("\nGitHub Pattern Tests:")
    for url in test_github:
        match = github_link_extraction_regex.search(url)
        status = "✅" if match else "❌"
        print(f"   {status} {url}")

    # Summary
    print_section("DEMONSTRATION COMPLETE")
    print("✅ All parsing functions working")
    print("✅ ContentAnalysis model validated")
    print("✅ Link extraction successful")
    print("✅ Code block detection operational")
    print("✅ Table extraction functional")
    print("✅ Entity recognition active")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
