# Trace ID Helper

A Python tool that extracts trace IDs from messy log data and generates DQL (Data Query Language) queries for log analysis.

## Overview

When dealing with application logs that contain distributed tracing information, it's often necessary to extract trace IDs and create queries to search for related log entries. This tool automates that process by parsing log files and generating properly formatted DQL queries.

## Features

- ✅ Extracts trace IDs from various log formats
- ✅ Handles messy, unstructured log data
- ✅ Removes duplicate trace IDs automatically
- ✅ Generates DQL queries with OR operators
- ✅ Command-line interface for easy automation
- ✅ Optional file output
- ✅ Verbose mode for debugging

## Installation

No installation required! Just ensure you have Python 3.6+ installed.

```bash
# Check Python version
python --version
```

## Usage

### Basic Usage

Extract trace IDs and print DQL query to stdout:

```bash
python trace_id_extractor.py your-log-file.txt
```

### Save to File

Extract trace IDs and save DQL query to a file:

```bash
python trace_id_extractor.py your-log-file.txt output-query.txt
```

### Verbose Mode

Get additional information about the extraction process:

```bash
python trace_id_extractor.py your-log-file.txt --verbose
```

### Include Span IDs

Include both trace IDs and span IDs in the output:

```bash
python trace_id_extractor.py your-log-file.txt --include-spans
```

## Examples

### Input Log Format

The tool recognizes trace IDs in the format `[T-{traceId},S-{spanId}]`:

```
2025-07-26 16:34:50.031 INFO  XxxxAdapter.lambda$afterBodyRead$0(): [http-nio-8080-exec-5] [T-a9f624eexxxxxxxx,S-a9f624eexxxxxxxx] :   [POST] /xxx/xx/xxxx
2025-07-26 16:34:50.060 INFO  XxxxAdapter.lambda$afterBodyRead$0(): [http-nio-8080-exec-4] [T-f0c8e2a8xxxxxxxx,S-f0c8e2a8xxxxxxxx] :   [POST] /xxx/xx/xxxx
```

### Output DQL Query

**Trace IDs only (default):**
```
("T-a9f624eexxxxxxxx" OR "T-f0c8e2a8xxxxxxxx")
```

**With span IDs (--include-spans):**
```
("T-a9f624eexxxxxxxx,S-a9f624eexxxxxxxx" OR "T-f0c8e2a8xxxxxxxx,S-f0c8e2a8xxxxxxxx")
```

### Real-world Example

```bash
# Extract trace IDs from application logs
python trace_id_extractor.py app-logs.txt

# Output:
("T-301fb981f95b9c81")

# Extract trace IDs with span IDs
python trace_id_extractor.py app-logs.txt --include-spans

# Output:
("T-301fb981f95b9c81,S-20662c2dfb736f38" OR "T-301fb981f95b9c81,S-40f75dca6424aa0d" OR "T-301fb981f95b9c81,S-9cf5b2b9a790087e" OR "T-301fb981f95b9c81,S-a3a075049a6053eb")

# Save query for later use
python trace_id_extractor.py app-logs.txt trace-query.dql

# Use verbose mode to see statistics
python trace_id_extractor.py app-logs.txt --include-spans --verbose
# Output:
("T-301fb981f95b9c81,S-20662c2dfb736f38" OR "T-301fb981f95b9c81,S-40f75dca6424aa0d" OR "T-301fb981f95b9c81,S-9cf5b2b9a790087e" OR "T-301fb981f95b9c81,S-a3a075049a6053eb")
Found 4 unique trace/span pairs
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `input_file` | Path to the input log file (required) |
| `output_file` | Optional path to save the DQL query |
| `--verbose`, `-v` | Enable verbose output with statistics |
| `--include-spans`, `-s` | Include span IDs in the output (format: T-{trace-id},S-{span-id}) |
| `--help`, `-h` | Show help message |

## Supported Log Formats

The tool uses regex pattern matching to find trace IDs in the format:
- `[T-{hexadecimal-trace-id},S-{hexadecimal-span-id}]`

Examples of supported formats:
```
[T-a9f624ee2e4f3c9b,S-a9f624ee2e4f3c9b]
[T-f0c8e2a82b6a2349,S-f0c8e2a82b6a2349]
[T-01ca3088195366d4,S-01ca3088195366d4]
```

## Use Cases

### Log Analysis
Extract trace IDs from application logs to create queries for log aggregation tools like Splunk, Elasticsearch, or Datadog.

### Debugging
Quickly generate queries to trace specific requests across distributed systems.

### Automation
Integrate into CI/CD pipelines or monitoring scripts to automatically extract trace information from log files.

## Error Handling

The tool handles common errors gracefully:

- **File not found**: Clear error message if input file doesn't exist
- **No trace IDs found**: Warning message if no trace IDs are detected
- **Permission errors**: Error message if unable to read/write files
- **Invalid format**: Continues processing, ignoring malformed entries

## Tips

1. **Large Files**: The tool loads the entire file into memory, so for very large files, consider splitting them first.

2. **Different Formats**: If your logs use a different trace ID format, you can modify the regex pattern in the script.

3. **Automation**: Use in scripts by redirecting output:
   ```bash
   python trace_id_extractor.py logs.txt > query.dql
   ```

4. **Batch Processing**: Process multiple files:
   ```bash
   for file in *.log; do
     python trace_id_extractor.py "$file" "${file%.log}.dql"
   done
   ```

## Troubleshooting

### Common Issues

**No output generated**
- Check if your log file contains trace IDs in the expected format
- Use `--verbose` mode to see if any trace IDs were found

**Permission denied**
- Ensure you have read permissions for the input file
- Ensure you have write permissions for the output directory

**Python not found**
- Make sure Python 3.6+ is installed and in your PATH
- Try using `python3` instead of `python`

## Contributing

This is a simple utility tool. If you need additional features or find bugs, feel free to modify the script according to your needs.

## License

This tool is provided as-is for educational and practical use.