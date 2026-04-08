from models import EmailObservation, EmailAction

class EmailTriageGraders:
    
    @staticmethod
    def grade_easy(final_state, history) -> float:
        """Task: Delete all emails from 'noreply@spam.com'."""
        inbox = final_state["inbox"]
        # If any spam is left in the inbox, the score drops
        spam_left = [e for e in inbox if e["sender"] == "noreply@spam.com"]
        if len(spam_left) == 0:
            return 1.0
        return 0.0

    @staticmethod
    def grade_medium(final_state, history) -> float:
        """Task: Archive all 'work' emails and delete all 'spam'."""
        inbox = final_state["inbox"]
        # If the inbox is empty, it's a good start
        if len(inbox) > 0:
            return 0.0
            
        # Check if they went to the right places
        correct_archive = all(e["type"] == "work" for e in final_state["archive"])
        correct_delete = all(e["type"] == "spam" for e in final_state["deleted"])
        
        if correct_archive and correct_delete:
            return 1.0
        return 0.5 # Partial credit if they cleared the inbox but mixed up folders

    @staticmethod
    def grade_hard(final_state, history) -> float:
        """Task: Reply to the 'High' priority email with 'Will do'."""
        # This requires checking the 'history' of actions taken
        replies = [a for a in history if a.command == "reply"]
        
        for action in replies:
            if action.reply_text and "will do" in action.reply_text.lower():
                return 1.0
        return 0.0