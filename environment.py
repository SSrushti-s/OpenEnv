import random
from models import EmailObservation, EmailAction, EmailReward, EmailSnippet

class EmailTriageEnv:
    def __init__(self):
        # This is the "Secret State" the AI can't see directly
        self.secret_emails = []
        self.archive = []
        self.deleted = []
        self.step_count = 0
        self.max_steps = 10

    def reset(self) -> EmailObservation:
        """Starts a fresh session with new random emails."""
        self.step_count = 0
        self.archive = []
        self.deleted = []
        
        # Generate some mock data
        self.secret_emails = [
            {"id": 1, "sender": "boss@company.com", "subject": "Urgent Meeting", "body": "Need to talk now.", "priority": "high", "type": "work"},
            {"id": 2, "sender": "noreply@spam.com", "subject": "WIN CASH!", "body": "Click here for $$$", "priority": "low", "type": "spam"},
            {"id": 3, "sender": "mom@gmail.com", "subject": "Dinner Sunday?", "body": "Are you coming over?", "priority": "medium", "type": "social"},
        ]
        return self._get_observation()

    def _get_observation(self) -> EmailObservation:
        """Converts secret state into the public 'Snippet' view for the AI."""
        snippets = [
            EmailSnippet(
                id=e["id"], 
                sender=e["sender"], 
                subject=e["subject"], 
                body_preview=e["body"][:20] + "...", 
                priority=e["priority"],
                timestamp="2026-04-08 10:00 AM"
            ) for e in self.secret_emails
        ]
        return EmailObservation(inbox=snippets, unread_count=len(snippets))

    def step(self, action: EmailAction) -> tuple[EmailObservation, EmailReward]:
        self.step_count += 1
        reward_val = 0.0
        comment = "Action processed."
        
        # 1. Find the target email
        target = next((e for e in self.secret_emails if e["id"] == action.email_id), None)
        
        if not target:
            return self._get_observation(), EmailReward(reward=-0.5, comment="Email ID not found.", is_terminal=False)

        # 2. Logic: Was this a good move?
        if action.command == "delete":
            self.secret_emails.remove(target)
            if target["type"] == "spam":
                reward_val = 1.0
                comment = "Correct! Deleted spam."
            else:
                reward_val = -2.0
                comment = f"Oops! You deleted a {target['type']} email."

        elif action.command == "archive":
            self.secret_emails.remove(target)
            if target["type"] in ["work", "social"]:
                reward_val = 1.0
                comment = "Nice. Archived a legitimate email."
            else:
                reward_val = -0.5
                comment = "Spam should be deleted, not archived."

        # 3. Check if we are done
        done = len(self.secret_emails) == 0 or self.step_count >= self.max_steps
        
        return self._get_observation(), EmailReward(reward=reward_val, comment=comment, is_terminal=done)

    def state(self):
        """Standard OpenEnv method to return the full raw state for debugging."""
        return {"inbox": self.secret_emails, "archive": self.archive, "deleted": self.deleted}