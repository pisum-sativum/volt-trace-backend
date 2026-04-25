from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
import os

from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure GOOGLE_API_KEY is set in your environment variables before running
# export GOOGLE_API_KEY="your_api_key"

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

ENERGY_PER_GB = 0.81  
CARBON_PER_KWH = 475  

@app.get("/api/scan")
def scan_website(url: str, carbon_intensity: float = 475.0):
    # Ensure it's a full URL
    if not url.startswith("http"):
        url = "https://" + url
        
    # Our new, stronger browser disguise
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
        
    try:
        # Using 'requests' instead of 'aiohttp'. It handles redirects automatically.
        response = requests.get(url, headers=headers, timeout=10)
        
        # Check if we got blocked
        if response.status_code != 200:
            raise Exception(f"Website blocked the scan (Status Code: {response.status_code}).")
        
        html = response.text
        
        # 1. Math Phase
        size_bytes = len(html.encode('utf-8'))
        size_gb = size_bytes / (1024 * 1024 * 1024)
        carbon_grams = size_gb * ENERGY_PER_GB * carbon_intensity
        
        # 2. Parsing Phase
        soup = BeautifulSoup(html, 'lxml')
        images = len(soup.find_all('img'))
        scripts = len(soup.find_all('script'))
        
        size_kb = round(size_bytes / 1024, 2)
        carbon_final = round(carbon_grams, 6)

     # 3. Agentic Reasoning Phase 
        prompt = f"""
                You are a senior Green IT Consultant auditing the website {url}.
                
                Audit Metrics:
                - Total Page Weight: {size_kb} KB
                - Carbon Footprint: {carbon_final} grams of CO2 per visit
                - Asset Count: {images} images, {scripts} scripts
                
                Based strictly on these metrics, identify the 3 most likely performance bottlenecks causing this carbon footprint.
                
                Return EXACTLY and ONLY a valid JSON array matching this format, with no markdown blocks or extra text:
                [
                  {{
                    "problem": "State the specific issue clearly.",
                    "solution": "Provide a technical engineering action, e.g., tree-shaking, WebP conversion."
                  }}
                ]
                """
        
        ai_response = llm.invoke(prompt)
        
        import json
        ai_text = ai_response.content.strip()
        if ai_text.startswith("```json"):
            ai_text = ai_text[7:]
        if ai_text.endswith("```"):
            ai_text = ai_text[:-3]
        
        try:
            ai_data = json.loads(ai_text)
        except Exception:
            # Fallback if the AI messes up the JSON
            ai_data = [{"problem": "Audit Analysis Output", "solution": ai_text}]
        
        # 4. Return Payload
        return {
            "target_url": response.url, # This will show the final URL even if redirected
            "page_size_kb": size_kb,
            "carbon_emissions_grams": carbon_final,
            "assets_found": {
                "images": images,
                "scripts": scripts
            },
            "ai_advice": ai_data
        }
                
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
