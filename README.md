# Document Refresher

This project provides a Python script to retrieve all Markdown (.md) files from a given public GitHub repository, or to download the repository as a zip file.

## Requirements

- Python 3.7 or higher
- `requests` library (see `requirements.txt`)

## Installation

1. Clone this repository or download the script.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line:

```bash
python get_md_files_from_github.py <owner> <repo> <action> [output_zip_path]
```

- `<owner>`: GitHub username or organization
- `<repo>`: Repository name
- `<action>`: `list-md` to list Markdown files, `download-zip` to download the repository as a zip file
- `[output_zip_path]`: (Optional) Path to save the downloaded zip file (only for `download-zip` action)

### Examples

**List all Markdown files in the `torvalds/linux` repository:**
```bash
python get_md_files_from_github.py torvalds linux list-md
```

**Download the `torvalds/linux` repository as a zip file:**
```bash
python get_md_files_from_github.py torvalds linux download-zip
```

**Download and save the zip file to a custom path:**
```bash
python get_md_files_from_github.py torvalds linux download-zip ./linux_repo.zip
```

## Output

- For `list-md`, the script prints the paths of all Markdown files found in the repository.
- For `download-zip`, the script downloads the repository as a zip file to the specified or default location. 