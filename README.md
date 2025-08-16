# Steam Scraper Competition Edition

A robust, production-ready Steam game data scraper built for competitive programming and data analysis projects. This scraper efficiently collects comprehensive game data from Steam using official APIs with proper rate limiting, error handling, and data validation.

## 🚀 Features

- **Comprehensive Data Collection**: Scrapes all Steam games with detailed metadata
- **Robust Error Handling**: Handles rate limits, network issues, and API failures gracefully
- **Rolling Window Fix**: Implements proper time-based rolling windows for rate limiting
- **Modular Architecture**: Clean, maintainable code structure
- **Data Validation**: Ensures data quality and consistency
- **Multiple Export Formats**: JSON, CSV, and Excel support
- **Resume Capability**: Checkpoint system to resume interrupted scraping
- **Configurable**: Easy-to-modify settings for different use cases

## 📊 Data Collected

- Game metadata (name, description, genres, tags)
- Pricing information (current price, discounts, currency)
- Release dates and developer information
- User review statistics and ratings
- System requirements and supported platforms
- DLC and package information
- Steam store metrics

## 🛠 Installation

```bash
# Clone the repository
git clone https://github.com/SeriogaRDC/steam-scraper-competition.git
cd steam-scraper-competition

# Install dependencies
pip install -r requirements.txt

# Run the scraper
python src/main.py
```

## 📖 Usage

### Basic Usage
```python
from src.steam_scraper import SteamScraper

scraper = SteamScraper()
scraper.scrape_all_games()
```

### Advanced Configuration
```python
from src.steam_scraper import SteamScraper
from src.config import Config

config = Config(
    rate_limit_requests=150,  # Requests per 5-minute window
    checkpoint_interval=1000,  # Save progress every N games
    output_format='json',
    include_dlc=False
)

scraper = SteamScraper(config)
scraper.scrape_all_games()
```

## 🏗 Architecture

```
src/
├── main.py              # Entry point
├── steam_scraper.py     # Main scraper class
├── api_client.py        # Steam API client with rate limiting
├── data_processor.py    # Data validation and processing
├── rolling_window.py    # Fixed rolling window implementation
├── config.py           # Configuration management
└── utils.py            # Utility functions

tests/
├── test_scraper.py     # Unit tests for scraper
├── test_api_client.py  # API client tests
└── test_rolling_window.py  # Rolling window tests

data/
├── raw/                # Raw scraped data
├── processed/          # Cleaned and processed data
└── checkpoints/        # Resume points
```

## 🔧 Configuration

Edit `src/config.py` to customize:
- Rate limiting parameters
- Output formats and locations
- Data filtering options
- Checkpoint intervals
- API endpoints

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_rolling_window.py -v
```

## 📈 Performance

- Handles ~200,000 Steam games efficiently
- Respects Steam's rate limits (200 requests per 5 minutes)
- Memory-efficient streaming processing
- Automatic retry logic with exponential backoff
- Estimated completion time: 2-3 days for full catalog

## 🏆 Competition Ready

This scraper is optimized for competitive programming and data science competitions:
- Clean, readable code structure
- Comprehensive documentation
- Robust error handling
- Efficient data processing
- Easy to extend and modify

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues or questions, please open a GitHub issue or contact the maintainer.