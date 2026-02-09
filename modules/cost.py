from modules.ai_client import client
import json
import re
from datetime import datetime


def cost_estimation(area, floors, quality="Standard", priority="Balanced", location="India"):
    """
    AI-powered cost estimation using Groq LLM with real-time market data.
    
    Args:
        area: Plot area in square yards
        floors: Number of floors
        quality: Quality level (Economy/Standard/Premium/Luxury)
        priority: Priority (Balanced/Speed)
        location: Location for market-specific pricing
    
    Returns:
        Dictionary with detailed cost breakdown and AI explanation
    """
    
    total_area = area * floors
    current_date = datetime.now().strftime("%B %Y")
    
    prompt = f"""You are an expert construction cost estimator with access to current market data for {current_date}.

Analyze and provide a DETAILED cost estimation for this construction project:

PROJECT SPECIFICATIONS:
- Location: {location}
- Plot Area: {area} square yards
- Number of Floors: {floors}
- Total Built-up Area: {total_area} square yards
- Quality Level: {quality}
- Priority: {priority}

INSTRUCTIONS:
1. Use CURRENT {current_date} market rates for construction materials and labor in {location}
2. Consider quality level impact on material selection and finishing
3. Factor in priority (Speed requires premium labor rates and potential material wastage)
4. Provide realistic, market-competitive pricing

Return ONLY a valid JSON object with this exact structure:
{{
    "material_cost": <number>,
    "labour_cost": <number>,
    "overhead": <number>,
    "contingency": <number>,
    "total_cost": <number>,
    "cost_per_sqyd": <number>,
    "breakdown_explanation": {{
        "material_details": "Detailed explanation of material costs including cement, steel, bricks, sand, aggregates, finishing materials, etc. with current market rates",
        "labour_details": "Detailed explanation of labor costs including masons, helpers, skilled workers, supervisors with current wage rates",
        "overhead_details": "Explanation of overhead costs including site management, utilities, equipment rental, etc.",
        "contingency_details": "Explanation of contingency buffer for price fluctuations and unforeseen expenses",
        "quality_impact": "How the {quality} quality level affects material selection and overall cost",
        "priority_impact": "How the {priority} priority affects timeline, labor costs, and material procurement",
        "market_factors": "Current market conditions, material availability, and pricing trends for {current_date}",
        "cost_justification": "Overall justification for the total cost estimate with key cost drivers"
    }}
}}

Be specific with numbers and percentages. Use realistic current market rates."""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,  # Slightly higher for more detailed explanations
            max_tokens=2000
        )
        
        response_text = completion.choices[0].message.content
        result = parse_cost_json(response_text)
        
        # Ensure all numeric fields are present and valid
        if result and "material_cost" in result:
            return result
        else:
            # Fallback to basic calculation if AI response is incomplete
            return fallback_calculation(area, floors, quality, priority)
            
    except Exception as e:
        print(f"Error in AI cost estimation: {e}")
        return fallback_calculation(area, floors, quality, priority)


def parse_cost_json(text):
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
        required_fields = ["material_cost", "labour_cost", "overhead", "contingency", "total_cost"]
        if all(field in data for field in required_fields):
            return data
        else:
            return None
            
    except Exception as e:
        print(f"JSON parsing error: {e}")
        return None


def fallback_calculation(area, floors, quality, priority):
    """Fallback to basic calculation if AI fails"""
    total_area = area * floors
    
    # Base Rates (Standard) - Updated for 2026
    base_material = 1500
    base_labour = 800
    
    # Quality Multipliers
    quality_factors = {
        "Economy": 0.8,
        "Standard": 1.0,
        "Premium": 1.3,
        "Luxury": 1.6
    }
    q_mult = quality_factors.get(quality, 1.0)
    
    # Priority Adjustment
    p_mult = 1.15 if priority == "Speed" else 1.0
    
    material_cost = total_area * base_material * q_mult
    labour_cost = total_area * base_labour * q_mult * p_mult
    overhead = 0.1 * (material_cost + labour_cost)
    contingency = 0.05 * (material_cost + labour_cost)
    total_cost = material_cost + labour_cost + overhead + contingency
    
    return {
        "material_cost": round(material_cost),
        "labour_cost": round(labour_cost),
        "overhead": round(overhead),
        "contingency": round(contingency),
        "total_cost": round(total_cost),
        "cost_per_sqyd": round(total_cost / total_area) if total_area else 0,
        "breakdown_explanation": {
            "material_details": f"Basic material calculation: {total_area} sq yd × ₹{base_material * q_mult}/sq yd",
            "labour_details": f"Basic labor calculation: {total_area} sq yd × ₹{base_labour * q_mult * p_mult}/sq yd",
            "overhead_details": "10% of material and labor costs for site management",
            "contingency_details": "5% buffer for unforeseen expenses",
            "quality_impact": f"{quality} quality multiplier: {q_mult}x",
            "priority_impact": f"{priority} priority multiplier: {p_mult}x on labor",
            "market_factors": "Fallback calculation - AI estimation unavailable",
            "cost_justification": "Standard calculation based on average market rates"
        }
    }
