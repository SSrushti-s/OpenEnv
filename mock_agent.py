import requests
import time

# The address of your running FastAPI server
BASE_URL = "http://127.0.0.1:7860"

def run_mock_agent():
    print("🚀 Starting Mock Agent (Free Version)...")
    
    # 1. Reset the environment to get the initial emails
    response = requests.get(f"{BASE_URL}/reset")
    if response.status_code != 200:
        print("❌ Error: Is your server running? Run 'python server/app.py' first.")
        return
    
    obs = response.json()
    inbox = obs["inbox"]
    
    print(f"📥 Received {len(inbox)} emails.")
    
    # 2. Loop through the emails and take action
    for email in inbox:
        print(f"\n--- Analyzing Email ID: {email['id']} ---")
        print(f"From: {email['sender']} | Subject: {email['subject']}")
        
        # MOCK AI LOGIC:
        # If it's from 'spam.com', delete it.
        # Otherwise, archive it.
        if "spam.com" in email["sender"]:
            action = {"command": "delete", "email_id": email["id"]}
            print("🤖 Decision: This looks like SPAM. Action: DELETE")
        else:
            action = {"command": "archive", "email_id": email["id"]}
            print("🤖 Decision: This looks LEGIT. Action: ARCHIVE")
        
        # 3. Send the action to the server
        step_response = requests.post(f"{BASE_URL}/step", json=action)
        
        # The server returns [Observation, Reward]
        new_obs, reward = step_response.json()
        
        print(f"🎯 Reward: {reward['reward']} | Feedback: {reward['comment']}")
        
        # Wait a second so we can watch it happen
        time.sleep(1)

    print("\n✅ All emails processed. Task Complete.")

if __name__ == "__main__":
    run_mock_agent()