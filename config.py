from pathlib import Path

#LLM SETTINGS

MODEL = "gemini-2.5-flash"
SPEECH_CONFIG = None
SUMMARY_CONFIG = {"temperature": 0.5, "max_output_tokens": 2500}
COGMODEL_CONFIG = {"temperature": 0}


class Paths:
    LAST_SESSION_PATH: Path = Path("Summaries/FatihaLast.txt")
    GLOBAL_SESSION_PATH: Path  = Path("Summaries/FatihaGlobal.txt")
    COGNITIVE_MODEL_PATH: Path = Path ("Persona/FatihaModel.csv")
    PERSONA_PATH: Path = Path("Persona/FatihaPersona.txt")
    LAST_SESSION_BACKUP_PATH: Path = Path("Summaries/Backups/FatihaLast_Backup.txt")
    GLOBAL_SESSION_BACKUP_PATH: Path = Path("Summaries/Backups/FatihaGlobal_Backup.txt")
    COGNITIVE_MODEL_BACKUP_PATH: Path = Path("Summaries/Backups/FatihaModel_Backup.csv")

class PatientPaths():
    def __init__(self, name: str):
        self.LAST_SESSION_PATH: Path = Path(f"Summaries/{name}Last.txt")
        self.GLOBAL_SESSION_PATH: Path  = Path(f"Summaries/{name}Global.txt")
        self.COGNITIVE_MODEL_PATH: Path = Path (f"Persona/{name}Model.csv")
        self.PERSONA_PATH: Path = Path(f"Persona/{name}Persona.txt")
        self.LAST_SESSION_BACKUP_PATH: Path = Path(f"Summaries/Backups/{name}Last_Backup.txt")
        self.GLOBAL_SESSION_BACKUP_PATH: Path = Path(f"Summaries/Backups/{name}Global_Backup.txt")
        self.COGNITIVE_MODEL_BACKUP_PATH: Path = Path(f"Summaries/Backups/{name}Model_Backup.csv")


EVENT_HIST = ""