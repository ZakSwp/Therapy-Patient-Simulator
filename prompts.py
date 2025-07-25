SPEECH_PROMPT_1 = "We're simulating a therapy session. You will play the role of the patient."\
                "This your persona description as a patient:\n{}\n"\
                "This following cognitive values model your cognitive behavior:\n{}\n"\
                "DO NOT USE ACTION BEATS, GESTURE DESCRIPTIONS OR PARENTHETICALS. Do not explicit your symptoms in a direct way"\
                " as that is unrealistic for a human therapy patient. This is the beginning of this therapy session."\
                "The following is the transcript from the last session: \n {}\n"\
                "The following is the global summary of all past sessions, including any events that occured in between sessions:\n {}\n "\
                "I will be your therapist. I begin by saying: {}"
SPEECH_PROMPT_2 = """We're simulating a therapy session. You will play the role of the patient.
                This your persona description as a patient:\n{}\n
                This following cognitive values model your cognitive behavior:\n{}\n
                DO NOT USE ACTION BEATS, GESTURE DESCRIPTIONS OR PARENTHETICALS. Do not explicit your symptoms in a direct way
                as that is unrealistic for a human therapy patient. This is a continuation of this conversation:\n{}\n
                The following is the transcript from the last session: \n {}\n 
                The following is the global summary of all past sessions, including any events that occured in between sessions:\n {}\n
                I will be your therapist. I say: {}"""



SUMMARY_PROMPT = "You are a summarizer agent. You will receive the transcript of a psycotherapy session and are tasked with summarizing"\
" said transcript down 50'%' if possible, keeping strictly all relevant information. Format it in screenplay format without being verbose."\
"The following is the session transcript:\n{}\n"

#GLOBAL_SUMMARY_PROMPT = "You are a summarizer agent. You will receive a global summary of multiple psycotherapy sessions, and"\
#" the transcript of the last session and are tasked with re-summarizing all of them into one global summary, keeping most"\
#" of all relevant information. Format as follows:\n**Session [sessionNumber]:** Summary#\n"\
#"The following is the global summary:\n{}\n"\
#"The following is the last session' transcript:\n{}\n"\
#"The following events happened between the last two sessions:\n{}\n"

GLOBAL_SUMMARY_PROMPT = "You are a summarizer agent. You will receive a transcript of a therapy session "\
" and are tasked with creating a new entry into the global summary list by summarizing the last session, keeping most"\
" of all relevant information. Format as follows:\n**Session {}:** Summary\n"\
"The following is the last session's transcript:\n{}\n" \
#"The following is the global summary, to which the new entry will be appended:\n{}\n"

TERMINATION_CHECK_PROMPT = "You are an agent responsible for determining whether a therapy session has reached its conclusion"\
" whether through agreement or SEVERE disagreement between the two conversing parties (patient and therapist).DO NOT SIMPLY TERMINATE THE SESSION AT THE FIRST SIGHT OF CONFLICT. You will base your"\
" judgement on the following conversation transcript between the two: {} Justify with chain of thought"\
"Output 'YES', 'NO' or 'INCONCLUSIVE' in a single line, and a brief justification in a newline.  "\


COG_PROMPT = "You are an agent responsible for updating a patient's cognitive model."\
"This is the transcript of the ongoing session:\n{}\n"\
"This is the last patient and therapist utterances:\n{}\n"\
"This is the patient's persona description:\n{}\n"\
"These are the current cognitive model values\n{}\n"\
" The cognitive model contains, in order, the following fields: Core beliefs (short string), Intermediate beliefs (short string),"\
" Coping strategies (short string), Automatic thoughts (short string), Emotions (short string), Behaviors (short string), Control "\
"(float in range 1 to -1), Self-Efficacy (float in range 1 to -1), Awareness (float in range 1 to -1), Recall (float in range 1 to -1"\
" defining how good of a memory this patient has), Cooperation Level (float in range 1 to 0 represents the patient's willingness to cooperate"\
" with therapy). Update the fields according to the  afore-mentioned data to mirror any change that occured within the last utterances. After"\
" returning the cognitive model STRICTLY EXACTLY the same way the given cognitive model was formatted (DO NOT use ``` or the word json)"\
", explain in a new paragraph titled 'Chain Of Thoughts' the changes using Chain Of Thoughts."\
#". Format STRICTLY EXACTLY the same way the given cognitive model was formatted."#, using double quotes"\
#" to mark strings, and no quotes at all for floats."
#" This is a summary of all previous sessions:\n{}\n"\

EVENT_GEN_PROMPT = "You are an event generation agent playing the role of narrator. The following is a therapy patient's persona:\n{}.\nThe following" \
" is the global summary of all the discussions between said persona and their therapist:\n{}\nThe following is the event severity level:\n{}" \
" (determines how important and/or severe the event to be generated is in said persona's life). \nThe following is the event revalance level"\
":\n{} (determines how relevant said event is to the discussions that occured in the global summary). The following is the event favorability level \n{}" \
" (determines how favorable the event is to the patient's life, with 1 being a net positive event, -1 a net negative event and 0.0 a neutral event" \
"\nGenerate a brief and simple description"\
" of an event that occured between the last session and the upcoming one that is worth saving in patient's global sessions summary. The event" \
" can be anything from the patient's car being broken into while it was parked in the last session, or them simply running into an old friend "\
"or stumbling upon a new music genre that they appreciate. Be CREATIVE and DIVERSE in the generation of the event, you CAN (but don't have to) even make it a continuity of a previous "\
"event that was already mentioned in the global memory, but formulate STRICTLY THE SAME as given "\
"in the following example:\n**Between sessions 1 and 2:** Patient's cousin is getting married to an ethnic Russian.\n" 