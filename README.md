# VoiceToxModTool
Final Project for CS 598 ECH Fall 2021 at UIUC

VoiceToxModTool is an automated notification system for detecting toxicity in Discord voice channels. 

Our tool uses CraigBot to record voice communications in a Discord server, then converts these recordings to text using Google's Text-to-Speech API. Finally, we use Perspective API to determine toxicity levels at the user level from these transcripts, and notify moderators of the channel whenever a user's levels exceeds a threshold.

## Usage
To add Craig Bot to your Discord server, follow https://craig.chat/home/
Store your downloaded audio files in a directory named "/audio-chunks"

Run the Jupyter Notebook code in your main directory. 

Cell 4 of the notebook uses Text-to-Speech API to transcribe your audio files into a file called "textx/csv".

Cell 5 uses Perspective API to assign toxicity scores ("TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "INSULT", "PROFANITY", "THREAT", "SEXUALLY_EXPLICIT") to each of these transcripts. This data is saved in a file called "texts_perspective.csv".

Finally, modify the Discord server info in cell 6, as well as the toxicity threshold if desired. Running this code will alert a channel of your choice of all users who exceeded the toxicity threshold in their recording.
