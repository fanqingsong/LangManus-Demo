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


def get_llm_by_type(llm_type_name: str, temperature: float = 0.7) -> Optional[ChatOpenAI]:
    """Get LLM instance by type name.
    
    Args:
        llm_type_name: String name of LLM type ("reasoning", "basic", "vision_language")
        temperature: Temperature setting for the LLM
        
    Returns:
        ChatOpenAI instance or None if configuration is missing
    """
    type_mapping = {
        "reasoning": LLMType.REASONING,
        "basic": LLMType.BASIC,
        "vision_language": LLMType.VISION_LANGUAGE
    }
    
    llm_type = type_mapping.get(llm_type_name)
    if not llm_type:
        logger.error(f"Unknown LLM type name: {llm_type_name}")
        return None
        
    return create_llm(llm_type, temperature)


# Create default LLM instances
reasoning_llm = create_llm(LLMType.REASONING)
basic_llm = create_llm(LLMType.BASIC)
vl_llm = create_llm(LLMType.VISION_LANGUAGE) 