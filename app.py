#!/usr/bin/env python3
"""
Trace ID Helper Web Application

A Flask web interface for the trace ID extraction tool.
"""

import os
import tempfile
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
import io

# Import the existing trace ID extraction functions
from trace_id_extractor import (
    extract_trace_ids,
    extract_trace_and_span_pairs,
    generate_dql_query,
    generate_dql_query_with_spans
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


@app.route('/')
def index():
    """Main page with the UI."""
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_log():
    """Process log content and return DQL query."""
    try:
        # Get form data
        include_spans = request.form.get('include_spans') == 'true'
        verbose = request.form.get('verbose') == 'true'
        
        # Get log content from either file upload or text input
        log_content = ""
        
        if 'log_file' in request.files and request.files['log_file'].filename:
            # File upload
            file = request.files['log_file']
            if file.filename != '':
                log_content = file.read().decode('utf-8')
        
        if not log_content and 'log_text' in request.form:
            # Text input
            log_content = request.form['log_text']
        
        if not log_content:
            return jsonify({
                'success': False,
                'error': 'Please provide log content either by uploading a file or pasting text.'
            })
        
        # Process the log content
        if include_spans:
            trace_span_pairs = extract_trace_and_span_pairs(log_content)
            if not trace_span_pairs:
                return jsonify({
                    'success': False,
                    'error': 'No trace/span pairs found in the log content. Please check the format.'
                })
            dql_query = generate_dql_query_with_spans(trace_span_pairs)
            count = len(trace_span_pairs)
            count_type = "trace/span pairs"
        else:
            trace_ids = extract_trace_ids(log_content)
            if not trace_ids:
                return jsonify({
                    'success': False,
                    'error': 'No trace IDs found in the log content. Please check the format.'
                })
            dql_query = generate_dql_query(trace_ids)
            count = len(trace_ids)
            count_type = "unique trace IDs"
        
        response_data = {
            'success': True,
            'dql_query': dql_query,
            'count': count,
            'count_type': count_type
        }
        
        if verbose:
            response_data['verbose_info'] = f"Found {count} {count_type}"
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error processing log content: {str(e)}'
        })


@app.route('/download')
def download_query():
    """Download the DQL query as a file."""
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Create a file-like object in memory
    output = io.StringIO()
    output.write(query)
    output.seek(0)
    
    # Convert to bytes
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    
    return send_file(
        mem,
        as_attachment=True,
        download_name='trace_query.dql',
        mimetype='text/plain'
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)