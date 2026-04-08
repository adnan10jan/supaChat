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
    
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if not gemini_key:
        print("GEMINI_API_KEY is not set. Cannot summarize logs with AI.")
        return
    
    print("Summarizing logs with Google Gemini...")
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        payload = {
            "contents": [{
                "parts": [{"text": "You are a DevOps assistant. Summarize the following Docker Compose logs, point out any errors, and explain possible root causes:\n\n" + logs[:4000]}]
            }]
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={
            'Content-Type': 'application/json'
        })
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            content = res_data['candidates'][0]['content']['parts'][0]['text']
        
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
