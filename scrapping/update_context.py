"""
RAG Context Update Script

Convenient script to run the complete RAG update pipeline:
1. Collect team data from Football-Data.org API
2. Build documents from the collected data
3. Generate embeddings
4. Store in Chroma vector database

Usage:
    python update_context.py              # Full update
    python update_context.py --skip-collect  # Skip data collection, only update embeddings
    python update_context.py --clear      # Clear existing embeddings before update
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from rag.context_collector import ContextCollector
from rag.embedding_manager import EmbeddingManager


def main():
    parser = argparse.ArgumentParser(description="Update RAG context data and embeddings")
    parser.add_argument(
        '--skip-collect',
        action='store_true',
        help='Skip data collection, only update embeddings from existing JSON files'
    )
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear existing embeddings before update'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("RAG Context Update Pipeline")
    print("="*60)
    
    # Step 1: Collect data from API
    if not args.skip_collect:
        print("\n[1/2] Collecting team data from Football-Data.org API...")
        print("-"*60)
        
        try:
            collector = ContextCollector()
            collector.collect_all_leagues()
            print("\nData collection complete!")
        except Exception as e:
            print(f"\nError during data collection: {e}")
            print("Continuing with existing data...")
    else:
        print("\n[1/2] Skipping data collection (using existing JSON files)")
    
    # Step 2: Generate and store embeddings
    print("\n[2/2] Generating embeddings and updating vector database...")
    print("-"*60)
    
    try:
        manager = EmbeddingManager()
        manager.update_all_embeddings(clear_existing=args.clear)
        print("\nEmbedding update complete!")
        
        # Show final stats
        print("\n" + "="*60)
        print("Update Summary")
        print("="*60)
        manager.get_collection_stats()
        
    except Exception as e:
        print(f"\nError during embedding update: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "="*60)
    print("RAG system is ready!")
    print("You can now use the agent with enhanced context.")
    print("="*60)


if __name__ == "__main__":
    main()

