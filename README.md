# **EduGuide: AI-Powered Multi-Agent Study Planner**

EduGuide is an AI-powered multi-agent study planner designed to help students create structured and adaptive study routines. It acts as a **personal AI study coach** that tracks a student's progress, adapts their study plan, and provides motivational feedback to improve consistency and performance.

---

## **Table of Contents**

Problem Statement
Why Agents?
What I Created
Demo
The Build
If I Had More Time
Technologies Used
Setup Instructions

---

## **Problem Statement**

Many students struggle not because of a lack of intelligence or motivation, but because they lack structured, consistent study routines. Common challenges include:

* Creating study plans that are too rigid or unrealistic.
* Underestimating the time needed for difficult topics.
* Forgetting to revise older topics before exams.
* Falling behind without realizing which subjects need more attention.
* Feeling demotivated due to a lack of visible progress.

Traditional timetables and to-do lists quickly become outdated. Without constant adaptation and feedback, students tend to abandon plans or cram at the last minute, leading to stress, burnout, and poor academic performance.

EduGuide was built to tackle these problems by acting as a personal AI study coach that learns about the student and adapts their study plan over time.

---

## **Why Agents?**

Static study plans or traditional apps cannot adapt to the student's changing schedule, progress, and focus. That's why **agents** are the perfect solution for this problem. EduGuide uses a **multi-agent system** where each agent specializes in different tasks:

1. **Profile Agent** collects and manages student details.
2. **Planner Agent** builds and updates the study plan.
3. **Coach Agent** interacts with the student and helps them stay on track.
4. **Evaluation Agent** reviews performance and adapts future schedules.

These agents can track progress, adjust tasks, and offer personalized guidance based on the student's performance and needs. They continuously evolve and ensure the plan stays relevant, unlike traditional static timetables.

---

## **What I Created**

### **Overall Architecture**

EduGuide is composed of four core agents and three shared services that work together to create an adaptive study plan.

* **Profile & Intake Agent**: Collects the student’s details and stores them in session memory.
* **Planner Agent**: Reads syllabus data, breaks it into tasks, and distributes them across days based on the student’s available time.
* **Coach Agent**: Displays daily tasks, allows task completion tracking, and provides motivational messages.
* **Evaluation Agent**: Analyzes weekly progress and adapts future plans to help students stay on track.

### **Shared Services**

* **SessionService**: Manages session-level data.
* **MemoryService**: Stores long-term data (student profile, study plan, logs).
* **LoggingService**: Records actions performed by agents for observability.

---

## **Demo**

### **1. Starting the Program**

Run the following command to start the EduGuide system:

```bash
python main.py
```

### **2. Setting up a Profile**

The program will prompt you for basic information about yourself:

* Your name.
* Your grade/level.
* The subjects you're studying.
* The number of minutes you can study each day.
* Your preferred study time (morning/evening).

### **3. Generating a Study Plan**

Once your profile is set up, the **Planner Agent** will read your syllabus and generate a study plan. The study plan will be divided over the next few days, based on your available study time.

Example output:

```
study_planner_agent/
|
+-- main.py
+-- requirements.txt
+-- README.md
|
+-- agents/
|   +-- __init__.py
|   +-- profile_agent.py
|   +-- planner_agent.py
|   +-- coach_agent.py
|   +-- evaluation_agent.py
|
+-- services/
|   +-- __init__.py
|   +-- session_service.py
|   +-- memory_service.py
|   +-- logging_service.py
|
+-- tools/
|   +-- __init__.py
|   +-- calculator_tool.py
|
\\-- data/
    +-- syllabus.json
    +-- user_profile.json
    \\-- study_plan.json
```

### **4. Daily Usage with the Coach Agent**

The **Coach Agent** will show you your tasks for the day. You can mark tasks as completed or skipped, and the agent will motivate you to keep going.

Example output:

```
Your plan for today:
1. [planned] Math – Quadratic Equations (35 min)
2. [planned] Science – Cell Structure (25 min)

Mark tasks as done or skipped.
```

### **5. Weekly Progress**

At the end of the week, the **Evaluation Agent** will provide a summary of your progress, including completed tasks, skipped tasks, and subject-wise performance.

Example output:

```
Weekly Progress Summary:
Total tasks: 12
Completed: 9
Skipped: 3
Completion rate: 75%

Tasks per subject:
- Math: 5/7 completed
- Science: 4/5 completed
```

This gives the student clarity and motivation to continue.

---

## **The Build**

### **Technologies Used**

* **Python** (developed in VS Code)
* **JSON** for long-term memory (e.g., student profile, study plan)
* **Multi-Agent System** to divide responsibilities and improve flexibility
* **Custom Calculator Tool** for estimating task durations and distributing workloads
* **Logging** for tracking decisions and actions

### **Key Concepts Implemented**

* Multi-agent architecture (ProfileAgent, PlannerAgent, CoachAgent, EvaluationAgent)
* Dynamic task adjustment based on performance and progress
* Session and long-term memory using simple JSON storage
* Motivational and feedback system via the Coach Agent

---

## **If I Had More Time**

If I had more time, I would add the following features to improve EduGuide:

### **1. Full Gemini Integration**

To provide:

* Topic explanations
* Personalized quizzes
* Smart revision prompts

### **2. Smarter Planning Algorithms**

Using:

* Difficulty-weighted scheduling
* Spaced repetition and energy-level modeling
* Real-time adaptive planning based on progress

### **3. Web or Mobile Interface**

A UI that would allow students to:

* View plans visually
* Track progress with charts
* Interact with agents through a more intuitive interface

### **4. Calendar and Notification Integration**

* Sync with Google Calendar
* Phone notifications and reminders

### **5. Teacher/Parent Dashboard**

Allow teachers to monitor:

* Study time
* Progress
* Weak areas

---

## **Technologies Used**

* **Python** (developed in VS Code)
* **JSON** for long-term memory (e.g., student profile, study plan)
* **Multi-Agent System** for managing tasks
* **Logging** for tracking agent performance

---

## **Setup Instructions**

To run the project locally:

1. Clone the repository.
2. Navigate to the project directory.
3. Install the dependencies by running:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```
