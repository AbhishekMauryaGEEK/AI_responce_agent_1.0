from newspaper import Article
import requests
from datetime import datetime

class ContentExtractor:
    def __init__(self):
        self.extracted_articles = []
    
    def extract_article(self, url):
        """Extract content from a single URL"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            # Optional: Use NLP features
            article.nlp()
            
            return {
                'url': url,
                'title': article.title,
                'authors': article.authors,
                'publish_date': article.publish_date,
                'text': article.text,
                'summary': article.summary if hasattr(article, 'summary') else '',
                'keywords': article.keywords if hasattr(article, 'keywords') else [],
                'top_image': article.top_image,
                'extraction_time': datetime.now()
            }
        except Exception as e:
            print(f"Error extracting {url}: {e}")
            return None
    
    def extract_multiple(self, urls):
        """Extract content from multiple URLs"""
        articles = []
        for url in urls:
            article_data = self.extract_article(url)
            if article_data:
                articles.append(article_data)
        return articles

# Usage
extractor = ContentExtractor()
urls = [result.get('link') for result in search_results]
articles = extractor.extract_multiple(urls)
