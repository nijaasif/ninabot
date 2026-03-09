# NINA Bot – AI Hospital Assistant

## System Design

The NINA Bot system is designed to automate hospital-patient interactions through an AI-powered conversational assistant.

Workflow:

1. A patient interacts with the chatbot widget embedded on a hospital website.
2. The widget sends the user query to the backend API.
3. The backend processes the query and sends it to an AI model.
4. The AI model combines:
   - hospital knowledge base
   - user query context
5. The AI generates a structured response.
6. The backend returns the response to the chatbot widget.
7. The user receives an instant reply.

This architecture enables hospitals to automate common patient queries such as:

• Visiting hours  
• Department information  
• Appointment guidance  
• Hospital services  

## Tech Stack

Backend-> Python
Frontend -> HTML, CSS, JavaScript
AI -> LLM API Integration

Data
• CSV storage
• Text-based knowledge base

## Project Structure

frontend/ → Chatbot UI  
main.py → Backend logic  
hospital_knowledge.txt → Knowledge base  
appointments.csv → Appointment data  
requirements.txt → Dependencies  


## Architecture

The system follows a simple AI assistant architecture designed for hospital query automation.

User → Chat Widget → Backend API → AI Model → Knowledge Base → Response → User

Components:

• **Frontend Widget**
Embedded chatbot UI built with HTML, CSS, and JavaScript.

• **Backend Server**
Python backend responsible for request handling and response generation.

• **AI Processing**
Uses LLM APIs to interpret user queries and generate responses.

• **Knowledge Base**
Hospital-specific information stored in a structured text dataset.

• **Appointment Data**
CSV storage for handling appointment-related data.

## System Architecture

## System Architecture

```
            ┌───────────────┐
            │   User /      │
            │   Patient     │
            └───────┬───────┘
                    │
                    ▼
        ┌─────────────────────┐
        │   Chatbot Widget    │
        │   (HTML/CSS/JS)     │
        └─────────┬───────────┘
                  │
             API Request
                  │
                  ▼
        ┌─────────────────────┐
        │    Backend Server   │
        │       (Python)      │
        └─────────┬───────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
 ┌───────────────┐   ┌─────────────────┐
 │   AI / LLM    │   │  Knowledge Base │
 │     API       │   │  hospital_data  │
 └──────┬────────┘   └────────┬────────┘
        │                     │
        └──────────┬──────────┘
                   ▼
           ┌───────────────┐
           │    Response   │
           │   to Patient  │
           └───────────────┘
```




           ## Demo

![NINA Bot Interface](Screenshot%202025-12-29%20000206.png)

## Future Improvements

• Integration with hospital scheduling systems  
• Multi-language patient support  
• Voice assistant capability  
• Secure database storage  
• Deployment on cloud infrastructure

## Setup

```bash
git clone https://github.com/nijaasif/ninabot.git
cd ninabot
pip install -r requirements.txt
python main.py
