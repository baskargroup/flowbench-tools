# Example: Downloading a Folder from Our Repository

**License:** cc-by-nc-4.0

Below is an example of downloading a folder from our repository.

## Installation

To run the example code, you need to install the following package:

```bash
pip install huggingface_hub
```

## Example Code

The following script demonstrates how to download a directory from the Hugging Face Hub:

```python 
from huggingface_hub import HfApi, hf_hub_download
import os
import shutil

REPO_ID = "BGLab/FlowBench"
DIRECTORY = "LDC_NS_2D"

# Initialize the Hugging Face API
api = HfApi()

# List files in the directory
files_list = api.list_repo_files(repo_id=REPO_ID, repo_type="dataset")

# Filter the files in the specified directory
files_to_download = [f for f in files_list if f.startswith(DIRECTORY)]

# Create local directory if it doesn't exist
os.makedirs(DIRECTORY, exist_ok=True)

# Download each file
for file in files_to_download:
    file_path = hf_hub_download(repo_id=REPO_ID, filename=file, repo_type="dataset")
    # Copy the file to the local directory using shutil.copy2
    shutil.copy2(file_path, os.path.join(DIRECTORY, os.path.basename(file_path)))

print("Files downloaded successfully.")

```

