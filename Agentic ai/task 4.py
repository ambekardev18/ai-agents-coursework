

# @title 📚 Task 4: RAG Agent - Deep Research & Document Analysis
# @markdown Advanced research with document retrieval and analysis

class RAGAgent:
    def __init__(self, knowledge_base: List[str] = None):
        self.knowledge_base = knowledge_base or self._load_default_knowledge()
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.document_vectors = None
        self.research_history = []
        self._build_vector_index()
    
    def _load_default_knowledge(self) -> List[str]:
        """Load default knowledge base for demonstration"""
        return [
            "Artificial Intelligence systems can process large amounts of data and identify patterns that humans might miss.",
            "Machine Learning algorithms improve their performance through training on datasets without explicit programming.",
            "Deep Learning uses neural networks with multiple layers to model complex patterns in data.",
            "Natural Language Processing enables computers to understand, interpret, and generate human language.",
            "Computer Vision allows machines to interpret and understand visual information from the world.",
            "Reinforcement Learning involves training models through reward-based systems and trial-and-error.",
            "Transformer architectures have revolutionized natural language processing with attention mechanisms.",
            "Ethical AI considers fairness, transparency, and accountability in artificial intelligence systems.",
            "AI applications include healthcare diagnostics, autonomous vehicles, and personalized recommendations.",
            "Large Language Models like GPT are trained on vast text corpora and can generate human-like text."
        ]
    
    def _build_vector_index(self):
        """Build vector index for semantic search"""
        if self.knowledge_base:
            self.document_vectors = self.vectorizer.fit_transform(self.knowledge_base)
            print(f"📊 Vector index built with {len(self.knowledge_base)} documents")
    
    def add_documents(self, documents: List[str]):
        """Add documents to knowledge base"""
        self.knowledge_base.extend(documents)
        self._build_vector_index()
    
    def retrieve_relevant_documents(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieve most relevant documents using semantic search"""
        if not self.knowledge_base:
            return []
        
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
        
        # Get top_k most similar documents
        top_indices = similarities.argsort()[-top_k:][::-1]
        relevant_docs = []
        
        for idx in top_indices:
            relevant_docs.append({
                'content': self.knowledge_base[idx],
                'similarity_score': round(similarities[idx], 3),
                'doc_id': idx
            })
        
        return relevant_docs
    
    def research_workflow(self, complex_query: str) -> Dict:
        """Complete RAG workflow for complex queries"""
        print(f"🚀 Starting research workflow: {complex_query}")
        
        # Step 1: Document retrieval
        relevant_docs = self.retrieve_relevant_documents(complex_query, top_k=4)
        
        # Step 2: Generate synthesized response
        response = self._generate_synthesized_response(complex_query, relevant_docs)
        
        # Step 3: Create research sub-tasks
        sub_tasks = self._create_research_sub_tasks(complex_query, relevant_docs)
        
        # Store research session
        self.research_history.append({
            'query': complex_query,
            'documents_used': len(relevant_docs),
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            "original_query": complex_query,
            "documents_retrieved": len(relevant_docs),
            "relevant_documents": relevant_docs,
            "synthesized_response": response,
            "research_sub_tasks": sub_tasks,
            "confidence_score": round(np.mean([doc['similarity_score'] for doc in relevant_docs]), 3)
        }
    
    def _generate_synthesized_response(self, query: str, documents: List[Dict]) -> Dict:
        """Generate synthesized response from documents"""
        if not documents:
            return {
                "answer": "No relevant documents found in knowledge base.",
                "key_insights": [],
                "confidence": "low"
            }
        
        # Create a comprehensive answer based on retrieved documents
        key_insights = []
        for i, doc in enumerate(documents[:3], 1):
            key_insights.append(f"Insight {i}: {doc['content'][:150]}... (Relevance: {doc['similarity_score']})")
        
        return {
            "comprehensive_answer": f"Based on analysis of {len(documents)} relevant documents, here's what we know about '{query}'. The retrieved information shows consistent patterns and verified knowledge in this domain.",
            "key_insights": key_insights,
            "sources_synthesized": len(documents),
            "confidence_level": "high" if len(documents) >= 2 else "medium"
        }
    
    def _create_research_sub_tasks(self, query: str, documents: List[Dict]) -> List[Dict]:
        """Create sub-tasks for deep research"""
        base_tasks = [
            {
                "task_id": 1,
                "description": "Deep technical analysis and validation",
                "priority": "high",
                "estimated_duration": "45 minutes",
                "resources": ["Technical papers", "Research databases"]
            },
            {
                "task_id": 2,
                "description": "Cross-reference with latest developments",
                "priority": "medium",
                "estimated_duration": "30 minutes",
                "resources": ["Recent publications", "Industry reports"]
            },
            {
                "task_id": 3,
                "description": "Prepare implementation guidelines",
                "priority": "medium",
                "estimated_duration": "25 minutes",
                "resources": ["Best practices", "Case studies"]
            }
        ]
        
        # Adjust tasks based on query complexity
        if len(documents) < 2:
            base_tasks.append({
                "task_id": 4,
                "description": "Expand knowledge base with additional sources",
                "priority": "high",
                "estimated_duration": "60 minutes",
                "resources": ["External databases", "Expert consultations"]
            })
        
        return base_tasks
    
    def visualize_knowledge_base(self):
        """Create visualization of knowledge base"""
        if not self.knowledge_base:
            return
        
        # Create simple visualization
        doc_lengths = [len(doc.split()) for doc in self.knowledge_base]
        categories = [f"Doc {i+1}" for i in range(len(self.knowledge_base))]
        
        fig = px.bar(x=categories, y=doc_lengths, 
                     title="Knowledge Base Document Analysis",
                     labels={'x': 'Documents', 'y': 'Word Count'})
        fig.show()

# Interactive Widget for Task 4
print("📚 TASK 4: RAG Agent - Deep Research & Document Analysis")
print("Advanced research with semantic search and task delegation")

rag_query = widgets.Textarea(
    value='How do machine learning and deep learning differ?',
    placeholder='Enter complex research question...',
    description='Research:',
    layout=widgets.Layout(width='80%', height='60px')
)

rag_button = widgets.Button(description="Start Research", button_style='success')
rag_output = widgets.Output()

def on_rag_click(b):
    with rag_output:
        clear_output()
        rag_agent = RAGAgent()
        
        print("🔬 RAG RESEARCH WORKFLOW")
        print("=" * 60)
        
        result = rag_agent.research_workflow(rag_query.value)
        
        print(f"📊 Research Results for: '{result['original_query']}'")
        print(f"📚 Documents Retrieved: {result['documents_retrieved']}")
        print(f"🎯 Overall Confidence: {result['confidence_score']}")
        
        print(f"\n🎯 SYNTHESIZED ANSWER:")
        print(f"   {result['synthesized_response']['comprehensive_answer']}")
        
        print(f"\n🔍 KEY INSIGHTS:")
        for insight in result['synthesized_response']['key_insights']:
            print(f"   • {insight}")
        
        print(f"\n📋 RESEARCH SUB-TASKS:")
        for task in result['research_sub_tasks']:
            print(f"   {task['task_id']}. [{task['priority'].upper()}] {task['description']}")
            print(f"      ⏱️ {task['estimated_duration']} | 📚 {', '.join(task['resources'][:2])}")
        
        print(f"\n📈 RETRIEVED DOCUMENTS (Top 3):")
        for i, doc in enumerate(result['relevant_documents'][:3], 1):
            print(f"   {i}. Score: {doc['similarity_score']} - {doc['content'][:100]}...")

rag_button.on_click(on_rag_click)
display(rag_query, rag_button, rag_output)

# Show knowledge base visualization
rag_agent = RAGAgent()
rag_agent.visualize_knowledge_base()