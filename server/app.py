from fastapi import FastAPI
from server.environment import EmailTriageEnv
from models import EmailAction, EmailObservation, EmailReward

app = FastAPI(title="Email Triage OpenEnv")
env = EmailTriageEnv()

@app.post("/reset")
def reset() -> EmailObservation:
    """The AI calls this to start over."""
    return env.reset()

@app.post("/step")
def step(action: EmailAction) -> tuple[EmailObservation, EmailReward]:
    """The AI calls this to take an action."""
    return env.step(action)

@app.get("/state")
def state():
    """For the Grader to check the secret 'God-mode' status."""
    return env.state()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
