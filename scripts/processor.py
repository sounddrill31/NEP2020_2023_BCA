import os
import re
import frontmatter
import subprocess
import datetime
import sys

# --- Configuration ---
# This system prompt ensures the AI outputs the exact format you want.
SYSTEM_PROMPT = """
You are a technical academic assistant.
1. ACTION: specific answer to the user's prompt.
2. FORMATTING: 
   - Use Markdown. 
   - Use #### (H4) or ##### (H5) for headings. 
   - NEVER use # (H1), ## (H2), or ### (H3).
   - Do NOT use HTML tags (<div>, <span>) unless strictly necessary.
3. DIAGRAMS: 
   - Skip visual diagrams/ASCII art. 
   - You may use 'mermaid' code blocks for diagrams if they are simple.
4. TONE: Concise, technical, and direct.
5. CODE: Feel free to include snippets that are short enough to represent the answer. 
"""

def call_gh_model(prompt):
    """
    Sends ONLY the specific prompt string to GitHub Models/Copilot.
    """
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser Question: {prompt}"
    
    try:
        # We use 'gh model' to keep it within the free/beta tier constraints
        # Ensure 'gh extension install github/gh-models' is run in workflow
        cmd = ["gh", "model", "prompt", "-m", "gpt-4o-mini", full_prompt] 
        
        # Subprocess to catch stdout
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"API Error: {result.stderr}", file=sys.stderr)
            return f"> **Error:** AI generation failed. Details: {result.stderr}"
    except Exception as e:
        return f"> **Error:** Script failed to invoke AI. {str(e)}"

def process_file(filepath):
    # Load the file
    try:
        post = frontmatter.load(filepath)
    except Exception as e:
        print(f"Skipping {filepath}: invalid frontmatter")
        return

    content = post.content
    original_content = content
    
    # Regex to find: use-AI-here-please: "some text"
    # Capture group 1 is the prompt text inside the quotes.
    pattern = re.compile(r'use-AI-here-please:\s*"(.*?)"', re.IGNORECASE)
    
    # Find all matches
    matches = list(pattern.finditer(content))
    
    if not matches:
        print(f"No specific tags found in {filepath}")
        return

    print(f"Found {len(matches)} tags in {filepath}...")

    # Iterate backwards so replacing text doesn't mess up character indices of earlier matches
    for match in reversed(matches):
        prompt_text = match.group(1)
        full_match_text = match.group(0)
        
        print(f"  - Processing: '{prompt_text[:40]}...'")
        
        # 1. Call AI with ONLY the prompt text
        ai_response = call_gh_model(prompt_text)
        
        # 2. Build the Disclaimer
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        disclaimer = f"\n<sub>This was AI generated from github copilot on {date_str}</sub>"
        
        # 3. Create the replacement block
        # We add newlines to ensure markdown renders correctly
        replacement_block = f"\n{ai_response}\n{disclaimer}\n"
        
        # 4. PYTHON performs the substitution locally
        start_index, end_index = match.span()
        content = content[:start_index] + replacement_block + content[end_index:]

    # Save changes if modifications happened
    if content != original_content:
        post.content = content
        
        # Cleanup: Remove the trigger from frontmatter if no tags remain
        # (We check specifically for the tag string to ensure we didn't miss any)
        if "use-AI-here-please:" not in content:
            if 'use-AI-here-please' in post.metadata:
                del post.metadata['use-AI-here-please']
                print("  - Removed frontmatter trigger key.")

        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        print(f"  - File updated successfully.")

def main():
    # The workflow passes the target directory via env var
    target_dir = os.environ.get("TARGET_DIR", ".")
    print(f"Processor starting in: {target_dir}")
    
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".md"):
                fp = os.path.join(root, file)
                
                # Check for the clanker flag before opening heavy logic
                try:
                    with open(fp, 'r', encoding='utf-8') as f:
                        header = f.read(500) # Read just the top
                    if 'clanker: true' in header:
                        process_file(fp)
                except:
                    continue

if __name__ == "__main__":
    main()