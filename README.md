# Documentation Refresher

This project implements RAG search over a code base to recommend documentation updates using OpenAI API.

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


