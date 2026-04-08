import argparse
import subprocess
import os
import urllib.request
import json

def restart_containers():
    print("Restarting all containers...")
    subprocess.run(["docker-compose", "restart"])

def summarize_logs():
    print("Fetching last 100 lines of logs...")
    result = subprocess.run(["docker-compose", "logs", "--tail=100"], capture_output=True, text=True)
    logs = result.stdout
    
    gemini_key = os.environ.get("GEMINI_API_KEY", "AIzaSyDUC4l1tJZnhxHx-pS7xHgFmhOJi1jELYQ")
    if not gemini_key:
        print("GEMINI_API_KEY is not set. Cannot summarize logs with AI.")
        return
    genai.configure(api_key=gemini_key)
    
    print("Summarizing logs with OpenAI...")
    try:
        OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        if not OPENAI_API_KEY:
            print("OPENAI_API_KEY is not set!")
            return
            
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": "You are a DevOps assistant. Summarize the following Docker Compose logs, point out any errors, and explain possible root causes."},
                {"role": "user", "content": logs[:4000]}
            ]
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}'
        })
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            content = res_data['choices'][0]['message']['content']
        
        print("--- AI Summary ---")
        print(content)
    except Exception as e:
        print(f"Failed to summarize logs via AI: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SupaChat DevOps Agent")
    parser.add_argument("action", choices=["restart", "summarize"], help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == "restart":
        restart_containers()
    elif args.action == "summarize":
        summarize_logs()
