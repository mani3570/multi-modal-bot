# Multi-Modal Chatbot

## Overview

The Multi-Modal Chatbot is a Python application that takes images as input and utilizes the Gemini API to process and respond to the input. This bot leverages Google's Gemini API for advanced image processing capabilities.

## Prerequisites

1. **Install Poetry**:
   Poetry is a dependency management tool for Python. If you don't have Poetry installed, you can install it using:
   ```bash
   pip install poetry
   ```

2. **Obtain API Keys**:
   - **Google API Key**: You'll need a Google API key for authentication. Add your API key to the environment variables:
     ```plaintext
     GOOGLE_API_KEY="AIzaSyDbakXj-------------"
     ```
   - **Gemini API Key**: Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Setup

1. **Clone the Repository**:
   First, clone the repository to your local machine:
   ```bash
   git clone https://github.com/mani3570/multi-modal-bot.git
   cd multi-modal-bot
   ```

2. **Install Dependencies**:
   Use Poetry to install the project's dependencies:
   ```bash
   poetry install
   ```

3. **Activate the Virtual Environment**:
   Enter the Poetry-managed virtual environment:
   ```bash
   poetry shell
   ```

## Running the Bot

To start the chatbot, use the following command:
```bash
python app.py
```

## Usage

The bot is designed to process images and make use of the Gemini API for its operations. Ensure that your environment variables are properly set and that the required API keys are configured before running the bot.

## Contributing

If you'd like to contribute to the development of this project, please fork the repository and submit a pull request with your changes.
