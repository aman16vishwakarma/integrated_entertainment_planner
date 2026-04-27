from engine.llm_client import LLMClient
from engine.vector_store import VectorStore
from engine.prompts import PROMPT_TEMPLATES

class ContentPipeline:
    def __init__(self):
        self.llm = LLMClient()
        self.db = VectorStore()
        self.history = {}

    def run_stage(self, stage, inputs):
        """Runs a specific stage of the pipeline."""
        context = self.db.search_context(f"Previous content for {stage}")
        
        template = PROMPT_TEMPLATES[stage]
        prompt = template.format(**inputs)
        
        if context:
            full_prompt = f"Background Context from previous stages:\n{context}\n\nNew Task:\n{prompt}"
        else:
            full_prompt = prompt

        output = self.llm.generate(full_prompt)
        
        if "Error" not in output and stage not in ["critic"]:
            self.db.add_content(output, stage)
            self.history[stage] = output
        
        return output

    def run_agentic_scene(self, outline, characters, max_iterations=2):
        """Agentic Loop: Writer generates, Critic evaluates, Writer revises."""
        import streamlit as st # To show agentic thoughts in UI
        
        # 1. Initial Draft (Writer)
        st.toast("🕵️ Writer Agent is drafting the scene...")
        scene = self.run_stage('scene', {'outline': outline, 'characters': characters})
        
        for i in range(max_iterations):
            # 2. Evaluation (Critic)
            st.toast(f"🧐 Critic Agent is reviewing (Attempt {i+1})...")
            critique = self.run_stage('critic', {'scene': scene})
            
            if "APPROVED" in critique.upper():
                st.toast("✅ Critic APPROVED the scene!")
                break
            else:
                st.toast(f"❌ Critic REJECTED. Rewriting... Feedback: {critique[:50]}...")
                # 3. Rewrite (Writer)
                scene = self.run_stage('rewrite', {'scene': scene, 'feedback': critique})
        
        return scene

    def run_planner(self, content):
        """Planner Agent: Extracts production details."""
        return self.run_stage('planner', {'content': content})


    def run_full_pipeline(self, base_idea, genre, tone):
        results = {}
        
        # 1. Concept
        results['concept'] = self.run_stage('concept', {'idea': base_idea, 'genre': genre, 'tone': tone})
        
        # 2. Logline
        results['logline'] = self.run_stage('logline', {'concept': results['concept']})
        
        # 3. Pitch
        results['pitch'] = self.run_stage('pitch', {'concept': results['concept'], 'logline': results['logline']})
        
        # 4. Outline
        results['outline'] = self.run_stage('outline', {'pitch': results['pitch']})
        
        # 5. Characters
        results['characters'] = self.run_stage('characters', {'outline': results['outline']})
        
        # 6. Scene (Agentic Loop)
        results['scene'] = self.run_agentic_scene(results['outline'], results['characters'])
        
        # 7. Production Planner (Agentic Extraction)
        results['planner'] = self.run_planner(results['scene'])
        
        return results
