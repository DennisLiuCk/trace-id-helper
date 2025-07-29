# Trace ID Helper

A Python tool that extracts trace IDs from messy log data and generates DQL (Data Query Language) queries for log analysis.

## Overview

When dealing with application logs that contain distributed tracing information, it's often necessary to extract trace IDs and create queries to search for related log entries. This tool automates that process by parsing log files and generating properly formatted DQL queries.

## Features

- ✅ Extracts trace IDs from various log formats
- ✅ Handles messy, unstructured log data
- ✅ Removes duplicate trace IDs automatically
- ✅ Generates DQL queries with OR operators
- ✅ **NEW: Web UI for user-friendly interaction**
- ✅ Command-line interface for easy automation
- ✅ Optional file output
- ✅ Verbose mode for debugging
- ✅ Copy to clipboard and download functionality
- ✅ Toggle options for include spans and verbose mode

## Installation

### For Web UI (Recommended)

1. Ensure you have Python 3.6+ installed:
   ```bash
   python3 --version
   ```

2. Install Flask dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Start the web interface:
   ```bash
   ./start_ui.sh
   # or manually: python3 app.py
   ```

4. Open your browser and go to [http://localhost:5000](http://localhost:5000)

### For Command Line Only

No installation required! Just ensure you have Python 3.6+ installed.

```bash
# Check Python version
python --version
```

## Usage

### Web UI (Recommended for most users)

The easiest way to use the Trace ID Helper is through the web interface:

1. **Start the web server:**
   ```bash
   ./start_ui.sh
   ```

2. **Open your browser** and navigate to [http://localhost:5000](http://localhost:5000)

3. **Upload a log file** or **paste log content** directly into the text area

4. **Configure options:**
   - Toggle "Include Span IDs" to include both trace and span IDs in the output
   - Toggle "Verbose Mode" to see extraction statistics

5. **Click "Generate DQL Query"** to process your logs

6. **Copy or download** the generated DQL query

### Command Line Interface

Extract trace IDs and print DQL query to stdout:

```bash
python trace_id_extractor.py your-log-file.txt
```

#### Save to File

Extract trace IDs and save DQL query to a file:

```bash
python trace_id_extractor.py your-log-file.txt output-query.txt
```

#### Verbose Mode

Get additional information about the extraction process:

```bash
python trace_id_extractor.py your-log-file.txt --verbose
```

#### Include Span IDs

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

## Web UI Features

The web interface provides a user-friendly way to interact with the trace ID extraction tool:

### 🌟 Key Features
- **Drag & Drop or Paste**: Upload log files or paste content directly
- **Real-time Processing**: Instant DQL query generation
- **Toggle Options**: Easy switches for span IDs and verbose mode
- **Copy to Clipboard**: One-click copying of generated queries
- **Download Results**: Save DQL queries as `.dql` files
- **Clear Guidelines**: Built-in instructions and examples
- **Responsive Design**: Works on desktop and mobile devices

### 📱 User Interface
- **Clean, modern design** with intuitive controls
- **Step-by-step guidance** for new users
- **Example log format** shown for reference
- **Error handling** with helpful feedback messages
- **Visual feedback** for all user actions

### 🔧 Technical Details
- Built with **Flask** web framework
- **No database required** - stateless processing
- **Lightweight** - minimal dependencies
- **Cross-platform** - runs on Windows, macOS, Linux

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