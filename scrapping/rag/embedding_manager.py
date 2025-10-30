"""
Embedding Manager

Orchestrates the complete RAG pipeline:
1. Read JSON data
2. Build documents
3. Generate embeddings
4. Store in Chroma vector database
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

import chromadb
from chromadb.config import Settings
from typing import List
from datetime import datetime

from .config import CHROMA_DB_PATH, CHROMA_COLLECTION_NAME
from .context_builder import ContextBuilder

# Import embedding service from backend
from odds_agent.backend.server_py.services.embedding_service import get_embedding_service


class EmbeddingManager:
    """Manages the embedding pipeline and vector storage"""
    
    def __init__(self):
        self.context_builder = ContextBuilder()
        self.embedding_service = get_embedding_service()
        
        # Initialize Chroma client
        print(f"Initializing Chroma DB at: {CHROMA_DB_PATH}")
        self.chroma_client = chromadb.PersistentClient(
            path=str(CHROMA_DB_PATH),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            metadata={"description": "Team context for betting analysis"}
        )
        
        print(f"Collection '{CHROMA_COLLECTION_NAME}' ready")
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        try:
            self.chroma_client.delete_collection(name=CHROMA_COLLECTION_NAME)
            self.collection = self.chroma_client.create_collection(
                name=CHROMA_COLLECTION_NAME,
                metadata={"description": "Team context for betting analysis"}
            )
            print("Collection cleared")
        except Exception as e:
            print(f"Error clearing collection: {e}")
    
    def update_team_embedding(self, team_name: str):
        """Update embedding for a single team"""
        print(f"Updating embedding for {team_name}...")
        
        # Build document
        document = self.context_builder.build_team_document(team_name)
        
        if not document:
            print(f"  Failed to build document for {team_name}")
            return False
        
        # Generate embedding
        embedding = self.embedding_service.embed_text(document.page_content)
        
        # Create unique ID
        doc_id = f"{document.metadata['league_code']}_{team_name.lower().replace(' ', '_')}"
        
        # Check if document already exists
        try:
            existing = self.collection.get(ids=[doc_id])
            if existing['ids']:
                # Update existing document
                self.collection.update(
                    ids=[doc_id],
                    embeddings=[embedding],
                    documents=[document.page_content],
                    metadatas=[document.metadata]
                )
                print(f"  Updated {team_name}")
            else:
                raise ValueError("Not found")
        except:
            # Add new document
            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[document.page_content],
                metadatas=[document.metadata]
            )
            print(f"  Added {team_name}")
        
        return True
    
    def update_all_embeddings(self, clear_existing: bool = False):
        """Update embeddings for all teams"""
        print("\nStarting embedding update process...")
        print(f"Clear existing: {clear_existing}")
        
        if clear_existing:
            self.clear_collection()
        
        # Build all documents
        documents = self.context_builder.build_all_documents()
        
        if not documents:
            print("No documents to process")
            return
        
        print(f"\nProcessing {len(documents)} team documents...")
        
        # Prepare data for batch insertion
        ids = []
        embeddings = []
        contents = []
        metadatas = []
        
        for i, doc in enumerate(documents):
            if (i + 1) % 10 == 0:
                print(f"  Processing {i + 1}/{len(documents)}...")
            
            # Generate unique ID
            doc_id = f"{doc.metadata['league_code']}_{doc.metadata['team'].lower().replace(' ', '_')}"
            ids.append(doc_id)
            
            # Generate embedding
            embedding = self.embedding_service.embed_text(doc.page_content)
            embeddings.append(embedding)
            
            contents.append(doc.page_content)
            metadatas.append(doc.metadata)
        
        # Batch upsert to Chroma
        print("\nStoring embeddings in Chroma DB...")
        
        # Chroma has a batch size limit, so we'll chunk if needed
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            end_idx = min(i + batch_size, len(ids))
            batch_ids = ids[i:end_idx]
            batch_embeddings = embeddings[i:end_idx]
            batch_contents = contents[i:end_idx]
            batch_metadatas = metadatas[i:end_idx]
            
            try:
                self.collection.upsert(
                    ids=batch_ids,
                    embeddings=batch_embeddings,
                    documents=batch_contents,
                    metadatas=batch_metadatas
                )
                print(f"  Stored batch {i//batch_size + 1} ({len(batch_ids)} documents)")
            except Exception as e:
                print(f"  Error storing batch: {e}")
        
        # Verify storage
        count = self.collection.count()
        print(f"\nEmbedding update complete!")
        print(f"Total documents in collection: {count}")
        
        # Update metadata
        self.collection.modify(
            metadata={
                "description": "Team context for betting analysis",
                "last_updated": datetime.now().isoformat(),
                "total_teams": count
            }
        )
    
    def get_collection_stats(self):
        """Get statistics about the collection"""
        count = self.collection.count()
        metadata = self.collection.metadata
        
        print(f"\nCollection Statistics:")
        print(f"  Name: {CHROMA_COLLECTION_NAME}")
        print(f"  Total documents: {count}")
        print(f"  Metadata: {metadata}")
        
        return {
            "count": count,
            "metadata": metadata
        }


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage RAG embeddings")
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear existing embeddings before update'
    )
    parser.add_argument(
        '--team',
        type=str,
        help='Update specific team only'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show collection statistics'
    )
    
    args = parser.parse_args()
    
    manager = EmbeddingManager()
    
    if args.stats:
        manager.get_collection_stats()
    elif args.team:
        manager.update_team_embedding(args.team)
    else:
        manager.update_all_embeddings(clear_existing=args.clear)


if __name__ == "__main__":
    main()

