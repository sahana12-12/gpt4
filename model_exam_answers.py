"""Model exam solutions: 30 Ollama-powered mini applications.

Requirements: Python 3.9+, requests, and Ollama running locally.
Install requests: python -m pip install requests
Start Ollama and pull a model (example): ollama pull llama3.2
Run: python model_exam_answers.py
"""
from pathlib import Path
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"  # Change this to a model installed in Ollama.

TASKS = {
 1: ("Grammar Correction Assistant", "Correct grammar and spelling in the text below. Preserve its meaning. Return only the corrected text.", "corrected_text.txt"),
 2: ("Sentiment Analysis Application", "Classify this customer review as Positive, Negative, or Neutral. Give a brief reason.", None),
 3: ("AI-Based MCQ Generator", "Create five multiple-choice questions about the topic. Give four options (A-D) and identify the correct answer after each question.", None),
 4: ("AI Study Assistant", "Explain the academic topic simply and give one suitable example.", None),
 5: ("AI Flashcard Generator", "Create exactly five study flashcards. Format each as Question: ... / Answer: ...", "flashcards.txt"),
 6: ("Meeting Minutes Generator", "Turn these notes into concise meeting minutes with summary, decisions, and action items with owners when stated. Do not invent missing owners.", "meeting_minutes.txt"),
 7: ("AI Resume Analyzer", "Analyze this resume text. List skills and qualifications, provide a brief profile summary, and suggest improvements. Do not infer facts not present.", None),
 8: ("College FAQ Chatbot", "Answer the question only from this FAQ dataset. If the answer is not present, say: Information unavailable in the FAQ dataset.", None),
 9: ("Customer Feedback Analyzer", "Identify the main complaint or appreciation, classify as Positive, Negative, or Neutral, and suggest an appropriate action.", None),
 10: ("Interview Preparation Assistant", "Generate five technical interview questions with answers at the specified difficulty.", None),
 11: ("AI Story Generator", "Write a short story based on the provided topic, genre, and audience.", "story.txt"),
 12: ("Text Translation Assistant", "Translate the supplied paragraph into the target language. Return only the translation.", "translated_text.txt"),
 13: ("AI Text Summarizer", "Write a concise summary and then list the main ideas from the text.", "summary.txt"),
 14: ("AI Question Paper Generator", "Generate the requested number of questions about the specified subject and topic, and provide an answer to each.", None),
 15: ("AI Paragraph Rewriter", "Rewrite the paragraph in the requested style (Formal, Simple, or Professional), preserving its meaning. Return only the rewrite.", "rewritten_text.txt"),
 16: ("AI Keyword Extractor", "Extract the important keywords, key phrases, and main concepts. Present them clearly as a list.", None),
 17: ("AI Assignment Topic Generator", "Suggest five relevant assignment topics for the subject and interest area. Give a brief description of each.", None),
 18: ("AI Product Description Generator", "Write an attractive, accurate product description for the stated product, features, and target customers. Do not invent features.", "product_description.txt"),
 19: ("AI Daily Task Planner", "Arrange these tasks into a practical daily schedule within the available time. Show suggested time slots; mention any tasks that do not fit.", None),
 20: ("AI Interview Preparation Assistant", "Generate five technical interview questions with answers at the specified difficulty.", None),
 21: ("AI Grammar Correction Assistant", "Correct grammar and spelling while preserving the original meaning. Return only the corrected text.", "corrected_text.txt"),
 22: ("Sentiment Analysis Assistant", "Classify the feedback as Positive, Negative, or Neutral and briefly explain the classification.", None),
 23: ("AI-Based MCQ Generator", "Create five multiple-choice questions about the subject and topic. Give four options (A-D) and identify each correct answer.", None),
 24: ("AI Study Assistant", "Explain the academic topic simply, give a relevant example, and list three important points to remember.", None),
 25: ("AI Flashcard Generator", "Create exactly five flashcards about the subject and topic. Format each as Question: ... / Answer: ...", "flashcards.txt"),
 26: ("Meeting Minutes Generator", "Prepare concise minutes with summary, decisions, and action items and responsibilities mentioned in the notes. Do not invent missing details.", "meeting_minutes.txt"),
 27: ("AI Resume Analyzer", "Analyze this resume. List skills and qualifications, summarize the candidate profile, and recommend improvements. Do not infer facts not present.", None),
 28: ("College FAQ Chatbot", "Answer only using the FAQ dataset. If the answer is not present, say: Information unavailable in the FAQ dataset.", None),
 29: ("Customer Feedback Analyzer", "Identify the main complaint or appreciation, classify as Positive, Negative, or Neutral, and suggest an appropriate action.", None),
 30: ("AI Email Assistant", "Draft an appropriate email reply with a suitable subject, greeting, message, and closing. Use the requested tone.", "email_reply.txt"),
}

