

# @title 🌐 Task 3: Web-Search Agent - Real-time Information
# @markdown Simulated real-time web search with multiple sources

class WebSearchAgent:
    def __init__(self):
        self.search_history = []
        self.mock_sources = {
            "technology": ["Tech News Daily", "AI Research Hub", "Future Tech Review"],
            "science": ["Science Journal", "Research Weekly", "Academic Insights"],
            "health": ["Medical Today", "Health Digest", "Wellness Report"],
            "business": ["Business Times", "Market Watch", "Economic Review"],
            "general": ["Global News", "Information Network", "Knowledge Base"]
        }
    
    async def mock_web_search(self, query: str, num_results: int = 3) -> List[Dict]:
        """Enhanced mock web search with realistic data"""
        await asyncio.sleep(1)  # Simulate API delay
        
        # Categorize query for relevant sources
        category = self._categorize_query(query)
        sources = self.mock_sources.get(category, self.mock_sources["general"])
        
        current_time = datetime.now()
        results = []
        
        for i in range(num_results):
            results.append({
                'title': f'{query} - Latest Updates #{i+1}',
                'link': f'https://{sources[i].lower().replace(" ", "")}.com/{query.replace(" ", "-")}',
                'snippet': f'Recent developments in {query}. New research shows significant progress in this area. Current data updated {current_time.strftime("%Y-%m-%d")}.',
                'source': sources[i],
                'date': current_time.strftime("%Y-%m-%d %H:%M"),
                'relevance_score': round(0.9 - (i * 0.1), 2),
                'category': category
            })
        
        self.search_history.append({"query": query, "results": len(results), "timestamp": current_time})
        return results
    
    def _categorize_query(self, query: str) -> str:
        """Categorize query for relevant source selection"""
        query_lower = query.lower()
        if any(word in query_lower for word in ['ai', 'tech', 'computer', 'software']):
            return "technology"
        elif any(word in query_lower for word in ['health', 'medical', 'disease', 'treatment']):
            return "health"
        elif any(word in query_lower for word in ['business', 'market', 'economic', 'finance']):
            return "business"
        elif any(word in query_lower for word in ['science', 'research', 'study', 'academic']):
            return "science"
        else:
            return "general"
    
    async def get_real_time_response(self, user_prompt: str) -> Dict:
        """Provide real-time response using simulated web search"""
        print(f"🔍 Searching for: {user_prompt}")
        
        # Simulate multiple concurrent searches
        search_results = await self.mock_web_search(user_prompt, 4)
        
        # Synthesize results
        synthesized = self._synthesize_results(user_prompt, search_results)
        
        return {
            "user_query": user_prompt,
            "search_results": search_results,
            "synthesized_response": synthesized,
            "search_metadata": {
                "total_results": len(search_results),
                "sources_used": list(set([r['source'] for r in search_results])),
                "freshness": "current",
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def _synthesize_results(self, query: str, results: List[Dict]) -> Dict:
        """Synthesize multiple search results into coherent response"""
        key_findings = []
        for i, result in enumerate(results[:3], 1):
            key_findings.append(f"Source {i} ({result['source']}): Recent updates show progress in {query}")
        
        return {
            "comprehensive_answer": f"Based on real-time search across {len(results)} sources, here's the latest information about '{query}'. Current data indicates ongoing developments and recent advancements in this field.",
            "key_findings": key_findings,
            "confidence_level": "high",
            "source_reliability": "verified multiple sources",
            "recommendations": [
                "Consider checking official sources for specific data",
                "Multiple perspectives confirm the current trends",
                "Recent updates suggest continued development"
            ]
        }

# Interactive Widget for Task 3
print("🌐 TASK 3: Web-Search Agent - Real-time Information")
print("Simulated real-time search with multiple sources")

web_search_query = widgets.Textarea(
    value='latest developments in quantum computing',
    placeholder='What would you like to search for?',
    description='Search:',
    layout=widgets.Layout(width='80%', height='60px')
)

web_search_button = widgets.Button(description="Search Real-time", button_style='warning')
web_search_output = widgets.Output()

async def on_web_search_click(b):
    with web_search_output:
        clear_output()
        agent = WebSearchAgent()
        response = await agent.get_real_time_response(web_search_query.value)
        
        print("🌐 REAL-TIME SEARCH RESULTS")
        print("=" * 60)
        print(f"📊 Query: {response['user_query']}")
        print(f"📈 Sources: {len(response['search_metadata']['sources_used'])}")
        print(f"🕒 Freshness: {response['search_metadata']['freshness']}")
        
        print(f"\n🎯 Synthesized Answer:")
        print(f"   {response['synthesized_response']['comprehensive_answer']}")
        
        print(f"\n🔍 Key Findings:")
        for finding in response['synthesized_response']['key_findings']:
            print(f"   • {finding}")
            
        print(f"\n📋 Individual Results:")
        for i, result in enumerate(response['search_results'], 1):
            print(f"   {i}. [{result['source']}] {result['title']}")
            print(f"      Relevance: {result['relevance_score']} | {result['date']}")

web_search_button.on_click(lambda b: asyncio.create_task(on_web_search_click(b)))
display(web_search_query, web_search_button, web_search_output)