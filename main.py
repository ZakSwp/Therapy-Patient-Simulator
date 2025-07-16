from google import genai
from dotenv import load_dotenv
from config import *
from prompts import *
import os
from datetime import datetime
import agents
import logging

load_dotenv() 

apiKey = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=apiKey)


patient = agents.PatientProfile("Persona/Patient_1.txt","Persona/sPatient_1.csv")
speechAgentInst = agents.SpeechAgent(apiKey, MODEL)
summaryAgentInst = agents.SummaryAgent(apiKey, MODEL)
cogModelAgentInst = agents.CogModelAgent(apiKey, MODEL, Paths.PERSONA_PATH)
speechAgentInst.link_agents([summaryAgentInst,cogModelAgentInst])



speechAgentInst.start_session(patient)
print(cogModelAgentInst.get_cog_model())







