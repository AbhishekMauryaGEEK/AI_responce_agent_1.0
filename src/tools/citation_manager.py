from datetime import datetime
import re
class CitationManager:
    def __init__(self, style='apa'):
        self.style = style
        self.citations = []
    
    def add_source(self, article_data, citation_id):
        """Add a source with automatic citation formatting"""
        citation = {
            'id': citation_id,
            'url': article_data['url'],
            'title': article_data['title'],
            'authors': article_data.get('authors', []),
            'publish_date': article_data.get('publish_date'),
            'domain': self.extract_domain(article_data['url']),
            'access_date': datetime.now().strftime('%Y-%m-%d')
        }
        self.citations.append(citation)
        return citation_id
    
    def format_citation(self, citation, style='apa'):
        """Format citation according to specified style"""
        if style.lower() == 'apa':
            return self.format_apa(citation)
        elif style.lower() == 'mla':
            return self.format_mla(citation)
        else:
            return self.format_basic(citation)
    
    def format_apa(self, citation):
        """APA style citation formatting"""
        authors = self.format_authors_apa(citation['authors'])
        date = citation['publish_date'].strftime('(%Y, %B %d)') if citation['publish_date'] else '(n.d.)'
        title = citation['title']
        domain = citation['domain']
        url = citation['url']
        
        return f"{authors} {date}. {title}. {domain}. {url}"
    
    def format_mla(self, citation):
        """MLA style citation formatting"""
        authors = self.format_authors_mla(citation['authors'])
        title = f'"{citation["title"]}"'
        domain = citation['domain']
        date = citation['publish_date'].strftime('%d %b %Y') if citation['publish_date'] else 'n.d.'
        url = citation['url']
        
        return f"{authors}. {title} {domain}, {date}, {url}."
    
    def format_authors_apa(self, authors):
        if not authors:
            return "Anonymous"
        if len(authors) == 1:
            return authors[0]
        elif len(authors) <= 7:
            return ", ".join(authors[:-1]) + f", & {authors[-1]}"
        else:
            return ", ".join(authors[:6]) + ", ... " + authors[-1]
    
    def extract_domain(self, url):
        """Extract domain name from URL"""
        match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        return match.group(1) if match else 'Unknown Source'
# Usage
citation_manager = CitationManager(style='apa')
for i, article in enumerate(articles, 1):
    citation_id = citation_manager.add_source(article, i)
