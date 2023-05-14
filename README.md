# Chatbot

This is a chatbot experiment repo. Using streamlit. 

What it will be doing. - Might need backend server to run this.
1. scrapes all data from a client website and save key data into a file system
2. connect various data sources and create a knowledge graph including key data above
3. lanchain agent base chatbot. It answers based on the knowledge graph
4. provide all available data to the web visitors using chat interface
5. also, could respond any email inquiries using langchain

## Getting Started

### Prerequisites

- Python 3.8
- pip

## Installation
    python3.8 -m venv venv
    source venv/bin/activate
    make install


## Run
    streamlit run app.py


# Pelican static site

## Getting started
- Pelican[Markdown]

### Prerequisites
* Start venv
* Install Pelican[Markdown]

### Generate website
1. Change to site
2. Run > pelican /content

### Run Pelican server
1. pelican --listen
