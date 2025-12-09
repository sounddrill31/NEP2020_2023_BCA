import os
import re
import frontmatter
import datetime
import sys
from openai import OpenAI

# --- Configuration ---
# GitHub Models Endpoint
ENDPOINT = "https://models.github.ai/inference"
# Using gpt-4o-mini as it is efficient and less likely to hit strict rate limits than full GPT-4
MODEL_NAME = "openai/gpt-4o-mini" 

SYSTEM_PROMPT = """
You are a technical academic assistant.
1. ACTION: Answer the user's specific prompt accurately.
2. FORMATTING: 
   - Use Markdown. 
   - Use #### (H4) or ##### (H5) for headings. 
   - NEVER use # (H1), ## (H2), or ### (H3).
   - Do NOT use HTML tags unless strictly necessary.
3. DIAGRAMS: 
   - Skip visual diagrams/ASCII art. 
   - You are encouraged to use 'mermaid' code blocks for simple diagrams especially if it increases the quality of the answer.
   - You may use any diagram type supported by vitepress-plugin-mermaid like Default flowcharts, Pie chart, Gantt Chart, Mindmap.
4. TONE: Concise, technical, and direct. Explain simplistically while using accurate terms.
5. LENGTH: Generally short. Keep it easy for a student to refer and write without increasing too much burden.
6. CODE: Keep shiki compatibility in mind for code highlighting. If algorithms is a core focus of the code, generate time and space complexity in correct LaTeX form. 
"""

def get_ai_client():
    """
    Initializes the OpenAI client pointing to GitHub Models.
    Requires GITHUB_TOKEN in environment variables.
    """
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN or GH_TOKEN not found.", file=sys.stderr)
        return None

    return OpenAI(
        base_url=ENDPOINT,
        api_key=token,
    )

def call_github_model(client, prompt):
    """
    Sends ONLY the specific prompt string to GitHub Models using OpenAI SDK.
    """
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.7, # Slightly lower for more academic/consistent results
            top_p=1.0,
            max_tokens=1000, # Safety cap to prevent large output eating into rate limits
            model=MODEL_NAME
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"API Error: {e}", file=sys.stderr)
        return f"> **Error:** AI generation failed. Details: {str(e)}"

def process_file(client, filepath):
    try:
        post = frontmatter.load(filepath)
    except Exception as e:
        print(f"Skipping {filepath}: invalid frontmatter")
        return

    content = post.content
    original_content = content
    
    # Regex to find: use-AI-here-please: "some text"
    pattern = re.compile(r'use-AI-here-please:\s*"(.*?)"', re.IGNORECASE)
    matches = list(pattern.finditer(content))
    
    if not matches:
        return

    print(f"Found {len(matches)} tags in {filepath}...")

    # Iterate backwards for safe substitution
    for match in reversed(matches):
        prompt_text = match.group(1)
        
        print(f"  - Processing: '{prompt_text[:40]}...'")
        
        # 1. Call AI
        ai_response = call_github_model(client, prompt_text)
        
        # 2. Build Disclaimer
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        disclaimer = f"\n<sub>This was AI generated from github copilot on {date_str}</sub>"
        
        # 3. Create Replacement
        replacement_block = f"\n{ai_response}\n{disclaimer}\n"
        
        # 4. Substitute
        start, end = match.span()
        content = content[:start] + replacement_block + content[end:]

    # Save changes if any
    if content != original_content:
        post.content = content
        
        # Cleanup frontmatter if all tags are gone
        if "use-AI-here-please:" not in content:
            if 'use-AI-here-please' in post.metadata:
                del post.metadata['use-AI-here-please']

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        print(f"  - File updated successfully.")

def main():
    target_dir = os.environ.get("TARGET_DIR", ".")
    print(f"Processor starting in: {target_dir}")
    
    # Initialize Client once
    client = get_ai_client()
    if not client:
        sys.exit(1)
    
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".md"):
                fp = os.path.join(root, file)
                
                # Light check for clanker flag
                try:
                    with open(fp, 'r', encoding='utf-8') as f:
                        header = f.read(500)
                    if 'clanker: true' in header:
                        process_file(client, fp)
                except:
                    continue

if __name__ == "__main__":
    main()