To run the simulator run main.py


Requirements for running a simulation are:

1- Patient persona descripion file (.txt)

2- Patient cognitive model file (.csv)

3- Global summary directory or file (.txt)

4- Last session transcript directory or file (.txt)

5- A .env file with your gemini api key configured as `"GEMINI_API_KEY"`

Replace `apiKey = os.environ.get("GEMINI_API_KEY")` with `apiKey = "your_api_key"` if dotenv fails to load your gemini api key.
