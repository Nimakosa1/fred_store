# Fred's Store

A modern e-commerce platform built with FastAPI, featuring MCP (Model Context Protocol) integration for enhanced AI capabilities.

## Features

- User Management
- Product Catalog
- Order Processing
- Subscription Management
- MCP Integration
- RESTful API
- Interactive API Documentation

## Quick Start

For detailed setup instructions, please see [GETTING_STARTED.txt](GETTING_STARTED.txt)

```bash
# Clone the repository
git clone https://github.com/[your-username]/fred_store.git
cd fred_store

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app:app --host 0.0.0.0 --port 5002 --reload
```

## API Documentation

Once the server is running, visit:
- http://localhost:5002/docs - Swagger UI
- http://localhost:5002/redoc - ReDoc UI

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 