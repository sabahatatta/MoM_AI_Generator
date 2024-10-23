---
title: MoM_ActionItems_Generator
app_file: MoM_ActionItems_Generator.py
sdk: gradio
sdk_version: 5.0.2
---
# **Developing an AI Model for Generating MoM and Action Items Using a Zero-Shot Approach**

## **Overview**
This project aims to develop an **AI-based solution** to automatically generate **Minutes of Meeting (MoM) and Action Items** from unstructured meeting data using a **Zero-Shot approach** with pre-trained language models (LLMs) such as **GPT-4**.

This guide walks you through the **problem, solution approach**, and the steps for **developing, testing, and deploying** the AI model. The goal is to automate the manual task of capturing key meeting details such as decisions, tasks, and follow-up actions.

---

## **Problem Definition**
Meetings are essential for collaboration, but **documenting key outcomes, decisions, and tasks manually** is time-consuming and error-prone. Important takeaways might be missed, and follow-up tasks may not be tracked effectively.

**Key Challenges:**
- **Time-consuming manual process.**
- **Inconsistent format** across different meetings.
- **Missed action items** leading to delays.

By **automating** this process, organizations can save time, **increase efficiency**, and ensure **structured documentation** of meetings.

---

## **Solution Overview**
The project focuses on building an AI-powered pipeline using **pre-trained LLMs** (like **GPT-4**) to **generate MoM and Action Items** from meeting data without requiring additional training (Zero-Shot).

- **Input:** Meeting data (audio or text transcripts).
- **Output:** Structured **Minutes of Meeting (MoM)** and **Action Items**.

If audio files are provided, we leverage **speech-to-text services** like **Whisper API** or **Google Speech-to-Text** to convert the audio into text.

---

### **Input and Output Details:**

#### **Input:**
1. **Text-based meeting data:**  
   - Collect meeting notes or transcripts directly from the user.  
2. **Audio meeting data (optional):**
   - Use **speech-to-text** models to convert audio files into text for further processing.

#### **Output:**
- **Structured MoM and Action Items:**
  1. **Meeting Title**  
  2. **Date and Time**  
  3. **Location / Platform**  
  4. **Attendees**  
  5. **Agenda**  
  6. **Key Discussions / Decisions**  
  7. **Actions and Responsibilities**  
  8. **Deadlines**  
  9. **Decisions Made**  
  10. **Follow-up Meeting Details**  

---

## **Steps for Developing the AI Model Using a Zero-Shot Approach**

### **Step 1: Define the Input and Output**
1. **Input:** Meeting data in the form of audio or text.
2. **Output:** A structured MoM with clearly defined action items, deadlines, and decisions.

---

### **Step 2: Understand the Task Completely**
The task involves generating **structured meeting summaries** from unstructured data using a **Zero-Shot approach**.  
The model needs to:
- Handle **diverse meeting formats** (project meetings, brainstorming sessions, client calls).
- Extract both **qualitative information** (e.g., discussions) and **quantitative details** (e.g., deadlines, responsibilities).

---

### **Step 3: Select Testing Data**
We need to simulate **various meeting types and scenarios** to test the robustness of the Zero-Shot model. Testing data should include:
- **Project meetings**
- **Sales calls**
- **Creative brainstorming sessions**
- **Planning meetings**

---

### **Step 4: Collect Testing Data**

Here are some **sample meeting snippets** to test the AI model:

1. **Project Meeting:**
   ```
   Meeting on October 5, 2024, via Zoom.  
   Attendees: John, Sarah, and Kevin.  
   Agenda: Project status updates.  
   Discussion: Sarah mentioned issues with deployment timelines.  
   Action: Kevin to fix the issue by Oct 12.  
   Decision: Proceed with phase 2 of the project.
   ```

2. **Sales Meeting:**
   ```
   Meeting held on October 10, 2024, in the office.  
   Attendees: Client (ABC Corp), Sales team.  
   Discussion: Presentation of new features.  
   Decision: Client agreed to a product demo next week.  
   Action: Prepare demo by October 17.
   ```

3. **Creative Brainstorming Session:**
   ```
   Date: October 12, 2024.  
   Location: Office meeting room.  
   Attendees: Creative Team.  
   Agenda: New product ideas.  
   Key Discussion: Suggested redesigning the app interface.  
   Decision: Explore UI/UX improvements.
   ```

4. **Planning Meeting:**
   ```
   Meeting on October 8, 2024, via Teams.  
   Attendees: All project stakeholders.  
   Agenda: Review project timelines.  
   Discussion: Adjusted the deadline to November 1.  
   Action: John to draft the updated schedule.
   ```

---

### **Step 5: Write the Zero-Shot AI Model Logic**

The **AI logic** is implemented using **OpenAI's GPT-4** via **API calls**.  
- We use **prompt engineering** to provide the model with clear instructions on what it should generate.
- The model generates structured **MoM** and **Action Items** directly from meeting descriptions.

See the full implementation in the `MoM_ActionItems_Generator.py` file.

---

### **Step 6: Test the Model on Different Examples**

1. **Run the Gradio app** to generate MoM for each example.
2. **Analyze the output** to ensure the following:
   - All key fields (title, date, attendees, etc.) are extracted.
   - Action items are clearly defined with responsibilities and deadlines.

---

### **Step 7: Compare Different LLMs and Select the Best**

- **Try different models** (e.g., GPT-3.5, GPT-4) to compare outputs.
- **Analyze free vs paid models** to determine the best one for your needs.
- Use the **best-performing model** for final deployment.

---

## **How to Run the Project**

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/your-username/MOM_ActionItems_Generator.git
cd MOM_ActionItems_Generator
```

### **Step 2: Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate      # Windows
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Set Up the Environment**
Create a `.env` file and fill in your credentials:
```
OPENAI_API_KEY=your_openai_api_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### **Step 5: Run the Application**
```bash
python MoM_ActionItems_Generator.py
```
Open the browser link provided by Gradio to interact with the app.

---

## **Features of the Application**

- **Zero-Shot AI Model:** Generate MoM and action items without training.
- **Email Integration:** Send generated MoM via email.
- **Status Messages:** Inform users of the process (e.g., "Generating...", "Email sent successfully").

---

## **Future Improvements**

- Add **support for other LLMs** (e.g., Anthropic, Cohere).
- Implement **speech-to-text conversion** for audio-based meetings.
- Integrate **reminder emails** for action item deadlines.

---

## **Technologies Used**

- **Python**: Backend logic.
- **OpenAI GPT-4 turbo**: Language model.
- **Gradio**: User interface.
- **SMTP**: Email integration.

---

## **License**

This project is licensed under the MIT License.

---

## **Contributing**

We welcome contributions! Please fork the repository, create a new branch, and submit a pull request.

---