import os
import frontmatter
import json
import sys

def scan_files():
    matrix_data = {}
    
    # Walk through the directory
    for root, dirs, files in os.walk("."):
        if ".git" in root or ".github" in root:
            continue
            
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                try:
                    # Load frontmatter to check for triggers
                    post = frontmatter.load(filepath)
                    
                    if post.get('clanker') is True and "use-AI-here-please" in post.content:
                        # Normalize path to handle Windows/Linux separators
                        norm_path = os.path.normpath(filepath)
                        parts = norm_path.split(os.sep)
                        
                        # Expected Structure: 3rdsem / SubjectName / Type / file.md
                        # We want to group by Subject (parts[0]/parts[1])
                        if len(parts) >= 2:
                            semester = parts[0]  # e.g., 3rdsem
                            subject = parts[1]   # e.g., Computer-Communications-Networks
                            
                            # Unique key for the Pull Request
                            key = f"{semester}/{subject}"
                            
                            if key not in matrix_data:
                                matrix_data[key] = {
                                    "category": semester,
                                    "subcategory": subject,
                                    # Use the path up to the subject so we scan recursively inside the subject
                                    "path": os.path.join(semester, subject)
                                }
                except Exception as e:
                    print(f"Error parsing {filepath}: {e}", file=sys.stderr)

    output_list = list(matrix_data.values())
    output_json = json.dumps(output_list)
    
    # Debug print to see what it found
    print(f"Generated Matrix: {output_json}")
    
    # Append to GITHUB_OUTPUT environment file
    if os.getenv('GITHUB_OUTPUT'):
        with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
            f.write(f"matrix={output_json}\n")

if __name__ == "__main__":
    scan_files()