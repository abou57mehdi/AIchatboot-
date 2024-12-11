import os
import nltk
from difflib import SequenceMatcher
from preprocessing import preprocess_text
import tkinter as tk

def load_knowledge_base(file_path):
    questions_dict = {}
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    for i in range(0, len(lines) - 1, 2):
        question = lines[i].strip()
        answer = lines[i + 1].strip()
        processed_question = preprocess_text(question)
        
        # Store both original and processed versions
        if processed_question not in questions_dict:
            questions_dict[processed_question] = {"original": question, "answer": answer}
    
    return questions_dict

def find_best_match(user_input, questions_dict, threshold=0.6):
    processed_input = preprocess_text(user_input)
    
    best_match = None
    best_ratio = 0
    
    for processed_question in questions_dict.keys():
        # Using sequence matcher instead of edit distance
        ratio = SequenceMatcher(None, processed_input, processed_question).ratio()
        if ratio > best_ratio and ratio >= threshold:
            best_ratio = ratio
            best_match = processed_question
    
    return best_match, best_ratio

def get_response(user_input, questions_dict):
    best_match, confidence = find_best_match(user_input, questions_dict)
    
    if best_match:
        return questions_dict[best_match]["answer"]
    else:
        return "Je ne suis pas sûr de comprendre votre question. Pourriez-vous la reformuler ?"

# Tkinter-based GUI for the chatbot
def create_chat_gui():
    knowledge_base_path = os.path.join("data", "knowledge_base.txt")
    questions_dict = load_knowledge_base(knowledge_base_path)
    
    def on_send_button_click():
        user_input = user_input_field.get().strip()
        if user_input.lower() == 'exit':
            window.quit()
        if user_input:
            chatbot_response = get_response(user_input, questions_dict)
            
            # Update the chat display
            chat_display.config(state=tk.NORMAL)  # Enable the text widget to update
            chat_display.insert(tk.END, "Vous: " + user_input + "\n")
            chat_display.insert(tk.END, "Chatbot: " + chatbot_response + "\n")
            chat_display.config(state=tk.DISABLED)  # Disable the text widget after updating
            
            user_input_field.delete(0, tk.END)  # Clear input field

    # Create the main window
    window = tk.Tk()
    window.title("Chatbot Interface")

    # Create the chat display (Text widget)
    chat_display = tk.Text(window, height=20, width=50, state=tk.DISABLED)
    chat_display.grid(row=0, column=0, columnspan=2)

    # Create the user input field (Entry widget)
    user_input_field = tk.Entry(window, width=40)
    user_input_field.grid(row=1, column=0)

    # Create the send button (Button widget)
    send_button = tk.Button(window, text="Envoyer", command=on_send_button_click)
    send_button.grid(row=1, column=1)

    # Start the Tkinter event loop
    window.mainloop()

if __name__ == "__main__":
    create_chat_gui()
