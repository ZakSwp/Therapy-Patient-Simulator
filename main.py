from google import genai
from dotenv import load_dotenv
from config import *
from prompts import *
import os
from datetime import datetime
import agents
import logging
from utils import reset_patient_state

load_dotenv() 

apiKey = os.environ.get("GEMINI_API_KEY")

if input("Reset patient state?").lower() in "yes":
    reset_patient_state("Fatiha")
patient = agents.PatientProfile(Paths.PERSONA_PATH,Paths.COGNITIVE_MODEL_PATH)
speechAgent = agents.SpeechAgent(apiKey, MODEL)
eventAgent = agents.EventAgent(apiKey, MODEL)
eventAgent.configure(0.2)
summaryAgent = agents.SummaryAgent(apiKey, MODEL)
cogModelAgent = agents.CogModelAgent(apiKey, MODEL, Paths.COGNITIVE_MODEL_PATH)
speechAgent.link_agents([summaryAgent,cogModelAgent, eventAgent])
speechAgent.start_session(patient)




#print(cogModelAgentInst.get_cog_model())
