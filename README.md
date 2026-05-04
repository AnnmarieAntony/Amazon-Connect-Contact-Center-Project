# Omnichannel Contact Center (Voice + Chat) using Amazon Connect

## Overview
Designed and implemented an omnichannel contact center solution for a broadband company using Amazon Connect.

The solution delivers a personalized and intelligent customer experience by integrating Amazon connect, AWS Lambda, Amazon DynamoDB, and Amazon Lex.

## Omnichannel Architecture

This solution supports both voice (IVR) and chat channels using Amazon Connect. 
Both channels share backend services (Lambda, DynamoDB, Lex) to provide a unified customer experience.

## Key Features:

Personalized Greeting:
Retrieves customer details from DynamoDB using Lambda. Existing customers are greeted by name, while new customers receive a general greeting.

Natural Language Interaction:
Integrated Amazon Lex to enable NLU-based conversations, allowing users to interact more naturally.

Hours of Operation Handling:
Validates business hours and plays appropriate messages for in-hours and after-hours calls.

Callback Functionality (After Hours):
Allows customers to request a callback when calling outside business hours.

Queue Callback (In Hours):
Provides callback option when agents are busy. Customers are automatically called back when an agent becomes available.

## Tech Stack
-Amazon Connect (Contact Flows, Routing)
-AWS Lambda (Python, Boto3)
-DynamoDB (Customer data lookup using GSI)
-Amazon Lex (NLU chatbot integration)
-IAM (Permissions and roles)

## Architecture
Omnichannel :

                    ┌──────────────────────────────┐
                    │        Customer Channels     │
                    └──────────────────────────────┘
                         │                  │
                         │                  │
                  📞 Voice (IVR)        💬 Chat (Web/App)
                         │                  │
                         ▼                  ▼
        ┌────────────────────────┐   ┌────────────────────────┐
        │ Amazon Connect         │   │ Amazon Connect         │
        │ Voice Contact Flow     │   │ Chat Flow              │
        └─────────────┬──────────┘   └─────────────┬──────────┘
                      │                            │
                      └──────────────┬─────────────┘
                                     ▼
                        ┌────────────────────────┐
                        │ AWS Lambda             │
                        │ (Business Logic)       │
                        └─────────────┬──────────┘
                                      │
                                      ▼
                        ┌────────────────────────┐
                        │ Amazon DynamoDB        │
                        │ (Customer Data)        │
                        └─────────────┬──────────┘
                                      │
                                      ▼
                        ┌────────────────────────┐
                        │ Amazon Lex             │
                        │ (NLU / Intents)        │
                        └─────────────┬──────────┘
                                      │
                                      ▼
                        ┌────────────────────────┐
                        │ Routing Logic          │
                        │ (Hours / Queue Select) │
                        └─────────────┬──────────┘
                                      │
                                      ▼
                        ┌────────────────────────┐
                        │ Agent Queue            │
                        │ (Voice + Chat)         │
                        └─────────────┬──────────┘
                                      │
                                      ▼
                              👩‍💻 Agent


  IVR Flow:
  

  Customer Call
      ↓
Amazon Connect (Entry Contact Flow)
      ↓
AWS Lambda (Initial Processing)
      ↓
DynamoDB Lookup (Customer Details)
      ↓
Amazon Lex (Optional NLU / Intent Capture)
      ↓
Check Hours of Operation
      ↓
┌──────────────────────────────────────┐
│              IN HOURS                │
└──────────────────────────────────────┘
      ↓
Customer Queue Flow
      ↓
Play Prompt (Queue Name + Agent Info)
      ↓
Get Customer Input (Callback Request if needed)
      ↓
Check Queue / Agent Availability
      ↓
If Agent Available → Connect to Agent
      ↓
If Queue Full → Offer Callback 
      ↓
Transfer to callback queue
      ↓

┌──────────────────────────────────────┐
│            OUT OF HOURS              │
└──────────────────────────────────────┘
      ↓
Play Closed Message
      ↓
Offer Callback Option
      ↓
Create Task (Callback Request)
     

## How it works
1. Customer calls contact center
2. Phone number captured in contact flow
3. Lambda function invoked
4. DynamoDB queried using GSI
5. Customer data returned and used in flow
6. Greeting using the customername if it exists or general greeting
7. Lex invoked and captures customer intent
8. Queue identified and check hours of operation
9. call back options based on hours of operation
10. Transfer to agent if in hours and connected to agent


Inbound Chat flow:


    Customer Starts Chat
        ↓
Amazon Connect Chat Entry Flow
        ↓
Welcome / Greeting Message
        ↓
Amazon Lex Bot (Intent Detection)
        ↓
Intent Identified
        ↓
Routing Decision (Lambda / Flow Logic)
        ↓
Route to Appropriate Queue
        ↓
                                            ┌───────────────────────────────┐
         -----------------                  │      OUT OF BUSINESS HOURS    │
                                            └───────────────────────────────┘
                                                          ↓
                                                  Out-of-Hours Message OR
                                                  Callback Option OR
           ↓                                      Task Creation (Lambda)
                                                          ↓
                                                      End Chat 

  ┌───────────────────────────────┐
│     IN BUSINESS HOURS    │
└───────────────────────────────┘
Agent Assigned
        ↓
Chat in Progress
        ↓
Customer / Agent Disconnect Event
        ↓

 chat disconnect flow
        ↓

────────────────────────────────────────
        🔁 DISCONNECT RECOVERY LOGIC
────────────────────────────────────────
        ↓
Customer Returns to Chat
        in ≤ 4 Hours?
        ↓
      ┌───────────────┐
      │ YES            │
      └───────────────┘
        ↓
Restore Chat Context
        ↓
Route to Any Available Agent
        ↓
Continue Previous Conversation
        ↓
Chat Resumed Successfully

      ┌───────────────┐
      │ NO (>4 hours)  │
      └───────────────┘
        ↓
New Chat Session Starts
        ↓
Lex → Routing → Fresh Flow

────────────────────────────────────────

/ Hold for Callback
