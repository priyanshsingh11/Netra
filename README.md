NETRA – AI-Powered Digital Threat Detection

> NETRA (National AI-Powered Threat Recognition & Analysis) is an AI-driven platform designed to detect, analyze, and counter anti-India campaigns on digital platforms in real time.



🚀 Features

AI + Cybersecurity Fusion → NLP + Sentiment Analysis + Threat Intelligence for national security.

Multilingual Support → Analyzes Hindi, English, Urdu, and Spanish content.

Real-time Monitoring → Detects disinformation, propaganda, and coordinated attacks on Twitter/X.

Interactive Dashboard → Provides insights, visualizations, and alerts for policymakers, security agencies, and media watchdogs.

Actionable Insights → Generates campaign trends, sentiment graphs, and impact scores.



---

🏗 Tech Stack

🔹 Backend & AI/ML

Python, FastAPI (REST APIs)

Hugging Face Transformers (twitter-roberta-base-sentiment)

Scikit-learn, NumPy, Pandas

BeautifulSoup, Selenium (web scraping)


🔹 Frontend & Dashboard

React.js + Tailwind CSS (UI)

Streamlit (analytics dashboard)

Chart.js / Recharts (data visualization)


🔹 Storage & Deployment

MongoDB (database)

Local/Cloud Python virtual environments

API integrations for Twitter/X



---

📊 System Architecture

1. Data Collection → Web scraping & APIs (Twitter/X, news, social media).


2. Preprocessing → Cleaning, tokenization, and language normalization.


3. ML Model → Sentiment analysis + propaganda detection.


4. Backend (FastAPI) → Exposes REST APIs for real-time insights.


5. Frontend (React + Streamlit) → Displays campaigns, alerts, and trends.


6. Visualization → Graphs, impact scores, and narrative tracking.




---

🔄 Workflow

1. Scrape data from Twitter/X using Selenium & BeautifulSoup.


2. Pass text to ML pipeline (RoBERTa sentiment + fine-tuned models).


3. Classify posts → Positive / Neutral / Negative / Propaganda.


4. Store insights in MongoDB.


5. Display results on React + Streamlit dashboard with live updates.




---

📌 Use Cases

🛡 Government & Security Agencies → Early detection of anti-national narratives.

📢 Media Watchdogs → Reliable, fact-based insights against propaganda.

🌍 Global Impact → Prevents negative portrayal of India internationally.

👥 Citizens → Reduces exposure to harmful misinformation.



---

⚠ Challenges & Mitigation

Data Access Limits → Use APIs & rate-limit handling.

Model Bias & Accuracy → Fine-tune with India-specific datasets.

Scalability → Optimize backend with cloud services.

Ethical & Legal Risks → Respect privacy laws (GDPR, IT Act, DPDP Act).



---

📂 Project Setup

# Clone repo
git clone https://github.com/priyanshsingh11/Netra.git
cd Netra


# Frontend setup
cd frontend
npm install
npm start


---

👨‍💻 Team Optuna – VIT Bhopal

Priyansh Singh

Priyanshu Singh

Oshmi Singh Sisodia

Kanak Paliwal

Ayush Rathi



---

📜 License

This project is open-source and available under the MIT License.
