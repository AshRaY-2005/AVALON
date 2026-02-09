from modules.ai_client import client
import json
import re


def blueprint_generation(area, floors, shape="Rectangular", bedrooms=2, kitchen_type="Closed", staircase="Internal"):
    """
    AI-powered blueprint and layout generation using Groq LLM.
    
    Args:
        area: Plot area in square yards
        floors: Number of floors
        shape: Plot shape (Rectangular/Square/Irregular)
        bedrooms: Number of bedrooms
        kitchen_type: Kitchen type (Open/Closed)
        staircase: Staircase type (Internal/External)
    
    Returns:
        Dictionary with intelligent space allocation and layout recommendations
    """
    
    total_area = area * floors
    
    prompt = f"""You are an expert architect and space planner specializing in residential construction in India.

Analyze and provide INTELLIGENT space planning recommendations for this residential project:

PROJECT SPECIFICATIONS:
- Plot Area: {area} square yards
- Number of Floors: {floors}
- Total Built-up Area: {total_area} square yards
- Plot Shape: {shape}
- Number of Bedrooms: {bedrooms}
- Kitchen Type: {kitchen_type}
- Staircase Type: {staircase}

INSTRUCTIONS:
1. Calculate optimal space allocation for each room type based on Indian building standards and best practices
2. Consider Vastu principles where applicable
3. Ensure proper circulation space (15-20% of total area)
4. Provide practical, implementable layout advice specific to the plot shape and configuration
5. Consider natural lighting, ventilation, and privacy requirements
6. Account for structural requirements and building codes

Return ONLY a valid JSON object with this EXACT structure:
{{
    "allocation": {{
        "living_room": <number in sq yards>,
        "bedroom": <number in sq yards - average per bedroom>,
        "kitchen": <number in sq yards>,
        "bathroom": <number in sq yards - total for all bathrooms>,
        "circulation": <number in sq yards - corridors, stairs, etc>,
        "floors": {floors}
    }},
    
    "layout_advice": [
        "Specific layout recommendation 1 based on plot shape and configuration",
        "Specific layout recommendation 2 for optimal space utilization",
        "Specific layout recommendation 3 for lighting and ventilation",
        "Specific layout recommendation 4 for privacy and functionality"
    ],
    
    "config": {{
        "shape": "{shape}",
        "bedrooms": {bedrooms},
        "kitchen": "{kitchen_type}"
    }}
}}

Provide realistic space allocations that sum to approximately {area * 0.6} sq yards (60% of plot area for built space, 40% for open areas).
Make layout advice specific, actionable, and relevant to the given configuration."""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1500
        )
        
        response_text = completion.choices[0].message.content
        result = parse_blueprint_json(response_text)
        
        if result and "allocation" in result:
            return result
        else:
            return fallback_blueprint(area, floors, shape, bedrooms, kitchen_type, staircase)
            
    except Exception as e:
        print(f"Error in AI blueprint generation: {e}")
        return fallback_blueprint(area, floors, shape, bedrooms, kitchen_type, staircase)


def parse_blueprint_json(text):
    """Parse JSON response from Groq LLM"""
    try:
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find raw JSON
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            json_str = json_match.group() if json_match else text
        
        data = json.loads(json_str)
        
        # Validate required fields
        if "allocation" in data and "layout_advice" in data:
            return data
        else:
            return None
            
    except Exception as e:
        print(f"Blueprint JSON parsing error: {e}")
        return None


def fallback_blueprint(area, floors, shape, bedrooms, kitchen_type, staircase):
    """Fallback to basic calculation if AI fails"""
    
    room_area = area * 0.6

    # Basic Area Allocation
    allocation = {
        "living_room": room_area * 0.25,
        "bedroom": room_area * (0.30 if bedrooms > 2 else 0.40),
        "kitchen": room_area * 0.15,
        "bathroom": room_area * 0.10,
        "circulation": room_area * 0.20,
        "floors": floors
    }

    # Layout Recommendations based on inputs
    recommendations = []

    if shape == "Rectangular":
        recommendations.append("Linear arrangement is efficient. Place staircase centrally to minimize corridors.")
    elif shape == "Square":
        recommendations.append("Central courtyard or core design works best for ventilation.")
    elif shape == "Irregular":
        recommendations.append("Use irregular corners for landscaping, storage, or utility areas to keep rooms square.")

    if kitchen_type == "Open":
        recommendations.append("Combine Living and Dining areas for a spacious feel.")
    
    if staircase == "External":
        recommendations.append("Ensure external staircase does not block main facade light.")

    return {
        "allocation": allocation,
        "layout_advice": recommendations,
        "config": {
            "shape": shape,
            "bedrooms": bedrooms,
            "kitchen": kitchen_type
        }
    }
