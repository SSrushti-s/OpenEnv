import os
import openai
from models import EmailAction

# 1. Setup the Brain
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_baseline():
    # 2. Connect to our App (locally for testing)
    import requests
    base_url = "http://localhost:7860"
    
    print("--- Starting Baseline Run ---")
    obs = requests.get(f"{base_url}/reset").json()
    
    for i in range(5): # Limit to 5 actions
        print(f"Current Inbox: {obs['unread_count']} emails.")
        
        # 3. Ask GPT what to do
        prompt = f"You are an email assistant. Here is the inbox: {obs['inbox']}. What is your next action? Return ONLY JSON matching the EmailAction model."
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        
        # 4. Perform the action
        action_data = response.choices[0].message.content
        print(f"AI decided to: {action_data}")
        
        result = requests.post(f"{base_url}/step", data=action_data).json()
        obs = result[0] # New observation
        reward = result[1] # The score
        
        print(f"Reward: {reward['reward']} | {reward['comment']}")
        
        if reward['is_terminal']:
            break

if __name__ == "__main__":
    run_baseline()