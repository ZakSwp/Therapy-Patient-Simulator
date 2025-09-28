from utils import *
from config import *
from prompts import *
import random
from google import genai
random.seed()

class PatientProfile():
    '''Class containing the patient persona (path) and cognitive model (path) for the construction of the overall personality.
    '''
    def __init__(self, patientPaths):
        try:
            with open(patientPaths.PERSONA_PATH, 'r') as file:
                self.persona = file.read()
            self.paths = patientPaths
            self.cogModel = load_dict(patientPaths.COGNITIVE_MODEL_PATH)
            #self.paths = [patientPaths.PERSONA_PATH, patientPaths.COGNITIVE_MODEL_PATH] 
        except IOError as e:
            print(f"Error loading patient profile: {e} ")

    def update_cognitive_model(self, cogModel):
        try:
            self.cogModel = cogModel
            save_dict(self.paths.COGNITIVE_MODEL_PATH , cogModel)
            #print(f"Cognitive model saved at {self.paths[1]}")
        except IOError as e:
            print(f"Error saving updated cognitive model to {self.paths.COGNITIVE_MODEL_PATH}")
 
class Session():
    def __init__(self,patientProfile: PatientProfile, dialgID=0, memory = []):
        self.patient = patientProfile
        self.dialgID = dialgID
        self.memory = memory
        #self.paths = [lastSessionPath,globalSessionPath ]
        with open(self.patient.paths.LAST_SESSION_PATH, 'r') as file:
            self.lastSessionSummary = file.read()
        with open(self.patient.paths.GLOBAL_SESSION_PATH, 'r') as file:
            self.globalSummary = file.read()
        try:
            self.seshID = get_session_number(self.lastSessionSummary)+1
            print(f"Sessino ID = {self.seshID}")
        except:
            self.seshID = 0
    def get_description(self):
        """Returns the relevant patient's persona description."""
        return(self.patient.persona)
    def get_cog_model(self):
        """Returns the relevant patinet's cognitive model."""
        return(self.patient.cogModel)
    def update_last_session_summary(self, summary):
        """Updates last session summary file with new summary."""
        self.lastSessionSummary = summary
        try:
            with open(self.patient.paths.LAST_SESSION_PATH, 'w', encoding = 'utf-8') as f:
                f.write(f"Summary of session {self.seshID}\n")
                f.writelines(summary)
            print(f"*Session summary updated: {self.patient.paths.LAST_SESSION_PATH}*")
        except IOError as e:
            print(f"Failed to update session summary: {self.patient.paths.LAST_SESSION_PATH}")
            raise
    def update_global_summary(self, summary):
        """Updates global sessions summary file with new summary."""
        self.globalSummary += summary #TODO file management 
        file = open(self.patient.paths.GLOBAL_SESSION_PATH, "a")
        file.writelines("\n" + summary + "\n")
        file.close()
    def update_memory(self, qst, ans):
        """Updates current session memory. Verbatim."""
        self.memory.append(f"\nDialogue Turn ID = {self.dialgID}:\n Therapist: {qst}\n Patient: {ans}\n")
        self.dialgID+=1
    def update_cognitive_model(self,cogModel):
        self.patient.update_cognitive_model(cogModel)
    def get_last_session_summary(self):
        return(self.lastSessionSummary)
    def get_global_summary(self):
        return(self.globalSummary)
    def get_last_utterance(self):
        try:
            return(self.memory[-1])
        except:
            print("Empty session memory.")
    def check_for_termination(self, apiKey : str, qst,ans):
        terminationAgent = BaseAgent(apiKey, MODEL, {})
        try:
            response = terminationAgent.run_prompt(TERMINATION_CHECK_PROMPT.format(self.memory), COGMODEL_CONFIG).text #FIXME PLACEHOLDER METHOD 
            line = response.split('\n')[0]
            words = line.strip().split()
            if words[0]=="YES":
                print("*Session concluded.*")
                return(1)
            return(0)
        except:
            print("Termination check failed")
        return(response)

