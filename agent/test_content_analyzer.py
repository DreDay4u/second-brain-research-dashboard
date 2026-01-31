"""
Comprehensive tests for the content_analyzer module.

Tests all parsing functions, regex patterns, and content analysis capabilities.
"""

import asyncio
from content_analyzer import (
    parse_markdown,
    analyze_content,
    ContentAnalysis,
    youtube_link_extraction_regex,
    github_link_extraction_regex,
    YOUTUBE_LINK_REGEX,
    GITHUB_LINK_REGEX,
)


# Test sample documents
SAMPLE_TUTORIAL = """# Building a REST API with FastAPI

## Introduction
This tutorial will guide you through building a production-ready REST API.

## Step 1: Setup
Install FastAPI and dependencies:

```bash
pip install fastapi uvicorn
```

## Step 2: Create Your First Endpoint

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## Step 3: Run the Server
Execute the following command:

```bash
uvicorn main:app --reload
```

## Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [YouTube Tutorial](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
- [GitHub Repository](https://github.com/tiangolo/fastapi)
- Code examples: https://github.com/fastapi/examples

Watch this tutorial: https://youtu.be/7t2alSnE2-I
"""

SAMPLE_RESEARCH = """# Machine Learning Model Performance Analysis

## Abstract
This paper analyzes the performance characteristics of various ML models.

## Methodology
We tested the following models:
- Random Forest
- Neural Networks
- Gradient Boosting

| Model | Accuracy | F1 Score |
|-------|----------|----------|
| Random Forest | 0.85 | 0.83 |
| Neural Network | 0.91 | 0.89 |
| Gradient Boost | 0.88 | 0.86 |

## Results
The neural network achieved the highest accuracy of 91%.

```python
import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
```

## Conclusion
Neural networks outperformed traditional ML models.

## References
- TensorFlow documentation
- Original research: https://github.com/research/ml-study
"""

SAMPLE_WITH_LINKS = """# Link Extraction Test

Various YouTube formats:
- Standard: https://www.youtube.com/watch?v=dQw4w9WgXcQ
- Short: https://youtu.be/7t2alSnE2-I
- Embed: https://www.youtube.com/embed/abc123defgh
- Shorts: https://youtube.com/shorts/xyz789

GitHub repositories:
- Main repo: https://github.com/facebook/react
- Raw file: https://raw.githubusercontent.com/user/repo/main/file.py
- Gist: https://gist.github.com/username/abc123
- GitHub Pages: https://username.github.io/project

Other links:
- Blog: https://example.com/blog
- Docs: https://docs.python.org
"""

SAMPLE_CODE_HEAVY = """# API Reference

## Authentication

```javascript
const auth = {
  apiKey: 'your-key',
  token: 'your-token'
};
```

## Making Requests

```python
import requests
response = requests.get('https://api.example.com')
```

## Response Format

```json
{
  "status": "success",
  "data": []
}
```

## Error Handling

```typescript
interface ErrorResponse {
  error: string;
  code: number;
}
```
"""


def test_parse_markdown_basic():
    """Test basic markdown parsing."""
    print("\n=== Test: Basic Markdown Parsing ===")

    result = parse_markdown(SAMPLE_TUTORIAL)

    print(f"Title: {result['title']}")
    print(f"Sections ({len(result['sections'])}): {result['sections']}")
    print(f"Code blocks ({len(result['code_blocks'])}): {[cb['language'] for cb in result['code_blocks']]}")
    print(f"All links ({len(result['all_links'])}): {result['all_links']}")

    assert result['title'] == 'Building a REST API with FastAPI'
    assert len(result['sections']) >= 4
    assert len(result['code_blocks']) >= 2
    print("✅ Basic parsing test PASSED")


def test_youtube_extraction():
    """Test YouTube link extraction."""
    print("\n=== Test: YouTube Link Extraction ===")

    result = parse_markdown(SAMPLE_WITH_LINKS)

    print(f"YouTube links found: {len(result['youtube_links'])}")
    for link in result['youtube_links']:
        print(f"  - {link}")

    assert len(result['youtube_links']) >= 3
    assert any('youtube.com/watch' in link for link in result['youtube_links'])
    assert any('youtu.be' in link for link in result['youtube_links'])
    print("✅ YouTube extraction test PASSED")


def test_github_extraction():
    """Test GitHub link extraction."""
    print("\n=== Test: GitHub Link Extraction ===")

    result = parse_markdown(SAMPLE_WITH_LINKS)

    print(f"GitHub links found: {len(result['github_links'])}")
    for link in result['github_links']:
        print(f"  - {link}")

    assert len(result['github_links']) >= 3
    assert any('github.com' in link for link in result['github_links'])
    print("✅ GitHub extraction test PASSED")


