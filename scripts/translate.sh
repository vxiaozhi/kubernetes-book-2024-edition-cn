#!/bin/bash

source .env
#export AZURE_OPENAI_ENDPOINT=https://openai-niuaiapp.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions
export AZURE_OPENAI_ENDPOINT=https://openai-niuaiapp.openai.azure.com
export AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
export AZURE_OPENAI_API_VERSION=2023-03-15-preview
python3 translate.py