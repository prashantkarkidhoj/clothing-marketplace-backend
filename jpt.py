def calculate_bmi(weight, height):
    """Calculate Body Mass Index (BMI) given weight in kilograms and height in meters."""
    if height <= 0:
        raise ValueError("Height must be greater than zero.")
    if weight <= 0:
        raise ValueError("Weight must be greater than zero.")
    
    bmi = weight / (height ** 2)
    return bmi