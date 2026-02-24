# 🚀 MarketPro Terminal & Portfolio Tracker

A lightweight, fintech-grade portfolio tracking terminal built with pure Python and Vanilla JavaScript. It features a transaction-based ledger, live market pricing, and AI-powered sentiment analysis.

## ✨ Features
* **Transaction Ledger Engine:** Accurate Weighted Average Cost (WAC) calculations based on buy/sell history.
* **Live Telemetry Charting:** Smooth, animated portfolio visualization using Chart.js.
* **Real-time Pricing:** Integrates with `yfinance` for live Gold (XAU), Silver (XAG), and USD-INR conversion.
* **AI Market Analysis:** Connects to Gemini 1.5 Flash to deliver cached, real-time market sentiment and news snippets.
* **Stateless Authentication:** Secure, UUID-based session token system using SQLite.
* **Zero-Build Frontend:** Pure HTML/CSS/JS served directly via Flask templates.

## 🛠️ Tech Stack
* **Backend:** Python, Flask, SQLite3
* **APIs:** yfinance, Google Generative AI (Gemini)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript, Chart.js

---

## 🚀 How to Install & Run Locally

Follow these steps to download and run the terminal on your own machine.

### Prerequisites
* Python 3.8+ installed on your system.
* A free [Google Gemini API Key](https://aistudio.google.com/app/apikey) for the market analysis engine.

### Step 1: Clone the Repository
Open your terminal and download the project:
```bash
git clone [https://github.com/sumadhwa28/market-terminal.git](https://github.com/sumadhwa28/market-terminal.git)
cd market-terminal

# Project Setup Guide

Follow these steps to set up and run the application locally.

## Step 2: Set Up a Virtual Environment (Recommended)
Isolate the project dependencies by creating a virtual environment:

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate

**Mac/Linux**
```bash
python3 -m venv venv
source venv/bin/activate


##Install all the necessary Python libraries:
```bash
pip install -r requirements.txt

## Configure the API Key
```bash
genai.configure(api_key="YOUR_GEMINI_API_KEY")

##Start the Server
```bash
python app.py


## Access the Application
'''bash
http://127.0.0.1:5000/
