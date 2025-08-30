import os 
from dotenv import load_dotenv

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser 

from langchain_aws import ChatBedrock, ChatBedrockConverse 

import boto3 
from botocore.config import Config 

from typing import Any

from ..llm.base import BaseLLM

_ = load_dotenv("../../../../../../.env")

aws_region = os.getenv("AWS_REGION", "us-east-1")
bedrock_config = Config(
    connect_timeout=120, 
    read_timeout=120,
    retries={"max_attempts": 0,},
)

bedrock_rt = boto3.client(
    "bedrock-runtime",
    region_name=aws_region,
    config=bedrock_config,
)

bedrock = boto3.client("bedrock", region_name=aws_region, config=bedrock_config)

class AWS_LLM(BaseLLM):
    """AWS Bedrock LLM implementation."""
    
    def __init__(self, model_id: str = "anthropic.claude-3-haiku-20240307-v1:0", region: str = 'us-east-1', temperature: float = 0.7):
        self.model_id = model_id
        self.temperature = temperature
        self.client = bedrock_rt
        self.model = ChatBedrock(
            model=model_id,
            region=region,
            model_kwargs={"temperature": 0},
        )
        self.conv_model = ChatBedrockConverse(
            model=model_id,
        )

    def invoke(self, messages, **kwargs):
        response = self.conv_model.invoke(input=messages, **kwargs)
        return response

    async def generate_structured_output(self, messages, schema: type[BaseModel], **kwargs) -> BaseModel:
        structured_llm = self.model.with_structured_output(schema) # type: ignore
        response = structured_llm.invoke(messages=messages, **kwargs)

        return response # type: ignore

    async def tool_call(self, messages, tools):
        tool_calling_model = self.conv_model.bind_tools(tools)
        response = tool_calling_model.invoke(messages)
        return response

    def return_tool_calling_model(self, tools) -> Any:
        return self.conv_model.bind_tools(tools)
    
    def with_structured_output(self, schema):
        return self.conv_model.with_structured_output(schema)
    
    def bind_tools(self, tools):
        return self.conv_model.bind_tools(tools)