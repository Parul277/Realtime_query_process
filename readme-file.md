# Data Query and Anomaly Removal System Using GenAI


## Overview
A Streamlit-based web application that combines automated data cleaning with natural language querying capabilities. This system helps users clean their CSV data and extract insights through conversational AI interactions powered by Azure OpenAI and LangChain.

## Features
- 🔍 Automated data quality assessment
- 🧹 Dynamic data cleaning and anomaly detection
- 💬 Natural language query interface
- 📊 Real-time data processing
- ⬇️ Cleaned data download functionality
- 🔒 Secure Azure OpenAI integration

## Prerequisites
```
Python 3.8+
Streamlit
pandas
numpy
scipy
Pillow
python-dotenv
langchain
langchain_experimental
```

## Installation


1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
OPENAI_API_KEY=your_api_key
DEPLOYMENT=your_deployment_name
OPENAI_API_VERSION=your_api_version
SERVICE_LINE=your_service_line
BRAND=your_brand
PROJECT=your_project
END_POINT=your_azure_endpoint
```

## Project Structure
```
├── query_process.py                # Main application file
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables
└── README.md             # Project documentation
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run query_process.py
```

2. Access the application through your web browser at `http://localhost:8501`

3. Upload your CSV file using the file uploader

4. Ask questions about your data using natural language

5. Download the cleaned dataset using the download button

## Features in Detail

### Data Cleaning
- Automatic handling of missing values
- Outlier detection and removal using Z-scores
- Data type standardization
- Statistical validation

### Query Interface
- Natural language processing using Azure OpenAI
- Context-aware responses
- Support for complex analytical queries
- Real-time processing

## API Integration

The system uses Azure OpenAI with custom headers:
```python
openai_headers = {
    'x-service-line': SERVICE_LINE,
    'x-brand': BRAND,
    'x-project': PROJECT,
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'api-version': 'v10',
    'Ocp-Apim-Subscription-Key': OPENAI_API_KEY,
}
```

## Development

### Setting Up Development Environment

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex operations
- Keep functions focused and modular

## Troubleshooting

Common issues and solutions:

1. **API Connection Issues**
   - Verify Azure OpenAI credentials
   - Check network connectivity
   - Ensure all environment variables are set

2. **File Upload Errors**
   - Verify CSV file format
   - Check file size limits
   - Ensure proper file permissions

3. **Processing Errors**
   - Check data format consistency
   - Verify memory availability
   - Review error logs in Streamlit

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
Parul Verma 
Nikhil Sethi
Project Link: [repository-url]

## Acknowledgments
- Azure OpenAI team
- LangChain community
- Streamlit framework
