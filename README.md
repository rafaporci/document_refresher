# Document Refresher

This project provides a Python script to retrieve all Markdown (.md) files from a given public GitHub repository, or to download the repository as a zip file.

## Requirements

- Python 3.7 or higher
- see `requirements.txt`

## Installation

- python3 -m venv venv 
- source venv/bin/activate    
- python3 -m pip install -r requirements.txt

## Running 

- create a loadvars.sh from loadvars.sh.dist
- source loadvars.sh
- python3 get_files_from_github.py rafaporci sample_classifieds_api fetch-clean-zip working-dir/
- python3 documentation_analyzer.py


