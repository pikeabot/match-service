# Simple Serverless Matchmaking service
Simple matchmaking service using AWS Lambda, SQS and MySQL RDS
Deployed using Terraform

Uses SQS queues as 'lobbies' for players. 

## Requirements
### Functional Requirements
- Offers player vs player matchmaking
- Offers multi player vs multi player matchmaking
- Should be able to match players as quickly as possible, provided there is someone around their skillset
- Players should be matched based on skill

### Non-Functional Requirements
- High Availablility
- Reliability

# Tentative design
Players will be sorted into different queues based on their rank and skill. 

Queues are checked and if there are enough players then a game object and leaderboard
are created

### SQS Message Format:
Messages sent to SQS queue will be in the body and have the format: 
{ playerid: <player id>, timestamp: <current timestamp> }