class BaseAgent():
    def __init__(self, apiKey, model, context = None , type= "generic"):
            self.context = context
            self.client = genai.Client(api_key=apiKey)
            self.apiKey = apiKey
            self.model = model
            self.partnerDict = {}
            self.type = type
    def run_prompt(self, prompt, generationConfig = None):  
        try:
            if generationConfig == None:
                response = self.client.models.generate_content(model = self.model, contents = prompt)
            else:
                response = self.client.models.generate_content(model = self.model, contents = prompt, config = generationConfig )#prompts a client and returns a response object
            if response.text == None:
                log_crash(response.__dict__)
                raise ValueError(f"Error retrieving {self.type} agent response.")
        except Exception as e:
                print(f"Prompt execution failed: {e}")
                raise
        log_usage("Zakaria", 1)
        return(response)

    def link_agents(self, agentList):
        for i in agentList:
            if isinstance(i,BaseAgent):
                self.partnerDict |= i.partnerDict
                self.partnerDict[str(i)] = i
                i.partnerDict[str(self)]=self
                i.partnerDict |= self.partnerDict
                i.partnerDict.pop(str(i), None)

            else:
                raise TypeError("Both arguments must be agent objects.")

    def __str__(self):
          return(self.type)
    
class SpeechAgent( BaseAgent ):
    def __init__(self, apiKey, model, context, dialgID=0, session = None):
        super().__init__(apiKey, model, context, type = "speaker")
        self.dialgID = dialgID
        self.session = session
    
    def load_session(self, patient: PatientProfile): 
        '''Debug method. Loads an empty session (NO DIALOGUE)
        '''
        self.session = Session(patient)
        print("Empty session started.")

    def start_session(self,patient: PatientProfile, debugMode=False):
        self.session = Session(patient) #TODO: get all patient related filepaths from patient args
        self.partnerDict["narrator"].check_event()
        while True:
            qst,ans=self.run_prompt(debugMode)
            self.partnerDict["cogModeller"].update_cognitive_model()
            if self.session.check_for_termination(self.apiKey, qst,ans):
                break
        self.partnerDict["summarizer"].generate_summary()
        self.partnerDict["summarizer"].generate_global_summary()
        print("*Global summary updated.*")

    def run_prompt(self, debugMode):
        if not self.dialgID:
            print("Session started.")
            qst = input("Therapist: ")
            prompt = SPEECH_PROMPT_1.format(self.session.get_description(),self.session.get_cog_model(),self.get_last_session_summary(), self.get_global_summary(),qst)
            self.dialgID=1
        else:
            print(f"\nDialogue turn ID: {self.dialgID}")
            qst = input("Therapist: ")
            prompt = SPEECH_PROMPT_2.format(self.session.get_description(),self.session.get_cog_model(),self.recall_current_session(),self.get_last_session_summary(),self.get_global_summary(),qst)
            self.dialgID+=1
        response = super().run_prompt(prompt, SPEECH_CONFIG)
        if debugMode:
            print(response.__dict__)
        ans = response.text
        log_usage("Zakaria", 1)
        print("Patient: ")
        print(ans)
        self.session.update_memory(qst, ans)
        return(qst,ans)
    def recall_last_utterance(self):
        if self.dialgID:
            return(self.session.memory[-1])
        else:
            return("This is the start of the conversation.")
    def recall_current_session(self):
        return("\n".join(self.session.memory))
    def get_last_session_summary(self):
        return(self.session.lastSessionSummary)
    def get_global_summary(self):
        return(self.session.globalSummary)
    
