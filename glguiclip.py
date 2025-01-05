import subprocess
import tkinter as tk
from tkinter import scrolledtext

class CLIPSInterface:
    def __init__(self):
        self.process = subprocess.Popen(
            ['clips', '-f', 'general_learner.clp'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    def send_command(self, command):
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()
        output = self.process.stdout.readline()
        return output.strip()

    def close(self):
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.stderr.close()
        self.process.terminate()

class ChatInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("General Learner Chat")

        self.clips_interface = CLIPSInterface()

        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.user_input = tk.Entry(root, width=40)
        self.user_input.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

    def send_message(self):
        user_input = self.user_input.get()
        self.chat_display.insert(tk.END, f"You: {user_input}\n")
        self.user_input.delete(0, tk.END)

        # Process the user input with the CLIPS interface
        response = self.process_input(user_input)
        self.chat_display.insert(tk.END, f"GL3: {response}\n")

    def process_input(self, user_input):
        if user_input.startswith("add_concept"):
            parts = user_input.split()
            if len(parts) < 4:
                return "Usage: add_concept <concept_id> <concept_type> <contents>"
            concept_id = parts[1]
            concept_type = parts[2]
            contents = " ".join(parts[3:])
            clips_command = f"(add-concept (create$ concept (concept-id {concept_id}) (concept-type \"{concept_type}\") (contents \"{contents}\")))"
            response = self.clips_interface.send_command(clips_command)
            return response
        elif user_input.startswith("add_rule"):
            parts = user_input.split()
            if len(parts) < 5:
                return "Usage: add_rule <rule_id> <situation> <action> <future_situation>"
            rule_id = parts[1]
            situation = parts[2]
            action = parts[3]
            future_situation = parts[4]
            clips_command = f"(add-rule (create$ rule (rule-id {rule_id}) (situation {situation}) (action {action}) (future-situation {future_situation})))"
            response = self.clips_interface.send_command(clips_command)
            return response
        elif user_input.startswith("learn"):
            parts = user_input.split()
            if len(parts) < 4:
                return "Usage: learn <situation> <action> <future_situation>"
            situation = parts[1]
            action = parts[2]
            future_situation = parts[3]
            clips_command = f"(learn-from-experience {situation} {action} {future_situation})"
            response = self.clips_interface.send_command(clips_command)
            return response
        elif user_input == "interact":
            self.clips_interface.send_command("(interact)")
            return "Interaction mode started."
        else:
            return "Unknown command"

if __name__ == "__main__":
    root = tk.Tk()
    chat_interface = ChatInterface(root)
    root.mainloop()
    chat_interface.clips_interface.close()
