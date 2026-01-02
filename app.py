from flask import Flask,request,render_template  #lightweight framework
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os

# loading a API key
load_dotenv()

# your application starts from here
app=Flask(__name__)

#configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-2.5-flash")

df=pd.read_csv("qa_data (1).csv")

#csv to context_text
context_text = ""
for _,row in df.iterrows():
    context_text += f"Q: {row['question']}\nA: {row ['answer']}\n\n"

def ask_gemini(query):
    prompt = f"""
Answer ONLY from the context below.
If not found, say: No relevant Q&A found.FileNotFoundError

Context:
{context_text}

Question: {query}
"""
    return model.generate_content(prompt).text.strip()

#flask Route Function 
@app.route("/",methods=["GET","POST"])
def home():
    answer= ""
    if request.method =="POST":
        query=request.form["query"]
        answer=ask_gemini(query)
    return render_template("index.html",answer=answer)

# flask app run
if __name__=="__main__":
    app.run()