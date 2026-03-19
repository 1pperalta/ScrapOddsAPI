"""
RAG Retrieval Service

Handles retrieval of team context from Chroma vector database.
Provides contextual information for the betting analysis agent.
"""

import sys
from pathlib import Path

# Add scrapping directory to path for config imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.append(str(project_root))

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional

from scrapping.rag.config import CHROMA_DB_PATH, CHROMA_COLLECTION_NAME
from .embedding_service import get_embedding_service


class RAGService:
    """Service for retrieving team context from vector database"""
    
    def __init__(self):
        self.embedding_service = get_embedding_service()
        
        # Initialize Chroma client
        self.chroma_client = chromadb.PersistentClient(
            path=str(CHROMA_DB_PATH),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get collection
        try:
            self.collection = self.chroma_client.get_collection(
                name=CHROMA_COLLECTION_NAME
            )
        except Exception as e:
            print(f"Warning: Collection not found. Run embedding_manager.py first. Error: {e}")
            self.collection = None
    
    def retrieve_team_context(self, team_name: str, top_k: int = 2) -> List[Dict]:
        """
        Retrieve context for a specific team
        
        Args:
            team_name: Name of the team
            top_k: Number of most relevant documents to retrieve
            
        Returns:
            List of context dictionaries with content, metadata, and similarity
        """
        if not self.collection:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_service.embed_query(team_name)
        
        # Search in Chroma
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            contexts = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    contexts.append({
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'similarity': 1 - results['distances'][0][i],  # Convert distance to similarity
                        'team': results['metadatas'][0][i].get('team', 'Unknown')
                    })
            
            return contexts
        except Exception as e:
            print(f"Error retrieving context for {team_name}: {e}")
            return []
    
    def retrieve_match_context(self, home_team: str, away_team: str, top_k_per_team: int = 2) -> Dict:
        """
        Retrieve context for both teams in a match
        
        Args:
            home_team: Name of home team
            away_team: Name of away team
            top_k_per_team: Number of documents to retrieve per team
            
        Returns:
            Dictionary with home_context and away_context
        """
        home_context = self.retrieve_team_context(home_team, top_k=top_k_per_team)
        away_context = self.retrieve_team_context(away_team, top_k=top_k_per_team)
        
        return {
            'home_team': home_team,
            'away_team': away_team,
            'home_context': home_context,
            'away_context': away_context
        }
    
    def retrieve_by_league(self, league_name: str, top_k: int = 10) -> List[Dict]:
        """
        Retrieve teams from a specific league
        
        Args:
            league_name: Name of the league
            top_k: Number of teams to retrieve
            
        Returns:
            List of team contexts from that league
        """
        if not self.collection:
            return []
        
        try:
            # Query with league filter
            results = self.collection.query(
                query_embeddings=[self.embedding_service.embed_query(league_name)],
                n_results=top_k,
                where={"league": league_name},
                include=["documents", "metadatas"]
            )
            
            contexts = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    contexts.append({
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'team': results['metadatas'][0][i].get('team', 'Unknown')
                    })
            
            return contexts
        except Exception as e:
            print(f"Error retrieving league {league_name}: {e}")
            return []
    
    def format_context_for_prompt(self, contexts: List[Dict]) -> str:
        """
        Format retrieved contexts into a string suitable for LLM prompts
        
        Args:
            contexts: List of context dictionaries
            
        Returns:
            Formatted string with all context information
        """
        if not contexts:
            return "No hay contexto disponible para este equipo."
        
        formatted_parts = []
        
        for i, ctx in enumerate(contexts, 1):
            team = ctx.get('team', 'Unknown')
            content = ctx.get('content', '')
            
            # Extract key information for concise prompt
            lines = content.split('\n')
            key_info = '\n'.join(lines[:15])  # First 15 lines contain the most important info
            
            formatted_parts.append(f"--- Contexto {i}: {team} ---\n{key_info}")
        
        return '\n\n'.join(formatted_parts)
    
    def format_match_context_for_prompt(self, match_context: Dict) -> str:
        """
        Format match context (both teams) for LLM prompt
        
        Args:
            match_context: Dictionary with home_context and away_context
            
        Returns:
            Formatted string with both teams' context
        """
        home_team = match_context.get('home_team', 'Unknown')
        away_team = match_context.get('away_team', 'Unknown')
        
        prompt = f"CONTEXTO DEL PARTIDO: {home_team} vs {away_team}\n\n"
        
        # Home team context
        home_contexts = match_context.get('home_context', [])
        if home_contexts:
            prompt += f"=== {home_team.upper()} (LOCAL) ===\n"
            prompt += self.format_context_for_prompt(home_contexts[:1])  # Use top result
            prompt += "\n\n"
        
        # Away team context
        away_contexts = match_context.get('away_context', [])
        if away_contexts:
            prompt += f"=== {away_team.upper()} (VISITANTE) ===\n"
            prompt += self.format_context_for_prompt(away_contexts[:1])  # Use top result
        
        return prompt
    
    def get_collection_info(self) -> Dict:
        """Get information about the collection"""
        if not self.collection:
            return {
                'status': 'not_initialized',
                'count': 0
            }
        
        try:
            count = self.collection.count()
            metadata = self.collection.metadata
            
            return {
                'status': 'ready',
                'count': count,
                'metadata': metadata,
                'collection_name': CHROMA_COLLECTION_NAME
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }


# Global instance
_rag_service = None


def get_rag_service() -> RAGService:
    """Get or create the global RAG service instance"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service


def main():
    """Test RAG service"""
    service = get_rag_service()
    
    # Show collection info
    info = service.get_collection_info()
    print("Collection Info:")
    print(info)
    
    # Test team retrieval
    print("\nTesting team context retrieval:")
    team = "Arsenal"
    contexts = service.retrieve_team_context(team)
    
    if contexts:
        print(f"\nFound {len(contexts)} contexts for {team}")
        print("\nFormatted context:")
        print(service.format_context_for_prompt(contexts))
    else:
        print(f"No context found for {team}")
    
    # Test match retrieval
    print("\n" + "="*60)
    print("Testing match context retrieval:")
    match_ctx = service.retrieve_match_context("Arsenal", "Chelsea")
    print(service.format_match_context_for_prompt(match_ctx))


if __name__ == "__main__":
    main()