class SummaryAgent( BaseAgent ):
    def __init__(self, apiKey, model):
        self.seshID=0
        super().__init__(apiKey, model,type = "summarizer")
    def update_transcript_file(self):

        pass
    
    def generate_summary(self):
        """Generates therapy session transcript summary and updates the linked speech agent's lastSessionSummary field.
        Summary agent is required to be linked to speech agent.
        """
        if "speaker" not in self.partnerDict:
            raise KeyError("Missing speech agent in partnersDict.")
        else:
            print("*Generating session summary*") 
            speechAgent = self.partnerDict["speaker"]
            session = speechAgent.session
            prompt = SUMMARY_PROMPT.format(speechAgent.recall_current_session()) #fetch speech agent's last conv memory list.
            summary = self.run_prompt(prompt, SUMMARY_CONFIG).text
            session.update_last_session_summary(summary)
    def generate_global_summary(self):
        if "speaker" not in self.partnerDict:
            raise KeyError("Missing speech agent in partnersDict.")
        else:
            print("*Generating global summary*")
            speechAgent = self.partnerDict["speaker"] 
            session = speechAgent.session
            prompt = GLOBAL_SUMMARY_PROMPT.format(session.seshID, speechAgent.get_last_session_summary()) #fetch speech agent's global sessions summary
            summary = self.run_prompt(prompt, SUMMARY_CONFIG).text
            session.update_global_summary(summary)
  
class CogModelAgent( BaseAgent ):
    def __init__(self, apiKey, model, personaPath):
         context = load_dict(personaPath)
         super().__init__(apiKey, model, context, type ="cogModeller")
    def update_cognitive_model(self):
        if "speaker" not in self.partnerDict:
           raise KeyError("Missing speech agent in partnerDict.") 
        else:
            print("*Updating patient cognitive model*") #TODO: replace print with info logging
            speechAgent = self.partnerDict["speaker"]
            session = speechAgent.session
            prompt = COG_PROMPT.format(speechAgent.recall_current_session(),speechAgent.recall_last_utterance(), speechAgent.session.get_description(), self.get_cog_model())
            response = self.run_prompt(prompt,COGMODEL_CONFIG)
            cogModel = response.text
            self.context=cogModel
            cogModel = string_to_dict(cogModel)
            session.update_cognitive_model(cogModel)  
    def get_cog_model(self):
        session = self.partnerDict["speaker"].session
        if session == None:
            raise ValueError("Found no active session in linked speech agent.\n")
        return(session.get_cog_model())

class EventAgent(BaseAgent):
    def __init__(self, apiKey, model): 
        super().__init__(apiKey, model, type ="narrator")
    def configure(self, p:float, severityRange:tuple =(0,1), relevanceRange:tuple=(0,1), favorabilityRange:tuple = (-1,1)):
        '''Between-session event generation configuration.
        Args:
            p (float) : The probability of an event generation occuring.
            severityRange (float tuple) : (beginning, end) defining the range of possible severity levels for the event. Max range = [0,1]
            relevanceRange (float tuple) : (beginning, end) defining the range of possible relevance to the global summary levels. Max range = [0,1]
            favorabilityRange (float tuple) : (beginning, end) defining the range of possible event favorability levels. Max range = [-1,1]
             '''
        self.context = {"Proba":p,
                        "sr": severityRange,
                        "rr": relevanceRange,
                        "fr": favorabilityRange}
    def check_event(self):
        print("Event check:")
        session = self.partnerDict["speaker"].session
        persona = session.get_description()
        if random.uniform(0,1)<=self.context["Proba"]:
            print(" Detected event.\n")
            sr=round(random.uniform(self.context["sr"][0],self.context["sr"][1]),2)
            rr=round(random.uniform(self.context["rr"][0],self.context["rr"][1]),2)
            fr=round(random.uniform(self.context["fr"][0],self.context["fr"][1]),2)
            print(f"Severity: {sr}, Relavance: {rr}, Favorability: {fr}")
            response = self.run_prompt(EVENT_GEN_PROMPT.format(persona,session.get_global_summary(),sr,rr,fr))
            session.update_global_summary(response.text) 
            print(response.text)
            return(response)
        else: 
            print("No event detected.\n")
        return(0)


#DONE: Reformat LLM output into a dict to be saved

#TODO: replace print debug messages with logger output

#TODO: restructure patient storage folders into seperate folders per patient