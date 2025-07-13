import requests
import sys
import os
import zipfile
import shutil

def get_md_files(owner, repo):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Failed to fetch repo tree: {response.status_code} {response.text}")
        return []
    tree = response.json().get('tree', [])
    md_files = [item['path'] for item in tree if item['path'].lower().endswith('.md')]
    return md_files

def download_repo_zip(owner, repo, output_path=None):
    zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
    response = requests.get(zip_url, stream=True)
    if response.status_code != 200:
        print(f"Failed to download zip: {response.status_code} {response.text}")
        return None
    if output_path is None:
        output_path = f"{repo}-HEAD.zip"
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Repository zip downloaded to: {output_path}")
    return output_path

def extract_py_files_from_zip(zip_path, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.lower().endswith('.py'):
                # Remove the top-level folder from the path if present
                parts = file_info.filename.split('/', 1)
                rel_path = parts[1] if len(parts) > 1 else parts[0]
                target_path = os.path.join(target_dir, rel_path)
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with zip_ref.open(file_info) as source, open(target_path, 'wb') as target:
                    target.write(source.read())
    print(f"Extracted .py files to: {target_dir}")

def clean_zip_py_only(zip_path, output_zip_path=None):
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract all files
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        # Remove non-.py files
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if not file.lower().endswith('.py'):
                    os.remove(os.path.join(root, file))
        # Create new zip with only .py files
        if output_zip_path is None:
            base = os.path.splitext(os.path.basename(zip_path))[0]
            output_zip_path = f"cleaned_{base}.zip"
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
        print(f"Cleaned zip with only .py files created at: {output_zip_path}")

def create_final_zip(folder_to_zip, output):
    """Create a zip file from the specified folder."""
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_to_zip):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_to_zip)
                zipf.write(file_path, arcname)
    print(f"Final zip file created at: {output}")

def fetch_clean_zip(owner, repo, working_dir):
    """
    Orchestrates the process of downloading a GitHub repo, extracting only .py files, and creating a cleaned zip file.
    Args:
        owner (str): GitHub username or org
        repo (str): Repository name
        working_dir (str): Directory to use for staging temporary files
    Returns:
        str: Path to the cleaned zip file
    """
    import tempfile
    import os

    # Ensure working_dir exists
    os.makedirs(working_dir, exist_ok=True)

    # Step 1: Download repo zip
    repo_zip_path = os.path.join(working_dir, f"{repo}-HEAD.zip")
    download_repo_zip(owner, repo, repo_zip_path)

    # Step 2: Extract only .py files to a temp folder inside working_dir
    py_extract_dir = os.path.join(working_dir, "py_files")
    extract_py_files_from_zip(repo_zip_path, py_extract_dir)

    # Step 3: Create a cleaned zip with only .py files
    cleaned_zip_path = os.path.join(working_dir, f"cleaned_{repo}.zip")
    create_final_zip(py_extract_dir, cleaned_zip_path)

    print(f"Orchestration complete. Cleaned zip at: {cleaned_zip_path}")
    return cleaned_zip_path

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python get_md_files_from_github.py <owner> <repo> <action> [output_zip_path]")
        print("<action>: 'fetch-clean-zip' to download a repo, extract only .py files, and create a cleaned zip file.")
        sys.exit(1)
    owner = sys.argv[1]
    repo = sys.argv[2]
    action = sys.argv[3]
    if action == 'fetch-clean-zip':
        if len(sys.argv) < 5:
            print("Usage: python get_md_files_from_github.py <owner> <repo> fetch-clean-zip <working_dir>")
            sys.exit(1)
        working_dir = sys.argv[4]
        fetch_clean_zip(owner, repo, working_dir)
    else:
        print("Unknown action. Use 'list-md' or 'download-zip' or 'extract-py' or 'clean-zip' or 'create-final-zip' or 'fetch-clean-zip'.")
        sys.exit(1) 

    # python3 get_files_from_github.py rafaporci sample_classifieds_api fetch-clean-zip working-dir/