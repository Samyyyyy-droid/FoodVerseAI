
def classify_freshness(features, food_name="Food"):

    brightness = features["brightness"]
    saturation = features["saturation"]
    edge_density = features["edge_density"]

    # Evaluate visible image characteristics
    if brightness < 35 and saturation < 40:
        freshness_level = "Moderate"
        safety_status = "Inspect Before Consumption"
        confidence = 65
        signs = ["Low brightness", "Low colour saturation"]

    elif brightness > 180 and saturation > 180:
        freshness_level = "Moderate"
        safety_status = "Inspect Before Consumption"
        confidence = 60
        signs = ["High brightness", "High saturation"]

    else:
        freshness_level = "Requires Further Inspection"
        safety_status = "Visual Assessment Inconclusive"
        confidence = 50
        signs = ["Visual features extracted successfully"]

    return {
        "item_name": food_name,
        "freshness_level": freshness_level,
        "confidence": confidence,
        "safety_status": safety_status,
        "detected_signs": signs,
        "image_features": {
            "brightness": brightness,
            "saturation": saturation,
            "edge_density": edge_density
        },
        "reasoning": "Assessment based on extracted visual characteristics. "
                     "Image analysis alone cannot confirm food safety.",
        "recommendation": "Check storage conditions, expiry date, smell "
                          "and visible signs of spoilage before consumption."
    }
