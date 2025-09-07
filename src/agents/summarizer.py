from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration
import torch
class AISummarizer:
    def __init__(self, model_name="t5-base"):
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.summarizer = pipeline("summarization", 
                                 model=self.model, 
                                 tokenizer=self.tokenizer)
    
    def summarize_text(self, text, max_length=150, min_length=50):
        """Generate summary for a single text"""
        # T5 requires task prefix
        input_text = f"summarize: {text}"
        
        # Truncate if too long
        max_input_length = 512
        if len(input_text.split()) > max_input_length:
            input_text = ' '.join(input_text.split()[:max_input_length])
        
        summary = self.summarizer(input_text, 
                                max_length=max_length, 
                                min_length=min_length, 
                                do_sample=False)
        return summary[0]['summary_text']
    
    def synthesize_multiple(self, articles, topic):
        """Create a comprehensive summary from multiple articles"""
        combined_text = f"Research topic: {topic}\n\n"
        
        for i, article in enumerate(articles, 1):
            combined_text += f"Source {i}: {article['title']}\n"
            combined_text += f"Summary: {article['text'][:500]}...\n\n"
        
        return self.summarize_text(combined_text, max_length=300, min_length=100)
# Usage
summarizer = AISummarizer()
comprehensive_summary = summarizer.synthesize_multiple(articles, "AI Research Trends")
