
# @title 📊 Task 2: Comparative Study - System vs User Prompts
# @markdown See the difference that system prompts make!

class ComparativeStudy:
    def __init__(self):
        self.agent = SimpleAgent()
    
    def user_prompt_only(self, user_prompt: str) -> StructuredResponse:
        """Response using only user prompt"""
        return self.agent.get_structured_response(user_prompt)
    
    def system_prompt_enhanced(self, user_prompt: str, system_prompt: str) -> StructuredResponse:
        """Response using system prompt + user prompt"""
        enhanced_prompt = f"CONTEXT: {system_prompt}\n\nQUESTION: {user_prompt}"
        return self.agent.get_structured_response(enhanced_prompt)
    
    def run_comparison(self, user_prompt: str, system_prompt: str):
        """Run comparative analysis with visualization"""
        user_only = self.user_prompt_only(user_prompt)
        system_enhanced = self.system_prompt_enhanced(user_prompt, system_prompt)
        
        # Create comparison visualization
        categories = ['Confidence Score', 'Key Points Count', 'Response Depth']
        user_scores = [user_only.confidence_score, len(user_only.key_points), len(user_only.summary)]
        system_scores = [system_enhanced.confidence_score, len(system_enhanced.key_points), len(system_enhanced.summary)]
        
        fig = go.Figure(data=[
            go.Bar(name='User Prompt Only', x=categories, y=user_scores, marker_color='blue'),
            go.Bar(name='System Enhanced', x=categories, y=system_scores, marker_color='green')
        ])
        
        fig.update_layout(
            title='Prompting Strategy Comparison',
            barmode='group',
            yaxis_title='Score',
            showlegend=True
        )
        
        return user_only, system_enhanced, fig

# Interactive Widget for Task 2
print("📊 TASK 2: Comparative Study - System vs User Prompts")
print("See how system prompts improve response quality!")

comparison_query = widgets.Textarea(
    value='What are the benefits of renewable energy?',
    placeholder='Enter your question here...',
    description='Query:',
    layout=widgets.Layout(width='80%', height='60px')
)

system_prompt = widgets.Textarea(
    value='You are an energy expert with 15 years experience. Provide detailed technical explanations with cost-benefit analysis and real-world examples.',
    placeholder='Enter system prompt here...',
    description='System:',
    layout=widgets.Layout(width='80%', height='60px')
)

compare_button = widgets.Button(description="Compare Responses", button_style='info')
comparison_output = widgets.Output()

def on_compare_click(b):
    with comparison_output:
        clear_output()
        study = ComparativeStudy()
        user_resp, system_resp, fig = study.run_comparison(comparison_query.value, system_prompt.value)
        
        print("🆚 COMPARISON RESULTS")
        print("=" * 60)
        
        print("\n🎯 USER PROMPT ONLY:")
        print(f"   Summary: {user_resp.summary}")
        print(f"   Confidence: {user_resp.confidence_score:.2f}")
        print(f"   Key Points: {len(user_resp.key_points)}")
        
        print("\n🚀 SYSTEM PROMPT ENHANCED:")
        print(f"   Summary: {system_resp.summary}")
        print(f"   Confidence: {system_resp.confidence_score:.2f}")
        print(f"   Key Points: {len(system_resp.key_points)}")
        
        print("\n📈 IMPROVEMENT ANALYSIS:")
        conf_improvement = system_resp.confidence_score - user_resp.confidence_score
        points_improvement = len(system_resp.key_points) - len(user_resp.key_points)
        
        print(f"   Confidence Improvement: {conf_improvement:+.2f}")
        print(f"   Additional Key Points: {points_improvement:+d}")
        print(f"   Enhancement: {'Significant' if conf_improvement > 0.1 else 'Moderate'}")
        
        # Show visualization
        fig.show()

compare_button.on_click(on_compare_click)

display(comparison_query, system_prompt, compare_button, comparison_output)
