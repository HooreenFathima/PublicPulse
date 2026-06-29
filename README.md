Public Pulse: A Social Media Analysis Framework for Citizens' Reactions to Government Actions
Public Pulse is a Python-based web application designed to automatically capture, process, and analyze public sentiment toward government policies, schemes, and actions. By replacing slow, traditional, manual survey-based methods , this framework leverages Natural Language Processing (NLP) and Machine Learning to categorize citizen feedback into Positive, Negative, or Neutral sentiments in real time. 
🚀 Key Features
Role-Based Access Control: Dual-portal interface featuring an administrative checkpoint. Users register and must wait for manual admin approval before accessing the prediction pipeline.
Automated NLP Text Processing: Cleans raw text inputs by converting to lowercase, removing punctuation/stopwords, and executing tokenization.
Vectorization & ML Classification: Utilizes TF-IDF vectorization to convert processed text into numerical features , passing them to a pre-trained machine learning classification model.
Admin Oversight & Visual Analytics: A dedicated administrative dashboard that manages user statuses (Approve/Reject/Delete) and displays real-time sentiment distributions via graphical charts. 
Robust Database Architecture: Secure data storage utilizing MySQL to map user accounts, submitted reactions, and corresponding prediction outputs.

🛠️ Tech Stack & Requirements
Software EnvironmentLanguage: Python  
Web Framework: Flask (with Flask-ORM)  
Front-End: HTML, CSS, JavaScript  
Database: MySQL (WAMP Server) 
ML/NLP Libraries: joblib  (for serialization), scikit-learn (for TF-IDF vectorization and classification models) 
Minimum Hardware RequirementsRAM: 4 GB   Storage: 20 GB Hard Disk 
Processor: Pentium-IV or higher  

📦 System Architecture & Modules
The system is split into 7 tightly decoupled modules to guarantee modular updates and maintainability: 
User Management: Handles user registration, validation, and session security. 
Admin Management: Exercises total control over account authorization and data flows. 
Reaction Collection: Captures citizen text strings regarding policies through a web UI. 
NLP Text Processing: Bridges raw text data into vectorized numerical representations. 
Sentiment Analysis: Predicts the structural sentiment type using pre-trained .pkl models. 
Result Visualization: Builds clear, graphical outputs representing global and individual feedback trends.  
Database Management: Backs the system integrity by handling query retrievals and entity relationships. 

