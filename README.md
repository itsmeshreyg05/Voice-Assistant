# VAPI Voice Assistant

## 🧠 Overview

The **VAPI Voice Assistant** is an AI-powered conversational interface built to handle voice-based interactions through phone calls. The assistant utilizes VAPI (Voice API) for real-time voice communication and integrates with **Make.com** (formerly Integromat) to automate workflows, respond dynamically to user inputs, and trigger backend actions like database updates, reminders, or webhooks.

This project is ideal for automating tasks like appointment booking, surveys, customer support calls, and intelligent voice notifications.

---

## 🔧 Tech Stack

- **VAPI (Voice API)** – to build and handle real-time voice call flows
- **Make.com (Integromat)** – for no-code workflow automation and backend logic
- **Webhooks & HTTP Modules** – to connect voice input with external APIs or databases
- **Google Text-to-Speech (TTS)** – to convert AI-generated text into natural voice responses
- **JavaScript / Python** (optional) – for any custom logic or functions triggered from Make.com

---

## 📦 Features

- AI voice assistant with real-time interaction
- Multi-step conversation flow using Make.com scenario builder
- Easily scalable and customizable for various use-cases (healthcare, education, etc.)
- TTS for natural voice generation
- Webhook triggers for database updates or external API calls
- Logs call transcripts and actions for audit purposes

---

## 🛠️ How It Works

### 1. VAPI Call Setup

- Use VAPI to initiate or receive a voice call.
- A call session starts and gets connected to the voice assistant.

### 2. Make.com Scenario

- A scenario in **Make.com** is triggered via a **Webhook**.
- This scenario includes:
  - Receiving real-time input from VAPI
  - Using HTTP modules or tools to process the data
  - Sending the output (text response) back to VAPI using their API

### 3. Conversation Flow

- The conversation is managed by conditional logic and text-based prompts.
- Google TTS or VAPI’s built-in voice tools are used to convert the response into speech.
- You can branch the conversation based on user input, using filters and routers inside Make.com.

### 4. Integration Capabilities

- Connect with:
  - Google Sheets / Excel for storing responses
  - Email or SMS services for notifications
  - CRMs or databases for data entry or retrieval
  - Any REST API for dynamic data fetch/post

---

## 📁 Example Use Case

**Use Case: Mental Health Screening Bot**

- User receives a call from the assistant.
- VAPI routes the user’s speech to Make.com via a webhook.
- Make.com determines which screening question to ask next.
- Responses are stored in a Google Sheet.
- If critical symptoms are detected, the assistant sends an alert email to a caregiver.

---

## 🚀 Getting Started

### Prerequisites

- VAPI account and phone number
- Make.com account
- Access to Google Workspace or any API endpoint
- Basic knowledge of Make.com scenario creation

### Setup Steps

1. Clone this repository (if applicable for the frontend/backend).
2. Create a webhook in Make.com to handle call events.
3. Build your scenario:
   - Trigger: Webhook
   - Actions: Logic + HTTP + Text-to-Speech + Response to VAPI
4. Configure VAPI to point to your Make.com webhook URL.
5. Test the end-to-end flow.

---

## 🧩 Folder Structure (if applicable)
