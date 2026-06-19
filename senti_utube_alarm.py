from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END, Frame, ttk, Toplevel
from textblob import TextBlob
import nltk
import time
import threading
import winsound  # For alarm sound on Windows
from googleapiclient.discovery import build

# Try to download required nltk corpora
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    from textblob.download_corpora import main
    main()
except nltk.exceptions.ContentRetrievalError:
    print("Error downloading corpora. Please check your internet connection.")

# YouTube API Key (Replace with your actual key)
YOUTUBE_API_KEY = "AIzaSyAiRuAyZ8cnMDWU1ekRrSYt9u5EqUiTQYc"
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

class ChatbotApp:
    def __init__(self, master):
        self.master = master
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

    def display_analysis_result(self, output_message, explanation):
        self.output_text.config(state='normal')        
        self.output_text.delete(1.0, END)
        self.output_text.insert(END, output_message + '\n\n')
        self.output_text.insert(END, explanation + '\n\n')
        self.output_text.config(state='disabled')

    def analyze_text(self):
        user_input = self.entry.get()

        sentiment, polarity, subjectivity, analysis = self.analyze_sentiment(user_input)  
        output_message = f"Sentiment: {sentiment}\nPolarity: {polarity:.2f}\nSubjectivity: {subjectivity}"
        explanation = self.generate_explanation(sentiment, polarity, subjectivity)

        self.display_analysis_result(output_message, explanation)

        if sentiment == "Negative":
            recommendations = self.get_youtube_recommendations(user_input)
            self.output_text.config(state='normal')
            self.output_text.insert(END, "You seem down. Here are some YouTube videos for you:\n")
            for link in recommendations:
                self.output_text.insert(END, f"{link}\n")
            self.output_text.insert(END, "Would you like to set an alarm? (Enter time in HH:MM format)\n")
            self.output_text.config(state='disabled')

            # Open Alarm window
            self.set_alarm_window()

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
    
    def generate_explanation(self, sentiment, polarity, subjectivity):
        explanation = f"The sentiment of the text is {sentiment.lower()}. "
        explanation += f"It generally expresses a {'positive' if sentiment == 'Positive' else 'negative'} sentiment. "
        explanation += f"The polarity score is {polarity:.2f}, where a higher value indicates stronger emotions. "
        explanation += f"The subjectivity score is {subjectivity:.2f}, where a higher value indicates the text is more subjective."
        return explanation

    def get_youtube_recommendations(self, mood):
        """Fetch YouTube videos based on mood."""
        search_query = "happy songs"  # Default search query

        # Determine the type of videos based on user input
        if "tired" in mood.lower():
            search_query = "relaxing music"
        elif "bored" in mood.lower():
            search_query = "funny videos"
        elif "sad" in mood.lower():
            search_query = "motivational speech"

        # YouTube API Request
        request = youtube.search().list(
            q=search_query,
            part="snippet",
            maxResults=3  # Get top 3 recommendations
        )
        response = request.execute()

        video_links = []
        for item in response["items"]:
            if item["id"]["kind"] == "youtube#video":
                video_id = item["id"]["videoId"]
                video_links.append(f"https://www.youtube.com/watch?v={video_id}")

        return video_links

    def set_alarm_window(self):
        """Opens a popup window to set an alarm."""
        self.alarm_window = Toplevel(self.master)
        self.alarm_window.title("Set Alarm")

        Label(self.alarm_window, text="Enter Alarm Time (HH:MM):").pack(pady=5)
        self.alarm_entry = Entry(self.alarm_window, width=10)
        self.alarm_entry.pack(pady=5)

        Button(self.alarm_window, text="Set Alarm", command=self.set_alarm).pack(pady=10)

    def set_alarm(self):
        """Starts a thread to run the alarm."""
        alarm_time = self.alarm_entry.get()
        self.alarm_window.destroy()  # Close the alarm window
        threading.Thread(target=self.run_alarm, args=(alarm_time,)).start()

    def run_alarm(self, alarm_time):
        """Waits until the alarm time and then rings."""
        while True:
            current_time = time.strftime("%H:%M")
            if current_time == alarm_time:
                self.ring_alarm()
                break
            time.sleep(30)  # Check every 30 seconds

    def ring_alarm(self):
        """Triggers an alarm sound and popup."""
        for _ in range(5):  # Beep 5 times
            winsound.Beep(1000, 500)  # Frequency = 1000Hz, Duration = 500ms

        # Show an alarm popup
        alarm_popup = Toplevel(self.master)
        alarm_popup.title("Alarm!")
        Label(alarm_popup, text="⏰ Alarm ringing! Time's up! ⏰", font=("Arial", 14, "bold")).pack(pady=10)
        Button(alarm_popup, text="Stop", command=alarm_popup.destroy).pack(pady=10)

if __name__ == "__main__":
    root = Tk()
    app = ChatbotApp(root)   
    root.mainloop()
