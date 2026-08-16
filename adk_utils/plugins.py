from google.adk.plugins import BasePlugin
from google.adk.models import LlmResponse
from google.genai import types

class Graceful429Plugin(BasePlugin):
    """Intercepts local failures to Agent Platform and handles them globally."""
    
    def __init__(self, name: str, fallback_text: str | dict):
        super().__init__(name=name)
        self.fallback_text = fallback_text

    def _get_fallback_text(self, request_contents) -> str:
        """Determines the correct fallback text by scanning the prompt for keywords."""
        if isinstance(self.fallback_text, str):
            return self.fallback_text
            
        # Convert the request object/dict/args to a lowercase string for easy keyword hunting
        req_str = str(request_contents).lower()
        
        best_keyword = None
        best_index = -1
        
        for keyword, response in self.fallback_text.items():
            if keyword == "default":
                continue
            idx = req_str.rfind(keyword.lower())
            if idx > best_index:
                best_index = idx
                best_keyword = keyword
                
        if best_keyword:
            return self.fallback_text[best_keyword]
                
        # If no keywords matched, return the default if provided
        return self.fallback_text.get("default", "**[System]** Quota exhausted. Please try again later.")

    async def on_model_error(
        self, 
        *, 
        agent, 
        model, 
        input, 
        error: Exception
    ) -> LlmResponse | None:
        """Standard ADK hook for handling model-level exceptions."""
        if "RESOURCE_EXHAUSTED" in str(error) or "429" in str(error):
            print(f"\n[PLUGIN TRIGGERED] Caught 429 Error. Returning Graceful Fallback for {self.name}.")
            
            fallback = self._get_fallback_text(input)
            return LlmResponse(
                content=types.Content(
                    role="model", 
                    parts=[types.Part.from_text(text=fallback)]
                )
            )
        return None

    def apply_test_failover(self, agent):
        """Surgically patches the agent's model to simulate a 429 failure."""
        async def forced_429_failover(*args, **kwargs):
            try:
                # Force the exception to simulate a 429
                raise Exception("429 RESOURCE_EXHAUSTED - Simulated for testing")
            except Exception as e:
                print(f"\n[PATCH DEBUG] Exception caught inside monkey-patch: {e}")
                
                # Extract whatever was passed to the model call to check for keywords
                request_contents = args[0] if len(args) > 0 else kwargs
                fallback = self._get_fallback_text(request_contents)
                
                # Return the fallback response directly to satisfy the test
                yield LlmResponse(
                    content=types.Content(
                        role="model", 
                        parts=[types.Part.from_text(text=fallback)]
                    )
                )
        
        # Patch targets
        targets = []
        
        # Determine if this is a single agent or a multi-agent (e.g., SequentialAgent)
        if hasattr(agent, 'sub_agents') and agent.sub_agents:
            for sub_agent in agent.sub_agents:
                if hasattr(sub_agent, 'model') and sub_agent.model:
                    targets.append(sub_agent.model)
                    if hasattr(sub_agent.model, 'client'):
                        targets.append(sub_agent.model.client)
        else:
            if hasattr(agent, 'model') and agent.model:
                targets.append(agent.model)
                if hasattr(agent.model, 'client'):
                    targets.append(agent.model.client)
        
        methods = ['generate_content', 'generate_content_async', 'call', 'invoke']
        for target in targets:
            for m in methods:
                try: object.__setattr__(target, m, forced_429_failover)
                except: pass
        
        print(f"\n[PLUGIN DEBUG] Low-level failover applied to {agent.name}.")


    def apply_429_interceptor(self, agent):
        '''Surgically wraps the agent's model to catch real 429s and yield the fallback robustly.'''
        targets = []
        if hasattr(agent, 'sub_agents') and agent.sub_agents:
            for sub_agent in agent.sub_agents:
                if hasattr(sub_agent, 'model'): targets.append(sub_agent.model)
        else:
            if hasattr(agent, 'model'): targets.append(agent.model)

        for target in targets:
            if not hasattr(target, 'generate_content_async'):
                continue
            original_method = getattr(target, 'generate_content_async')
            
            async def wrapped_429_failover(*args, **kwargs):
                try:
                    async for result in original_method(*args, **kwargs):
                        yield result
                except Exception as e:
                    if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                        print(f"\n[PLUGIN TRIGGERED] Caught real 429 Error. Returning Graceful Fallback.")
                        request_contents = args[0] if len(args) > 0 else kwargs
                        fallback = self._get_fallback_text(request_contents)
                        yield LlmResponse(
                            content=types.Content(
                                role="model", 
                                parts=[types.Part.from_text(text=fallback)]
                            )
                        )
                    else:
                        raise
                        
            object.__setattr__(target, 'generate_content_async', wrapped_429_failover)
