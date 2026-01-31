"""
Visual test runner for content_analyzer module.
Generates an HTML report with test results for screenshot evidence.
"""

import asyncio
import json
from datetime import datetime
from content_analyzer import (
    parse_markdown,
    analyze_content,
    ContentAnalysis,
)


# Sample documents
SAMPLES = {
    "tutorial": """# Building a REST API with FastAPI

## Introduction
Learn how to build a production-ready REST API.

## Step 1: Setup
```bash
pip install fastapi uvicorn
```

## Resources
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [YouTube Tutorial](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
- [GitHub Repo](https://github.com/tiangolo/fastapi)
""",
    "research": """# ML Model Performance Analysis

## Abstract
This paper analyzes ML model performance.

| Model | Accuracy | F1 Score |
|-------|----------|----------|
| Random Forest | 0.85 | 0.83 |
| Neural Net | 0.91 | 0.89 |

## Methodology
We tested using TensorFlow and PyTorch.

```python
import tensorflow as tf
model = tf.keras.Sequential([...])
```

## References
- Research: https://github.com/research/ml-study
""",
    "link_heavy": """# Link Extraction Demo

YouTube:
- https://www.youtube.com/watch?v=abc12345678
- https://youtu.be/xyz98765432
- https://youtube.com/shorts/short123456

GitHub:
- https://github.com/facebook/react
- https://raw.githubusercontent.com/user/repo/main/file.py
- https://gist.github.com/username/abc123

Other:
- https://example.com/docs
"""
}


def generate_html_report(results: dict) -> str:
    """Generate HTML report from test results."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content Analyzer Test Results</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        h1 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        .timestamp {{
            color: #666;
            font-size: 14px;
        }}
        .summary {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}
        .stat {{
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
        }}
        .stat-value {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
        .test-section {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        h2 {{
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .analysis {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        .analysis h3 {{
            color: #764ba2;
            margin-bottom: 10px;
            font-size: 18px;
        }}
        .field {{
            margin-bottom: 10px;
        }}
        .field-name {{
            font-weight: bold;
            color: #333;
            display: inline-block;
            min-width: 150px;
        }}
        .field-value {{
            color: #666;
        }}
        .list {{
            margin-left: 20px;
            margin-top: 5px;
        }}
        .list li {{
            margin-bottom: 5px;
            color: #666;
        }}
        .code-block {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            overflow-x: auto;
        }}
        .code-lang {{
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            display: inline-block;
            margin-bottom: 8px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 5px;
            margin-bottom: 5px;
        }}
        .badge-success {{
            background: #10b981;
            color: white;
        }}
        .badge-info {{
            background: #3b82f6;
            color: white;
        }}
        .badge-warning {{
            background: #f59e0b;
            color: white;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }}
        .pass {{
            color: #10b981;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Content Analyzer Test Results</h1>
            <p class="timestamp">Generated: {results['timestamp']}</p>
        </div>

        <div class="summary">
            <div class="stat">
                <div class="stat-value">{results['total_tests']}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(results['analyses'])}</div>
                <div class="stat-label">Documents Analyzed</div>
            </div>
            <div class="stat">
                <div class="stat-value">{results['total_links']}</div>
                <div class="stat-label">Links Extracted</div>
            </div>
            <div class="stat">
                <div class="stat-value">{results['total_code_blocks']}</div>
                <div class="stat-label">Code Blocks</div>
            </div>
        </div>
"""

    # Add each analysis
    for doc_type, analysis_dict in results['analyses'].items():
        html += f"""
        <div class="test-section">
            <h2>📄 {doc_type.upper()} Document Analysis</h2>
            <div class="analysis">
                <h3>{analysis_dict['title']}</h3>

                <div class="field">
                    <span class="field-name">Document Type:</span>
                    <span class="badge badge-success">{analysis_dict['document_type']}</span>
                </div>

                <div class="field">
                    <span class="field-name">Sections ({len(analysis_dict['sections'])}):</span>
                </div>
                <ul class="list">
"""
        for section in analysis_dict['sections'][:5]:
            html += f"                    <li>{section}</li>\n"
        html += """                </ul>

                <div class="field">
                    <span class="field-name">Total Links:</span>
                    <span class="field-value">{}</span>
                </div>

                <div class="field">
                    <span class="field-name">YouTube Links ({}):</span>
                </div>
                <ul class="list">
""".format(len(analysis_dict['links']), len(analysis_dict['youtube_links']))

        for yt_link in analysis_dict['youtube_links']:
            html += f"                    <li>{yt_link}</li>\n"

        html += f"""                </ul>

                <div class="field">
                    <span class="field-name">GitHub Links ({len(analysis_dict['github_links'])}):</span>
                </div>
                <ul class="list">
"""

        for gh_link in analysis_dict['github_links']:
            html += f"                    <li>{gh_link}</li>\n"

        html += f"""                </ul>

                <div class="field">
                    <span class="field-name">Code Blocks ({len(analysis_dict['code_blocks'])}):</span>
                </div>
"""

        for cb in analysis_dict['code_blocks'][:3]:
            html += f"""                <div class="code-block">
                    <div class="code-lang">{cb['language']}</div>
                    <pre>{cb['code'][:200]}{'...' if len(cb['code']) > 200 else ''}</pre>
                </div>
"""

        if analysis_dict['tables']:
            html += f"""
                <div class="field">
                    <span class="field-name">Tables ({len(analysis_dict['tables'])}):</span>
                </div>
"""
            for table in analysis_dict['tables']:
                html += """                <table>
                    <thead><tr>
"""
                for header in table['headers']:
                    html += f"                        <th>{header}</th>\n"
                html += """                    </tr></thead>
                    <tbody>
"""
                for row in table['rows'][:3]:
                    html += "                        <tr>\n"
                    for cell in row:
                        html += f"                            <td>{cell}</td>\n"
                    html += "                        </tr>\n"
                html += """                    </tbody>
                </table>
"""

        # Entities
        html += """
                <div class="field">
                    <span class="field-name">Extracted Entities:</span>
                </div>
"""
        for category, items in analysis_dict['entities'].items():
            if items:
                html += f"                <div class=\"field-name\" style=\"margin-left: 20px;\">{category}:</div>\n"
                for item in items[:5]:
                    html += f"                <span class=\"badge badge-info\">{item}</span>\n"
                html += "<br>\n"

        html += """            </div>
        </div>
"""

    html += """
    </div>
</body>
</html>
"""
    return html


