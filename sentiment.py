from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END, Frame, ttk
from textblob import TextBlob
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    from textblob.download_corpora import main
    main()
except nltk.exceptions.ContentRetrievalError:
    print("Error downloading corpora. Please check your internet connection.")

class ChatbotApp:
    def __init__(self, master):
        self.master   = master
        master.title("Sentiment Analysis Chatbot")  

        self.frame = Frame(master, padx=50, pady=50)
        self.frame.pack()

        self.label = ttk.Label(self.frame, text="Enter text:")
        self.label.grid(row=0, column=0, sticky='w')

        self.entry = ttk.Entry(self.frame, width=60)
        self.entry.grid(row=1, column=0, padx=5, pady=5)

        self.button = ttk.Button(self.frame, text="Analyze", command=self.analyze_text)
        self.button.grid(row=2, column=0, pady=10)

        self.reset_button = ttk.Button(self.frame, text="Reset", command=self.reset_text)
        self.reset_button.grid(row=2, column=1, padx=5)

        self.output_text = Text(self.frame, wrap='word', height=20, width=60)
        self.output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.scrollbar = Scrollbar(self.frame, command=self.output_text.yview)
        self.scrollbar.grid(row=3, column=2, sticky='ns')

        self.output_text.config(yscrollcommand=self.scrollbar.set)

    def fade_in(self, widget, alpha):
        widget.attributes("-alpha", alpha)
        alpha += 0.1
        if alpha <= 1.0:
            self.master.after(50, self.fade_in, widget, alpha)

    def display_analysis_result(self, output_message, explanation):
        self.output_text.config(state='normal')        
        self.output_text.delete(1.0, END)
        self.output_text.insert(END, output_message + '\n\n')
        self.output_text.insert(END, explanation + '\n\n')
        self.output_text.config(state='disabled')

        # fade in animation
        self.master.after(50, self.fade_in, self.output_text, 0.0)

    def analyze_text(self):
        user_input = self.entry.get()

        sentiment, polarity, subjectivity, analysis = self.analyze_sentiment(user_input)  
        output_message = f"Sentiment: {sentiment}\nPolarity: {polarity:.2f}\nSubjectivity: {subjectivity}"
        explanation = self.generate_explanation(sentiment, polarity, subjectivity)

        self.display_analysis_result(output_message, explanation)
        self.entry.delete(0, 'end')

    def reset_text(self):
        self.entry.delete(0, 'end')
        self.output_text.config(state='normal')        
        self.output_text.delete(1.0, END)
        self.output_text.config(state='disabled')

    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        polarity, subjectivity = analysis.sentiment.polarity, analysis.sentiment.subjectivity
        sentiment = 'Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral'
        return sentiment, polarity, subjectivity, analysis
    
    def generate_explanation(self,sentiment,polarity,subjectivity):
        explanation = f"The sentiment of text is {sentiment.lower()}. "
        explanation += f"It generally expresses a {'positive' if sentiment == 'Positive' else 'negative'} sentiment. "
        explanation += f"The polarity score is {polarity:.2f}, where a higher value indicates stronger emotions. "
        explanation += f"The subjectivity score is {subjectivity:.2f}, where a higher value indicates the text is more subjective."
        return explanation

if __name__ == "__main__":
    root = Tk()
    app = ChatbotApp(root)   
    root.mainloop()
