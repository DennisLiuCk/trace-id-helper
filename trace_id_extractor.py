#!/usr/bin/env python3
"""
Trace ID Extractor Tool

Extracts trace IDs from messy log data and generates DQL queries.
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Set, List, Tuple


def extract_trace_ids(log_content: str) -> Set[str]:
    """
    Extract unique trace IDs from log content.
    
    Args:
        log_content: Raw log data as string
        
    Returns:
        Set of unique trace IDs
    """
    pattern = r'\[T-([a-f0-9]+),S-[a-f0-9]+\]'
    matches = re.findall(pattern, log_content)
    return set(matches)


def extract_trace_and_span_pairs(log_content: str) -> Set[Tuple[str, str]]:
    """
    Extract unique trace ID and span ID pairs from log content.
    
    Args:
        log_content: Raw log data as string
        
    Returns:
        Set of unique (trace_id, span_id) tuples
    """
    pattern = r'\[T-([a-f0-9]+),S-([a-f0-9]+)\]'
    matches = re.findall(pattern, log_content)
    return set(matches)


def generate_dql_query(trace_ids: Set[str]) -> str:
    """
    Generate DQL query from trace IDs.
    
    Args:
        trace_ids: Set of trace IDs
        
    Returns:
        DQL query string
    """
    if not trace_ids:
        return ""
    
    formatted_ids = [f'"T-{trace_id}"' for trace_id in sorted(trace_ids)]
    return f"({' OR '.join(formatted_ids)})"


def generate_dql_query_with_spans(trace_span_pairs: Set[Tuple[str, str]]) -> str:
    """
    Generate DQL query from trace ID and span ID pairs.
    
    Args:
        trace_span_pairs: Set of (trace_id, span_id) tuples
        
    Returns:
        DQL query string
    """
    if not trace_span_pairs:
        return ""
    
    formatted_pairs = [f'"T-{trace_id},S-{span_id}"' for trace_id, span_id in sorted(trace_span_pairs)]
    return f"({' OR '.join(formatted_pairs)})"


def process_log_file(input_file: Path, output_file: Path = None, include_spans: bool = False) -> str:
    """
    Process log file and generate DQL query.
    
    Args:
        input_file: Path to input log file
        output_file: Optional path to output file
        include_spans: Whether to include span IDs in the output
        
    Returns:
        Generated DQL query
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {input_file}")
    except Exception as e:
        raise Exception(f"Error reading input file: {e}")
    
    if include_spans:
        trace_span_pairs = extract_trace_and_span_pairs(log_content)
        if not trace_span_pairs:
            print("Warning: No trace/span pairs found in the log file")
            return ""
        dql_query = generate_dql_query_with_spans(trace_span_pairs)
    else:
        trace_ids = extract_trace_ids(log_content)
        if not trace_ids:
            print("Warning: No trace IDs found in the log file")
            return ""
        dql_query = generate_dql_query(trace_ids)
    
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(dql_query)
            print(f"DQL query written to: {output_file}")
        except Exception as e:
            raise Exception(f"Error writing output file: {e}")
    
    return dql_query


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Extract trace IDs from log files and generate DQL queries"
    )
    parser.add_argument(
        "input_file",
        help="Path to the input log file"
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        help="Optional path to output file (prints to stdout if not provided)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--include-spans", "-s",
        action="store_true",
        help="Include span IDs in the output (format: T-{trace-id},S-{span-id})"
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    output_path = Path(args.output_file) if args.output_file else None
    
    try:
        dql_query = process_log_file(input_path, output_path, args.include_spans)
        
        if not args.output_file:
            print(dql_query)
        
        if args.verbose:
            log_content = input_path.read_text(encoding='utf-8')
            if args.include_spans:
                trace_span_pairs = extract_trace_and_span_pairs(log_content)
                print(f"Found {len(trace_span_pairs)} unique trace/span pairs", file=sys.stderr)
            else:
                trace_ids = extract_trace_ids(log_content)
                print(f"Found {len(trace_ids)} unique trace IDs", file=sys.stderr)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()