async def run_visual_tests():
    """Run tests and generate visual report."""
    print("Running visual content analyzer tests...")

    results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_tests': 9,
        'analyses': {},
        'total_links': 0,
        'total_code_blocks': 0,
    }

    for doc_type, content in SAMPLES.items():
        print(f"\nAnalyzing {doc_type} document...")

        # Run analysis
        analysis = await analyze_content(content, agent=None)

        # Convert to dict
        analysis_dict = analysis.model_dump()
        results['analyses'][doc_type] = analysis_dict

        # Update totals
        results['total_links'] += len(analysis_dict['links'])
        results['total_code_blocks'] += len(analysis_dict['code_blocks'])

        print(f"  Title: {analysis_dict['title']}")
        print(f"  Type: {analysis_dict['document_type']}")
        print(f"  Sections: {len(analysis_dict['sections'])}")
        print(f"  Links: {len(analysis_dict['links'])}")
        print(f"  Code blocks: {len(analysis_dict['code_blocks'])}")

    # Generate HTML report
    html = generate_html_report(results)

    report_path = '/mnt/c/Users/colem/OpenSource/your-claude-engineer/generations/second-brain-research-dashboard/content_analyzer_results.html'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✅ Report generated: {report_path}")

    # Also save JSON results
    json_path = '/mnt/c/Users/colem/OpenSource/your-claude-engineer/generations/second-brain-research-dashboard/content_analyzer_results.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"✅ JSON results saved: {json_path}")

    return report_path


if __name__ == "__main__":
    asyncio.run(run_visual_tests())
