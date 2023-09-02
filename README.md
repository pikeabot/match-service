# Tournament and Matchmaking service
Simple matchmaking service using AWS Lambda, SQS and PostgreSQL RDS

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