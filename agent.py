# agent.py
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import json

# Initialize OpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

def parse_meal_text(meal_description):
    """Parse natural language meal description into structured nutrition"""
    
    prompt = f"""
    You are a nutrition expert. Parse this meal description and estimate nutrition facts.
    
    Meal: "{meal_description}"
    
    Return ONLY a JSON object with these fields:
    - description: cleaned description
    - calories: estimated total calories (integer)
    - protein: protein in grams (number)
    - carbs: carbohydrates in grams (number)
    - fat: fat in grams (number)
    
    Be realistic with estimates. If unsure, make reasonable assumptions.
    Example: "turkey sandwich on whole wheat with avocado" -> 520 cal, 32g protein, 45g carbs, 18g fat
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Parse the JSON response
    try:
        # Find JSON in response (in case there's extra text)
        text = response.content
        start = text.find('{')
        end = text.rfind('}') + 1
        json_str = text[start:end]
        result = json.loads(json_str)
        return result
    except:
        # Fallback if parsing fails
        return {
            "description": meal_description,
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0
        }

def analyze_food_image(image_file):
    """Analyze a food image and return nutrition estimates"""
    
    import base64
    from langchain_core.messages import HumanMessage
    
    # Convert image to base64
    image_data = base64.b64encode(image_file.read()).decode()
    
    # Create message with image
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": """Analyze this food image. Identify the foods and estimate:
                1. What foods do you see?
                2. Estimated portion sizes
                3. Total calories
                4. Protein (g)
                5. Carbs (g)
                6. Fat (g)
                
                Return ONLY a JSON object with: description, calories, protein, carbs, fat"""
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
            }
        ]
    )
    
    response = llm.invoke([message])
    
    # Parse JSON response
    try:
        text = response.content
        start = text.find('{')
        end = text.rfind('}') + 1
        json_str = text[start:end]
        return json.loads(json_str)
    except:
        return {
            "description": "Food from image",
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0
        }