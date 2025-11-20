# Overview

This is a simple Python application that demonstrates OpenAI API integration. The project serves as a basic example of how to interact with OpenAI's chat completion API using the GPT-4 model. It includes conversation handling with multi-turn dialogue and basic API key management through environment variables.

# Recent Changes

**November 20, 2025**: Fixed multiple bugs in main.py
- Fixed KeyError when OPENAI_API_KEY environment variable is missing by using `os.environ.get()` instead of direct access
- Updated deprecated OpenAI API usage from old global `openai.api_key` to new client-based approach using `OpenAI(api_key=...)`
- Fixed error checking logic that would never execute due to prior KeyError
- Improved output formatting to display just the message content instead of the full response object

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Application Structure
- **Single-file application**: The entire application logic is contained in `main.py`, making it a straightforward example for learning and experimentation
- **Synchronous execution**: Uses blocking API calls without async/await patterns, suitable for simple scripts and demonstrations

## API Integration
- **OpenAI Chat Completions API**: Uses the official OpenAI Python SDK v1.x with modern client-based approach
- **Conversation pattern**: Demonstrates multi-turn conversation structure with system, user, and assistant roles
- **Model selection**: Hard-coded to use "gpt-4" model for chat completions
- **Output formatting**: Extracts and prints just the message content from the API response

## Configuration Management
- **Environment-based secrets**: API key is retrieved safely using `os.environ.get()` with empty string default
- **Graceful error handling**: Provides clear instructions to users when the API key is missing or empty, including setup guidance
- **Security-first approach**: Avoids committing sensitive credentials to the repository

# External Dependencies

## Third-Party Services
- **OpenAI API**: Core dependency for chat completion functionality
  - Requires valid API key from OpenAI Platform
  - Uses GPT-4 model endpoint
  - Billing applies based on OpenAI's pricing structure

## Python Libraries
- **openai**: Official OpenAI Python SDK for API interaction
- **os**: Standard library for environment variable access
- **sys**: Standard library for error output and exit handling

## Environment Requirements
- **OPENAI_API_KEY**: Required environment variable containing the OpenAI API key
  - Must be obtained from https://platform.openai.com
  - Should be stored securely using Replit's Secrets Tool or similar secret management