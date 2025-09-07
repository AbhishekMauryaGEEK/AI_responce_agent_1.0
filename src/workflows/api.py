from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/research', methods=['POST'])
def conduct_research():
    try:
        data = request.get_json()
        topic = data.get('topic')
        num_sources = data.get('num_sources', 10)
        citation_style = data.get('citation_style', 'apa')
        
        # Initialize research components
        searcher = WebSearcher(api_key, search_engine_id)
        extractor = ContentExtractor()
        summarizer = AISummarizer()
        citation_manager = CitationManager(style=citation_style)
        
        # Perform research pipeline
        search_results = searcher.search(topic, num_sources)
        urls = [result.get('link') for result in search_results]
        articles = extractor.extract_multiple(urls)
        
        # Generate summary and citations
        summary = summarizer.synthesize_multiple(articles, topic)
        
        sources = []
        for i, article in enumerate(articles, 1):
            citation_id = citation_manager.add_source(article, i)
            sources.append({
                'id': citation_id,
                'title': article['title'],
                'url': article['url'],
                'authors': article['authors'],
                'publish_date': article['publish_date'].isoformat() if article['publish_date'] else None
            })
        
        return jsonify({
            'summary': summary,
            'sources': sources,
            'topic': topic,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/pdf', methods=['POST'])
def export_pdf():
    """Generate PDF report"""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    data = request.get_json()
    
    # Create PDF using ReportLab
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Add content to PDF
    p.drawString(100, 750, f"Research Report: {data['topic']}")
    p.drawString(100, 720, f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
    
    y_position = 680
    p.drawString(100, y_position, "Summary:")
    y_position -= 30
    
    # Add summary (word wrap needed for production)
    summary_lines = data['summary'][:500].split('\n')
    for line in summary_lines:
        p.drawString(120, y_position, line)
        y_position -= 20
    
    p.save()
    
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return Response(
        pdf_data,
        mimetype='application/pdf',
        headers={'Content-Disposition': 'attachment; filename=research_report.pdf'}
    )

if __name__ == '__main__':
    app.run(debug=True)
