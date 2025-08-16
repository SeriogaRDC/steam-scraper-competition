"""
Main entry point for the Steam Scraper Competition Edition.
Simple interface for running the scraper with sensible defaults.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from steam_scraper import SteamScraper


def main():
    """Main entry point with competition-optimized settings."""
    print("🎮 Steam Scraper - Competition Edition")
    print("=" * 50)
    
    # Create optimized configuration for competition use
    config = Config(
        # Conservative rate limiting to avoid issues
        rate_limit_requests=150,
        rate_limit_window=300,
        request_delay=1.2,
        
        # Frequent checkpoints for safety
        checkpoint_interval=500,
        
        # Skip non-essential content for speed
        include_dlc=False,
        include_software=False,
        
        # JSON output for flexibility
        output_format='json',
        
        # Validation enabled for data quality
        validate_data=True,
        skip_invalid_games=True,
        
        # Logging for monitoring
        log_level='INFO'
    )
    
    print(f"📊 Configuration:")
    print(f"   Rate limit: {config.rate_limit_requests} requests per {config.rate_limit_window}s")
    print(f"   Output format: {config.output_format}")
    print(f"   Checkpoints every: {config.checkpoint_interval} games")
    print(f"   Include DLC: {config.include_dlc}")
    print(f"   Data validation: {config.validate_data}")
    print()
    
    # Create and run scraper
    scraper = SteamScraper(config)
    
    try:
        print("🚀 Starting scraping process...")
        print("   This may take several hours to complete")
        print("   Progress will be saved automatically")
        print("   Press Ctrl+C to stop gracefully")
        print()
        
        output_path = scraper.scrape_all_games(resume=True)
        
        print()
        print("✅ Scraping completed successfully!")
        print(f"📁 Data exported to: {output_path}")
        print()
        
        # Show final statistics
        progress_info = scraper.get_progress_info()
        stats = progress_info['stats']
        
        print("📈 Final Statistics:")
        print(f"   Total apps processed: {stats['processed_apps']:,}")
        print(f"   Successful: {stats['successful_apps']:,}")
        print(f"   Failed: {stats['failed_apps']:,}")
        print(f"   Success rate: {(stats['successful_apps']/max(1, stats['processed_apps']))*100:.1f}%")
        
        api_stats = progress_info['api_stats']
        print(f"   API requests made: {api_stats['requests_made']:,}")
        print(f"   API success rate: {api_stats['success_rate']:.1f}%")
        
        return output_path
        
    except KeyboardInterrupt:
        print("\n⏹️  Interrupted by user")
        scraper.stop_gracefully()
        print("💾 Progress saved. You can resume later by running the script again.")
        return None
        
    except Exception as e:
        print(f"\n❌ Scraping failed: {e}")
        print("💾 Check logs for details. Any progress has been saved.")
        raise


if __name__ == "__main__":
    main()