# OSINT-Recon Tool

![Alt text](spy.png)

An automated OSINT (Open Source Intelligence) reconnaissance tool that uses Google dorking techniques to gather publicly
available information about domains and individuals.

## Features

- **106 Pre-built Dorks**: Comprehensive collection of Google dorks for both domain and person reconnaissance
- **Domain Intelligence**: Discover files, configurations, admin panels, APIs, subdomains, and more
- **Person Intelligence**: Find social profiles, documents, contact information, work history, and public records
- **Web Crawler**: Recursively crawl discovered URLs to find additional links
- **Proxy Support**: Rotate through proxies to distribute requests
- **Robot.txt Compliance**: Optionally respect website robots.txt rules
- **Multiple Output Formats**: Save results as JSON or TXT
- **Color-coded CLI**: Easy-to-read terminal output

## Installation

### Prerequisites

- Python 3.7+
- Google Custom Search API Key and CX (Search Engine ID)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd osint-recon
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CX=your_search_engine_id_here
```

### Getting Google API Credentials

1. **Get API Key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable "Custom Search API"
   - Create credentials (API Key)

2. **Get CX (Search Engine ID)**:
   - Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
   - Create a new search engine
   - Configure it to search the entire web
   - Copy the Search Engine ID (CX)

## Usage

### Basic Commands

```bash
# Display banner and help
python osint.py

# List all available dorks
python osint.py --list

# Run a domain-based dork
python osint.py -t github.com -d 5

# Run a person-based dork
python osint.py -t "John Doe" -d 63

# Show detailed help
python osint.py -h
```

### Advanced Usage

```bash
# Use crawler with depth 2
python osint.py -t example.com -d 5 --crawl --depth 2

# Use proxy rotation
python osint.py -t example.com -d 5 -p

# Save results to JSON
python osint.py -t example.com -d 5 -o results.json

# Save results to TXT
python osint.py -t example.com -d 5 -o results.txt

# Ignore robots.txt (use responsibly)
python osint.py -t example.com -d 5 --crawl --no-robots

# Limit maximum results
python osint.py -t example.com -d 5 --max-results 20
```

## Dork Categories

### Domain-Based Dorks (1-50)

- **Files**: PDFs, Word docs, spreadsheets, presentations
- **Configs**: ENV files, backups, config files, logs
- **Database**: SQL dumps, database backups
- **WebApp**: Login pages, admin panels, APIs, CMS detection
- **Infrastructure**: Subdomains, cloud storage (S3, Azure)
- **Secrets**: GitHub leaks, credentials
- **Intel**: Job postings, tech stack, security policies

### Person-Based Dorks (51-106)

- **Documents**: Resumes, publications, academic papers
- **Social Media**: LinkedIn, Twitter, Facebook, GitHub
- **Contact**: Email addresses, phone numbers, locations
- **Media**: Photos, videos, presentations
- **Professional**: Work history, skills, certifications
- **Background**: Education, affiliations, legal records


## Command-Line Options

| Option | Description |
|--------|-------------|
| `-t, --target` | Target domain or person name |
| `-d, --dork` | Dork number (1-106) |
| `-l, --list` | List all available dorks |
| `--crawl` | Enable crawler on found URLs |
| `-p, --use-proxy` | Use proxy rotation |
| `-o, --output` | Save results to file (JSON or TXT) |
| `--depth` | Crawler depth (default: 1) |
| `--no-robots` | Ignore robots.txt restrictions |
| `--max-results` | Maximum results to fetch (default: 10) |

## Examples

### Example 1: Find ENV Files
```bash
python osint.py -t example.com -d 5
```

### Example 2: LinkedIn Profile Search
```bash
python osint.py -t "Jane Smith" -d 63
```

### Example 3: Deep Crawl with Proxies
```bash
python osint.py -t example.com -d 11 --crawl --depth 3 -p -o scan_results.json
```

### Example 4: API Endpoint Discovery
```bash
python osint.py -t api.example.com -d 15 --crawl
```

## Legal Disclaimer

This tool is designed for:
- **Educational purposes**: Learning about OSINT techniques
- **Security research**: Authorized penetration testing
- **Legitimate reconnaissance**: With proper authorization

**Important**:
- Only use on domains/people you have permission to research
- Respect privacy laws and terms of service
- Be aware of rate limits and robots.txt
- This tool only searches publicly available information
- Users are responsible for how they use this tool

## Responsible Use Guidelines

1. **Get Permission**: Always obtain authorization before scanning domains you don't own
2. **Respect Rate Limits**: Use appropriate delays between requests
3. **Follow robots.txt**: Don't use `--no-robots` without good reason
4. **Privacy First**: Be ethical when researching individuals
5. **Legal Compliance**: Follow all applicable laws and regulations

## Troubleshooting

### No Results Found
- Check your API key and CX in `.env` file
- Verify the target format is correct
- Try a different dork
- Check if you've exceeded API quota

### Proxy Issues
- Free proxies often fail - this is normal
- The tool will fall back to direct connection
- Consider using paid proxy services for reliability

### Crawler Timeout
- Reduce crawler depth
- Some sites may block automated requests
- Use proxies to distribute requests

## Contributing

Contributions are welcome! Areas for improvement:


## API Rate Limits

Google Custom Search API free tier:
- 100 queries per day
- 10 results per query maximum

Consider upgrading for production use.

## Dependencies

- `requests`: HTTP library
- `beautifulsoup4`: HTML parsing
- `python-dotenv`: Environment variable management

## License

This project is for educational purposes. Use responsibly and ethically.

## Future Enhancements

- [ ] Multi-threaded crawling
- [ ] Support for other search engines (Bing, DuckDuckGo)
- [ ] PDF parsing for deeper analysis
- [ ] Database integration
- [ ] Web dashboard
- [ ] Email notifications
- [ ] Screenshot capture
- [ ] Wayback Machine integration

