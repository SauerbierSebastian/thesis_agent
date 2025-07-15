"""
AI Service for brainstorming.

This module handles AI-powered thesis brainstorming using Gemini and smolagent.

Author: Thesis Helper Team
Date: 2024
"""

import json
import google.generativeai as genai
from typing import Dict, List, Any, Optional
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from backend.app.core.config import settings
from backend.app.models.schemas import UserQuestionnaireRequest, ThesisField

class ThesisAIBrainstormAgent:
    """
    AI agent for thesis brainstorming.
    
    This class uses Gemini AI to generate and discuss ideas and outlines for thesis topics based on user input.
    """

    def __init__(self):
        """
        Initialize the AI agent with the necessary configurations.
        """
        # Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.AI_MODEL)

        # Field-specific knowledge base
        # omitted

    def brainstorm(self, user_data: UserQuestionnaireRequest) -> Dict[str, Any]:
        """
        Generate thesis ideas based on user input.
        
        Args:
            user_data (UserQuestionnaireRequest): User's questionnaire data.
        
        Returns:
            Dict[str, Any]: A dictionary containing the brainstormed ideas and outlines.
        """
        # Prepare the prompt for Gemini
        description_prompt = self._create_description_prompt(user_data, user_data.thesis_description)

        chat_prompt = self._create_chat_prompt(user_data, user_data.thesis_description)

        try:
            description_response = self.model.generate_content(description_prompt)
            chat_response = self.model.generate_content(chat_prompt)

            return {
                "description": description_response.text.strip(),
                "chat message": chat_response.text.strip()
            }
        except Exception as e:
            raise Exception(f"Error generating brainstorm ideas: {str(e)}")
        
    def _create_chat_prompt(self, user_data: UserQuestionnaireRequest,
                       thesis_description: str
                       ) -> str:
        """
        Create a prompt for the AI model based on user data and thesis description.
        
        Args:
            user_data (UserQuestionnaireRequest): User's questionnaire data.
            thesis_description (str): Description of the thesis provided by the user.
        
        Returns:
            str: The generated prompt for the AI model.
        """
        prompt = f"""
        You are an expert thesis advisor specializing in {user_data.thesis_field.value}.
        Help the user brainstorm ideas for their thesis based on the following information:

        {f"THESIS DESCRIPTION:" if thesis_description else ""}
        {thesis_description if thesis_description else ""}

        CHAT HISTORY:
        {user_data.chat_history}

        REQUIREMENTS:
        1. Offer creative and relevant thesis ideas based on the user's field of study.
        2. Ensure the ideas are feasible and align with the user's academic goals.
        3. Provide a variety of ideas, including potential research questions and methodologies.
        4. Use the user's chat history to inform your suggestions.
        5. Ensure the ideas have not been previously discussed in the chat.
        6. The ideas should be structured and easy to understand.
        """
        return prompt
    
    def _create_description_prompt(self, user_data: UserQuestionnaireRequest,
                                   thesis_description: str) -> str:
        """
        Create a prompt for generating a thesis description based on user data.
        
        Args:
            user_data (UserQuestionnaireRequest): User's questionnaire data.
            thesis_description (str): Description of the thesis provided by the user.
        
        Returns:
            str: The generated prompt for the AI model.
        """
        prompt = f"""
        You are an expert thesis advisor specializing in {user_data.thesis_field.value}.
        Help the user generate a detailed description of their thesis based on the following information:

        PREVIOUS THESIS DESCRIPTION:
        {thesis_description if thesis_description else "No previous description."}

        CHAT HISTORY:
        {user_data.chat_history}

        REQUIREMENTS:
        1. Provide a clear, concise thesis description based on the previous description and chat history.
        2. Ensure it aligns with the user's field of study.
        3. The description should be comprehensive and cover all necessary aspects of the thesis topic.
        4. Use the user's chat history to inform the description.
        5. The description should be suitable for academic purposes and reflect the user's research interests.
        6. The description should be structured and easy to understand.
        """
        return prompt

# Global AI Brainstorm instance
ai_brainstorm_agent = ThesisAIBrainstormAgent()