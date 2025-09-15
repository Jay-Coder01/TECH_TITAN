from datetime import date
from django.utils import timezone

def calculate_age(dob):
    """Calculate age from date of birth"""
    if not dob:
        return None
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def check_age_requirement(student, scholarship):
    """Check if student meets age requirements for scholarship"""
    age = calculate_age(student.date_of_birth)
    
    if age is None:
        return False, "Age not specified"
    
    if scholarship.min_age and age < scholarship.min_age:
        return False, f"Too young (min age: {scholarship.min_age})"
    
    if scholarship.max_age and age > scholarship.max_age:
        return False, f"Too old (max age: {scholarship.max_age})"
    
    return True, "Age requirement met"

def check_cgpa_requirement(student, scholarship):
    """Check if student meets CGPA requirements for scholarship (10-point scale)"""
    if not student.cgpa:
        return False, "CGPA not specified"
    
    if scholarship.min_gpa and student.cgpa < float(scholarship.min_cgpa):
        return False, f"CGPA too low (min: {scholarship.min_cgpa})"
    
    return True, "CGPA requirement met"

def check_education_level(student, scholarship):
    """Check if student's education level matches scholarship requirements"""
    if scholarship.education_level == 'any':
        return True, "Education level requirement met"
    
    if student.education_level != scholarship.education_level:
        return False, f"Education level mismatch (required: {scholarship.education_level})"
    
    return True, "Education level requirement met"

def check_citizenship(student, scholarship):
    """Check if student meets citizenship requirements"""
    citizenship_reqs = scholarship.get_citizenship_requirements()
    
    if not citizenship_reqs:  # No citizenship requirements
        return True, "Citizenship requirement met"
    
    if student.citizenship and student.citizenship in citizenship_reqs:
        return True, "Citizenship requirement met"
    
    return False, f"Citizenship requirement not met (required: {', '.join(citizenship_reqs)})"

def check_field_of_study(student, scholarship):
    """Check if student's field of study matches scholarship requirements"""
    field_reqs = scholarship.get_field_of_study_requirements()
    
    if not field_reqs:  # No field requirements
        return True, "Field of study requirement met"
    
    if student.field_of_study and student.field_of_study.lower() in [f.lower() for f in field_reqs]:
        return True, "Field of study requirement met"
    
    return False, f"Field of study mismatch (required: {', '.join(field_reqs)})"

def check_financial_need(student, scholarship):
    """Check if student meets financial need requirements"""
    if not scholarship.income_max and not scholarship.income_min:
        return True, "Financial need requirement met"
    
    if not student.family_income:
        return False, "Family income not specified"
    
    if scholarship.income_max and student.family_income > scholarship.income_max:
        return False, f"Family income too high (max: ₹{scholarship.income_max})"  # Changed to ₹
    
    if scholarship.income_min and student.family_income < scholarship.income_min:
        return False, f"Family income too low (min: ₹{scholarship.income_min})"  # Changed to ₹
    
    return True, "Financial need requirement met"

def check_minority_preferences(student, scholarship):
    """Check if student qualifies for minority preferences"""
    minority_prefs = scholarship.get_minority_preferences()
    
    if not minority_prefs:  # No minority preferences
        return True, "Minority preference requirement met"
    
    student_minorities = student.get_minority_groups()
    
    for minority in minority_prefs:
        if minority in student_minorities:
            return True, f"Qualifies for minority preference ({minority})"
    
    return False, "Does not qualify for minority preferences"

def check_disability_preferences(student, scholarship):
    """Check if student qualifies for disability preferences"""
    disability_prefs = scholarship.get_disability_preferences()
    
    if not disability_prefs:  # No disability preferences
        return True, "Disability preference requirement met"
    
    student_disabilities = student.get_disabilities()
    
    for disability in disability_prefs:
        if disability in student_disabilities:
            return True, f"Qualifies for disability preference ({disability})"
    
    return False, "Does not qualify for disability preferences"

def check_scholarship_type(student, scholarship):
    """Check scholarship type specific requirements"""
    if scholarship.scholarship_type == 'merit':
        # For merit-based scholarships, CGPA is important (10-point scale)
        if not student.cgpa or student.cgpa < 7.0:  # Changed threshold to 7.0 CGPA
            return False, "Insufficient CGPA for merit-based scholarship"
        return True, "Meets merit-based requirements"
    
    elif scholarship.scholarship_type == 'need':
        # For need-based scholarships, financial need is important
        if not student.financial_aid_needed:
            return False, "No financial need demonstrated"
        return True, "Meets need-based requirements"
    
    elif scholarship.scholarship_type == 'athletic':
        # Check if student has athletic extracurriculars
        extracurriculars = student.get_extracurriculars()
        athletic_activities = ['sports', 'athletics', 'basketball', 'football', 'soccer', 
                            'tennis', 'swimming', 'track', 'field', 'volleyball']
        
        has_athletic = any(any(activity in ext.lower() for activity in athletic_activities) 
                        for ext in extracurriculars)
        
        if not has_athletic:
            return False, "No athletic activities found"
        return True, "Meets athletic scholarship requirements"
    
    # Add more scholarship type checks as needed
    
    return True, "Scholarship type requirements met"

# All rules to be applied
ALL_RULES = [
    check_age_requirement,
    check_cgpa_requirement,  # Changed from check_cgpa_requirement
    check_education_level,
    check_citizenship,
    check_field_of_study,
    check_financial_need,
    check_minority_preferences,
    check_disability_preferences,
    check_scholarship_type,
]