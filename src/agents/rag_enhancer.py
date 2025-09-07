import chromadb
from sentence_transformers import SentenceTransformer

class RAGEnhancer:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection("research_articles")
    
    def add_articles_to_db(self, articles):
        """Store articles in vector database"""
        documents = []
        metadatas = []
        ids = []
        
        for i, article in enumerate(articles):
            documents.append(article['text'])
            metadatas.append({
                'title': article['title'],
                'url': article['url'],
                'authors': ', '.join(article['authors']) if article['authors'] else 'Unknown'
            })
            ids.append(f"article_{i}")
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query_relevant_context(self, query, n_results=5):
        """Retrieve relevant context for query"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return {
            'documents': results['documents'][0],
            'metadatas': results['metadatas'][0]
        }

# Enhanced summarization with RAG
def rag_enhanced_summary(topic, articles, query_context=None):
    rag = RAGEnhancer()
    rag.add_articles_to_db(articles)
    
    # Get relevant context
    context = rag.query_relevant_context(topic)
    
    # Combine with existing summarization
    enhanced_prompt = f"""
    Topic: {topic}
    
    Relevant Context:
    {' '.join(context['documents'][:3])}
    
    Generate a comprehensive research summary.
    """
    
    summarizer = AISummarizer()
    return summarizer.summarize_text(enhanced_prompt)
