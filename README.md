# VoiceToxModTool
Final Project for CS 598 ECH Fall 2021 at UIUC

VoiceToxModTool is an automated notification system for detecting toxicity in Discord voice channels. 

Our tool uses CraigBot to record voice communications in a Discord server, then converts these recordings to text using Google's Text-to-Speech API. Finally, we use Perspective API to determine toxicity levels at the user level from these transcripts, and notify moderators of the channel whenever a user's levels exceeds a threshold.
