"""
Configuration management for Steam Scraper.
Centralized configuration with validation and environment variable support.
"""

import os
from typing import Optional, List
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    """Configuration class for Steam Scraper with sensible defaults."""
    
    # API Configuration
    steam_api_base: str = "https://api.steampowered.com"
    steam_store_api: str = "https://store.steampowered.com/api"
    
    # Rate Limiting (Steam allows ~200 requests per 5 minutes)
    rate_limit_requests: int = 180  # Conservative limit
    rate_limit_window: int = 300    # 5 minutes in seconds
    request_delay: float = 1.0      # Minimum delay between requests
    
    # Retry Configuration
    max_retries: int = 5
    retry_delay: float = 2.0
    backoff_multiplier: float = 2.0
    
    # Data Processing
    checkpoint_interval: int = 1000  # Save progress every N games
    batch_size: int = 100           # Process games in batches
    include_dlc: bool = False       # Include DLC in scraping
    include_software: bool = False  # Include software/tools
    
    # Output Configuration
    output_format: str = "json"     # json, csv, excel
    output_dir: Path = field(default_factory=lambda: Path("data"))
    raw_data_dir: Path = field(default_factory=lambda: Path("data/raw"))
    processed_data_dir: Path = field(default_factory=lambda: Path("data/processed"))
    checkpoint_dir: Path = field(default_factory=lambda: Path("data/checkpoints"))
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = "steam_scraper.log"
    
    # Data Validation
    validate_data: bool = True
    skip_invalid_games: bool = True
    
    # Currency and Language
    currency: str = "USD"
    language: str = "english"
    country_code: str = "US"
    
    def __post_init__(self):
        """Create directories and validate configuration."""
        # Create output directories
        for directory in [self.output_dir, self.raw_data_dir, 
                         self.processed_data_dir, self.checkpoint_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Load from environment variables if available
        self._load_from_env()
        
        # Validate configuration
        self._validate()
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_mappings = {
            'STEAM_RATE_LIMIT': ('rate_limit_requests', int),
            'STEAM_OUTPUT_FORMAT': ('output_format', str),
            'STEAM_CURRENCY': ('currency', str),
            'STEAM_LANGUAGE': ('language', str),
            'STEAM_LOG_LEVEL': ('log_level', str),
        }
        
        for env_var, (attr_name, type_func) in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                setattr(self, attr_name, type_func(value))
    
    def _validate(self):
        """Validate configuration values."""
        if self.rate_limit_requests <= 0:
            raise ValueError("rate_limit_requests must be positive")
        
        if self.rate_limit_window <= 0:
            raise ValueError("rate_limit_window must be positive")
        
        if self.output_format not in ['json', 'csv', 'excel']:
            raise ValueError("output_format must be 'json', 'csv', or 'excel'")
        
        if self.checkpoint_interval <= 0:
            raise ValueError("checkpoint_interval must be positive")
    
    @classmethod
    def from_file(cls, config_path: str) -> 'Config':
        """Load configuration from a file (future enhancement)."""
        # This could be implemented to load from YAML/JSON config files
        return cls()
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return {
            field.name: getattr(self, field.name) 
            for field in self.__dataclass_fields__.values()
        }