# Edit these example entries to match your college's official information.
FAQS = {
 "admission": "Contact the college admissions office for current eligibility, dates, and application steps.",
 "courses": "Consult the current college prospectus or academic office for the complete course list.",
 "library timings": "Check the library noticeboard or contact the library for today's opening hours.",
 "examination schedules": "Check the official examination noticeboard or college website for the current timetable.",
}


def ask(prompt):
    return input(prompt + "\n> ").strip()


def collect(task_id):
    if task_id in (1, 21): return ask("Enter sentence or paragraph")
    if task_id in (2, 9, 22, 29): return ask("Enter customer review or feedback")
    if task_id in (3, 5, 16, 17):
        topic = ask("Enter topic" if task_id != 17 else "Enter subject and area of interest")
        return topic
    if task_id in (4, 24): return ask("Enter academic topic")
    if task_id in (6, 26): return ask("Enter meeting notes")
    if task_id in (7, 27):
        filename = input("Resume text file [resume.txt]: ").strip() or "resume.txt"
        try: return Path(filename).read_text(encoding="utf-8")
        except OSError as exc: raise ValueError(f"Could not read {filename}: {exc}")
    if task_id in (8, 28):
        return "FAQ DATASET:\n" + "\n".join(f"{k}: {v}" for k, v in FAQS.items()) + "\n\nQUESTION: " + ask("Ask a college question")
    if task_id in (10, 20): return "Subject: " + ask("Enter technical subject") + "\nDifficulty (Beginner/Intermediate/Advanced): " + ask("Enter difficulty")
    if task_id == 11: return "Topic: " + ask("Enter story topic") + "\nGenre (Fantasy/Adventure/Mystery/Science Fiction): " + ask("Enter genre") + "\nAudience (Children/Teenagers/Adults): " + ask("Enter audience")
    if task_id == 12: return "Target language: " + ask("Enter target language") + "\nParagraph: " + ask("Enter paragraph")
    if task_id == 13: return ask("Enter long paragraph")
    if task_id == 14: return "Subject: " + ask("Enter subject") + "\nTopic: " + ask("Enter topic") + "\nNumber of questions: " + ask("Enter number")
    if task_id == 15: return "Style: " + ask("Enter Formal, Simple, or Professional") + "\nParagraph: " + ask("Enter paragraph")
    if task_id == 18: return "Product: " + ask("Enter product name") + "\nFeatures: " + ask("Enter product features") + "\nTarget customers: " + ask("Enter target customers")
    if task_id == 19: return "Tasks: " + ask("List tasks") + "\nAvailable time: " + ask("Enter available hours and preferred start time")
    if task_id == 23: return "Subject: " + ask("Enter subject") + "\nTopic: " + ask("Enter topic")
    if task_id == 25: return "Subject: " + ask("Enter subject") + "\nTopic: " + ask("Enter topic")
    if task_id == 30: return "Original email: " + ask("Paste original email") + "\nTone (Formal/Friendly/Professional): " + ask("Enter tone")
    return ask("Enter input")


def generate(instruction, content):
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": f"{instruction}\n\nInput:\n{content}",
        "stream": False,
    }, timeout=180)
    response.raise_for_status()
    return response.json()["response"].strip()


def main():
    print("Ollama Model Exam Answer Application")
    print("Choose a question number (1-30); enter 0 to quit.")
    while True:
        try:
            number = int(input("\nQuestion number: ").strip())
            if number == 0: break
            if number not in TASKS:
                print("Enter a number from 1 to 30.")
                continue
            title, instruction, output_file = TASKS[number]
            print(f"\n{title}")
            result = generate(instruction, collect(number))
            print("\n" + result)
            if output_file:
                Path(output_file).write_text(result + "\n", encoding="utf-8")
                print(f"\nSaved to {output_file}")
        except ValueError as exc:
            print(f"Input error: {exc}")
        except requests.RequestException as exc:
            print(f"Ollama request failed. Check that Ollama is running and MODEL is installed. Details: {exc}")
        except (KeyError, TypeError) as exc:
            print(f"Unexpected Ollama response: {exc}")

if __name__ == "__main__":
    main()