def test_code_block_detection():
    """Test code block detection."""
    print("\n=== Test: Code Block Detection ===")

    result = parse_markdown(SAMPLE_CODE_HEAVY)

    print(f"Code blocks found: {len(result['code_blocks'])}")
    for idx, block in enumerate(result['code_blocks']):
        print(f"  Block {idx + 1}: {block['language']} ({len(block['code'])} chars)")

    assert len(result['code_blocks']) >= 4
    languages = [block['language'] for block in result['code_blocks']]
    assert 'python' in languages or 'javascript' in languages or 'typescript' in languages
    print("✅ Code block detection test PASSED")


def test_table_extraction():
    """Test table extraction."""
    print("\n=== Test: Table Extraction ===")

    result = parse_markdown(SAMPLE_RESEARCH)

    print(f"Tables found: {len(result['tables'])}")
    for idx, table in enumerate(result['tables']):
        print(f"  Table {idx + 1}: {len(table['headers'])} columns, {table['row_count']} rows")
        print(f"    Headers: {table['headers']}")

    assert len(result['tables']) >= 1
    assert result['tables'][0]['row_count'] >= 2
    print("✅ Table extraction test PASSED")


def test_regex_patterns():
    """Test individual regex patterns."""
    print("\n=== Test: Regex Patterns ===")

    # YouTube regex tests
    youtube_test_cases = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/7t2alSnE2-I",
        "https://www.youtube.com/embed/abc123defgh",
        "https://youtube.com/shorts/xyz789",
    ]

    print("YouTube regex matches:")
    for url in youtube_test_cases:
        match = YOUTUBE_LINK_REGEX.search(url)
        print(f"  {url}: {'✅ Match' if match else '❌ No match'}")
        assert match is not None, f"Failed to match: {url}"

    # GitHub regex tests
    github_test_cases = [
        "https://github.com/facebook/react",
        "https://raw.githubusercontent.com/user/repo/main/file.py",
        "https://gist.github.com/username/abc123",
        "https://username.github.io/project",
    ]

    print("\nGitHub regex matches:")
    for url in github_test_cases:
        match = GITHUB_LINK_REGEX.search(url)
        print(f"  {url}: {'✅ Match' if match else '❌ No match'}")
        assert match is not None, f"Failed to match: {url}"

    print("✅ Regex patterns test PASSED")


async def test_analyze_content():
    """Test full content analysis with ContentAnalysis model."""
    print("\n=== Test: Full Content Analysis ===")

    # Test without agent (using heuristic classification)
    analysis = await analyze_content(SAMPLE_TUTORIAL, agent=None)

    print(f"Title: {analysis.title}")
    print(f"Document Type: {analysis.document_type}")
    print(f"Sections: {len(analysis.sections)}")
    print(f"Links: {len(analysis.links)}")
    print(f"YouTube Links: {len(analysis.youtube_links)}")
    print(f"GitHub Links: {len(analysis.github_links)}")
    print(f"Code Blocks: {len(analysis.code_blocks)}")
    print(f"Tables: {len(analysis.tables)}")
    print(f"Entities: {dict(analysis.entities)}")

    assert isinstance(analysis, ContentAnalysis)
    assert analysis.title == 'Building a REST API with FastAPI'
    assert analysis.document_type in ['tutorial', 'guide', 'article']
    assert len(analysis.sections) >= 4
    assert len(analysis.code_blocks) >= 2
    print("✅ Content analysis test PASSED")


async def test_document_classification():
    """Test document type classification."""
    print("\n=== Test: Document Classification ===")

    # Test tutorial
    tutorial_analysis = await analyze_content(SAMPLE_TUTORIAL, agent=None)
    print(f"Tutorial classified as: {tutorial_analysis.document_type}")
    assert tutorial_analysis.document_type == 'tutorial'

    # Test research
    research_analysis = await analyze_content(SAMPLE_RESEARCH, agent=None)
    print(f"Research classified as: {research_analysis.document_type}")
    assert research_analysis.document_type == 'research'

    # Test technical doc
    tech_analysis = await analyze_content(SAMPLE_CODE_HEAVY, agent=None)
    print(f"Technical doc classified as: {tech_analysis.document_type}")
    assert tech_analysis.document_type in ['technical_doc', 'guide']

    print("✅ Document classification test PASSED")


async def test_entity_extraction():
    """Test entity extraction."""
    print("\n=== Test: Entity Extraction ===")

    analysis = await analyze_content(SAMPLE_RESEARCH, agent=None)

    print("Extracted entities:")
    for category, items in analysis.entities.items():
        if items:
            print(f"  {category}: {items}")

    assert 'technologies' in analysis.entities or 'tools' in analysis.entities
    print("✅ Entity extraction test PASSED")


async def run_all_tests():
    """Run all test cases."""
    print("\n" + "=" * 60)
    print("Content Analyzer Test Suite")
    print("=" * 60)

    try:
        # Synchronous tests
        test_parse_markdown_basic()
        test_youtube_extraction()
        test_github_extraction()
        test_code_block_detection()
        test_table_extraction()
        test_regex_patterns()

        # Async tests
        await test_analyze_content()
        await test_document_classification()
        await test_entity_extraction()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        return True

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)
