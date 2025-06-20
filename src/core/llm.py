"""LLM management for LangManus Demo."""

from enum import Enum
from typing import Optional
from langchain_openai import ChatOpenAI
from src.config.env import REASONING_LLM, BASIC_LLM, VL_LLM
import logging

logger = logging.getLogger(__name__)


class LLMType(Enum):
    """LLM types for different tasks."""
    REASONING = "reasoning"
    BASIC = "basic"
    VISION_LANGUAGE = "vision_language"


def create_llm(llm_type: LLMType, temperature: float = 0.7) -> Optional[ChatOpenAI]:
    """Create an LLM instance based on type.
    
    Args:
        llm_type: Type of LLM to create
        temperature: Temperature setting for the LLM
        
    Returns:
        ChatOpenAI instance or None if configuration is missing
    """
    try:
        if llm_type == LLMType.REASONING:
            config = REASONING_LLM
        elif llm_type == LLMType.BASIC:
            config = BASIC_LLM
        elif llm_type == LLMType.VISION_LANGUAGE:
            config = VL_LLM
        else:
            raise ValueError(f"Unknown LLM type: {llm_type}")
            
        if not config.api_key:
            logger.error(f"API key not configured for {llm_type.value} LLM")
            return None
            
        return ChatOpenAI(
            model=config.model,
            api_key=config.api_key,
            base_url=config.base_url,
            temperature=temperature
        )
        
    except Exception as e:
        logger.error(f"Error creating {llm_type.value} LLM: {e}")
        return None


# Create default LLM instances
reasoning_llm = create_llm(LLMType.REASONING)
basic_llm = create_llm(LLMType.BASIC)
vl_llm = create_llm(LLMType.VISION_LANGUAGE) 