# StupidCerts - Certificate Scraper

StupidCerts is a PyQt5-based application that automates the process of scraping PFX certificates from the GrayHat Warfare Buckets API over a specified number of days. It simplifies downloading and basic processing of certificates.

## Features

- **API Integration:** Connects with GrayHat Warfare Buckets API to fetch and download PFX files.
- **Certificate Download:** Downloads certificates filtered by the last modified date.
- **User Interface:** Simple PyQt5 GUI for easy interaction.
- **Logging:** Real-time log updates within the GUI.

## Requirements

- Python 3.6+
- PyQt5
- requests

## Installation

Before running the application, ensure that all dependencies are installed:

```bash
pip install PyQt5 requests
```

## Running the Application

To run the application, execute the Python script:

```bash
python stupidcerts_app.py
```

Ensure that you replace `stupidcerts_app.py` with the actual filename if it differs.

## GUI Elements

- **API Key Input:** Enter your API key for GrayHat Warfare Buckets API.
- **Days Input:** Specify the number of days to look back for certificates.
- **Start Search Button:** Begins the scraping process.
- **Log Output:** Displays real-time logs of the application's operations.

## Project Structure

```plaintext
stupidcerts_app.py      Main application script for running the GUI and handling operations.
```

## Usage

1. **Start the Application:** Run the script to open the GUI.
2. **Input API Key:** Enter your API key in the 'API Key' field.
3. **Specify Days:** Input the number of days in the 'Days' field.
4. **Start Search:** Click on 'Start Search' to begin the process.
5. **View Logs:** Watch the logs for updates and errors in real-time.

## Troubleshooting

If you encounter any issues:
- Ensure your API key is valid and active.
- Check your internet connection for any disruptions.
- Ensure all dependencies are correctly installed.

## Contributing

Contributions to StupidCerts are welcome. Please feel free to fork the repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

---

### Explanation and Tips

- **Clear and Concise Descriptions:** Each section of the README is designed to give users clear and concise information about what the project does, how to set it up, and how to use it.
- **Formatting and Structure:** The README is formatted for easy reading, with clear headings and a logical flow from installation instructions to usage tips.
- **Usage Instructions:** Detailed step-by-step usage instructions help new users get started without confusion.
- **Troubleshooting:** A simple troubleshooting section addresses potential common issues to help users solve problems on their own.

This README is a comprehensive guide that should help any user to understand and use your application effectively.
