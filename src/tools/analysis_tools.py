"""Analysis tools for repository data processing."""

import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from datetime import datetime
import matplotlib.dates as mdates
import re
import os
from typing import Dict, List, Tuple, Any
import logging
from src.config.tools import (
    CHART_FIGURE_SIZE, 
    CHART_DPI,
    CHART_OUTPUT_DIR,
    COMMIT_CHART_NAME,
    CATEGORY_CHART_NAME, 
    TOPICS_CHART_NAME
)

logger = logging.getLogger(__name__)


def categorize_commit(message: str) -> str:
    """Categorize a commit message by type.
    
    Args:
        message: Commit message to categorize
        
    Returns:
        str: Category with emoji
    """
    message = message.lower()
    
    if any(kw in message for kw in ["fix", "bug"]):
        return "🐛 Bug Fixes"
    elif any(kw in message for kw in ["add", "feature", "implement"]):
        return "✨ Features"
    elif any(kw in message for kw in ["doc", "readme"]):
        return "📄 Documentation"
    elif any(kw in message for kw in ["remove", "delete"]):
        return "🔥 Removals"
    elif any(kw in message for kw in ["update", "upgrade"]):
        return "🔧 Updates"
    elif any(kw in message for kw in ["merge", "pull"]):
        return "🔀 Merges"
    else:
        return "📦 Others"


def generate_commit_timeline_chart(commit_dates: List[str]) -> str:
    """Generate a chart showing commits over time.
    
    Args:
        commit_dates: List of commit dates in ISO format
        
    Returns:
        str: Path to the generated chart
    """
    try:
        commit_day_counts = defaultdict(int)
        for date_str in commit_dates:
            try:
                day = datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
                commit_day_counts[day] += 1
            except ValueError:
                continue
                
        if not commit_day_counts:
            logger.warning("No valid commit dates found")
            return ""
            
        recent_days = sorted(commit_day_counts.keys())
        counts = [commit_day_counts[day] for day in recent_days]

        plt.figure(figsize=CHART_FIGURE_SIZE, dpi=CHART_DPI)
        plt.plot(recent_days, counts, marker='o', linestyle='-', color='tab:blue', label='Commits per day')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        plt.gcf().autofmt_xdate()
        plt.xlabel("Date")
        plt.ylabel("Commits")
        plt.title("📈 Commits Over Time")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        chart_path = os.path.join(CHART_OUTPUT_DIR, COMMIT_CHART_NAME)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=CHART_DPI, bbox_inches='tight')
        plt.close()
        
        return chart_path
        
    except Exception as e:
        logger.error(f"Error generating commit timeline chart: {e}")
        return ""


def generate_category_chart(commit_messages: List[str]) -> str:
    """Generate a chart showing commit categories.
    
    Args:
        commit_messages: List of commit messages
        
    Returns:
        str: Path to the generated chart
    """
    try:
        category_counter = Counter()
        
        for msg in commit_messages:
            short_msg = re.split(r'—|@', msg)[0].strip()
            category = categorize_commit(short_msg)
            category_counter[category] += 1

        if not category_counter:
            logger.warning("No commit categories found")
            return ""
            
        plt.figure(figsize=CHART_FIGURE_SIZE, dpi=CHART_DPI)
        cats, values = zip(*category_counter.items())
        plt.bar(cats, values, color='tab:green')
        plt.ylabel("Commits")
        plt.title("🧩 Commits by Category")
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        
        chart_path = os.path.join(CHART_OUTPUT_DIR, CATEGORY_CHART_NAME)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=CHART_DPI, bbox_inches='tight')
        plt.close()
        
        return chart_path
        
    except Exception as e:
        logger.error(f"Error generating category chart: {e}")
        return ""


def generate_topics_chart(commit_messages: List[str]) -> str:
    """Generate a chart showing most mentioned topics in commits.
    
    Args:
        commit_messages: List of commit messages
        
    Returns:
        str: Path to the generated chart
    """
    try:
        word_freq = Counter()
        
        for msg in commit_messages:
            # Extract words with length >= 4
            words = re.findall(r'\b\w{4,}\b', msg.lower())
            word_freq.update(words)

        if not word_freq:
            logger.warning("No words found in commit messages")
            return ""
            
        most_common = word_freq.most_common(10)
        if not most_common:
            return ""
            
        labels, freqs = zip(*most_common)
        
        plt.figure(figsize=CHART_FIGURE_SIZE, dpi=CHART_DPI)
        plt.bar(labels, freqs, color='tab:purple')
        plt.ylabel("Frequency")
        plt.title("🔥 Most Mentioned Topics in Commits")
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        
        chart_path = os.path.join(CHART_OUTPUT_DIR, TOPICS_CHART_NAME)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=CHART_DPI, bbox_inches='tight')
        plt.close()
        
        return chart_path
        
    except Exception as e:
        logger.error(f"Error generating topics chart: {e}")
        return ""


def generate_charts(commit_messages: List[str], commit_dates: List[str]) -> List[str]:
    """Generate all analysis charts.
    
    Args:
        commit_messages: List of commit messages
        commit_dates: List of commit dates
        
    Returns:
        List[str]: Paths to generated charts
    """
    charts = []
    
    # Generate timeline chart
    timeline_chart = generate_commit_timeline_chart(commit_dates)
    if timeline_chart:
        charts.append(timeline_chart)
        
    # Generate category chart
    category_chart = generate_category_chart(commit_messages)
    if category_chart:
        charts.append(category_chart)
        
    # Generate topics chart
    topics_chart = generate_topics_chart(commit_messages)
    if topics_chart:
        charts.append(topics_chart)
        
    return charts


def analyze_code_activity(repo_data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Analyze repository activity and generate insights.
    
    Args:
        repo_data: Repository data containing commits and metadata
        
    Returns:
        Tuple of (analysis insights, chart paths)
    """
    try:
        commit_messages = repo_data.get('commits', [])
        commit_dates = repo_data.get('commit_dates', [])
        
        if not commit_messages:
            return ["No commit data available for analysis"], []
            
        # Generate charts
        chart_paths = generate_charts(commit_messages, commit_dates)
        
        # Analyze commit categories
        commit_categories = defaultdict(list)
        category_counter = Counter()
        
        for msg in commit_messages:
            short_msg = re.split(r'—|@', msg)[0].strip()
            category = categorize_commit(short_msg)
            commit_categories[category].append(short_msg)
            category_counter[category] += 1

        # Build analysis insights
        analysis = ["## 🔍 Commit Analysis by Category"]
        
        for cat, msgs in commit_categories.items():
            count = category_counter[cat]
            analysis.append(f"\n### {cat} ({count} commits)")
            
            # Show top 3 commits for each category
            for msg in msgs[:3]:
                clean_msg = msg.replace("\n", " ").strip()
                if len(clean_msg) > 100:
                    clean_msg = clean_msg[:100] + "..."
                analysis.append(f"- {clean_msg}")
                
        # Add summary statistics
        analysis.append(f"\n## 📊 Summary Statistics")
        analysis.append(f"- Total commits analyzed: {len(commit_messages)}")
        analysis.append(f"- Most active category: {category_counter.most_common(1)[0][0] if category_counter else 'N/A'}")
        analysis.append(f"- Number of categories: {len(category_counter)}")
        
        return analysis, chart_paths
        
    except Exception as e:
        logger.error(f"Error analyzing code activity: {e}")
        return [f"Error during analysis: {str(e)}"], [] 