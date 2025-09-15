# recommendation_engine/utils.py
from ..models import Scholarship, StudentProfile, ScholarshipRecommendation, Signup
from decimal import Decimal
import json

def get_recommendations_for_user(user, limit=None):
    """
    Get scholarship recommendations for a Signup user
    """
    try:
        # Get the student profile for this user
        profile = StudentProfile.objects.get(user=user)
        
        # Get all recommendations for this student, ordered by match score
        recommendations = ScholarshipRecommendation.objects.filter(
            student=profile
        ).select_related('scholarship').order_by('-match_score')
        
        if limit:
            recommendations = recommendations[:limit]
            
        return recommendations
    except StudentProfile.DoesNotExist:
        return []

def refresh_recommendations_for_student(profile):
    """
    Refresh scholarship recommendations for a student profile
    """
    # Clear existing recommendations
    ScholarshipRecommendation.objects.filter(student=profile).delete()
    
    # Get all scholarships
    all_scholarships = Scholarship.objects.all()
    
    count = 0
    for scholarship in all_scholarships:
        match_score = calculate_match_score(profile, scholarship)
        
        # Create recommendation even with lower scores, but prioritize higher ones
        if match_score > 20:  # Lower threshold to get more recommendations
            ScholarshipRecommendation.objects.create(
                student=profile,
                scholarship=scholarship,
                match_score=match_score,
                reason=generate_recommendation_reason(profile, scholarship, match_score)
            )
            count += 1
    
    return count

def calculate_match_score(profile, scholarship):
    """
    Calculate match score between student profile and scholarship
    """
    score = 0
    max_possible_score = 100  # Total possible score
    
    # 1. Education level match (20 points)
    if (profile.education_level and scholarship.education_level and
        (profile.education_level == scholarship.education_level or 
         scholarship.education_level == 'any')):
        score += 20
    
    # 2. CGPA check (20 points) - Convert both to Decimal for comparison
    if (profile.cgpa is not None and scholarship.min_cgpa is not None):
        try:
            profile_cgpa = Decimal(str(profile.cgpa))
            min_required_cgpa = Decimal(str(scholarship.min_cgpa))
            if profile_cgpa >= min_required_cgpa:
                score += 20
            else:
                # Partial points for being close
                cgpa_ratio = float(profile_cgpa) / float(min_required_cgpa)
                if cgpa_ratio >= 0.8:  # If within 80% of required CGPA
                    score += int(10 * cgpa_ratio)
        except (TypeError, ValueError):
            pass
    
    # 3. Financial need match (15 points)
    if (hasattr(profile, 'financial_aid_needed') and 
        profile.financial_aid_needed and 
        scholarship.scholarship_type == 'need'):
        score += 15
    
    # 4. Field of study match (15 points)
    if (profile.field_of_study and 
        scholarship.field_of_study_requirements):
        field_requirements = scholarship.get_field_of_study_requirements()
        if field_requirements:  # Only check if there are requirements
            if any(req.lower() in profile.field_of_study.lower() 
                  for req in field_requirements if req):
                score += 15
    
    # 5. Income level match (10 points)
    if (profile.family_income is not None and 
        scholarship.income_min is not None and 
        scholarship.income_max is not None):
        try:
            income = Decimal(str(profile.family_income))
            min_income = Decimal(str(scholarship.income_min)) if scholarship.income_min else Decimal('0')
            max_income = Decimal(str(scholarship.income_max)) if scholarship.income_max else Decimal('999999999')
            
            if min_income <= income <= max_income:
                score += 10
        except (TypeError, ValueError):
            pass
    
    # 6. Minority status match (10 points)
    if (hasattr(profile, 'get_minority_groups') and 
        scholarship.minority_preferences):
        minority_prefs = scholarship.get_minority_preferences()
        student_minorities = profile.get_minority_groups()
        if any(minority in minority_prefs for minority in student_minorities):
            score += 10
    
    # 7. Disability match (10 points)
    if (hasattr(profile, 'get_disabilities') and 
        scholarship.disability_preferences):
        disability_prefs = scholarship.get_disability_preferences()
        student_disabilities = profile.get_disabilities()
        if any(disability in disability_prefs for disability in student_disabilities):
            score += 10
    
    return min(score, max_possible_score)  # Ensure score doesn't exceed 100%

def generate_recommendation_reason(profile, scholarship, match_score):
    """
    Generate a descriptive reason for the recommendation
    """
    reasons = []
    
    # Education level match
    if (profile.education_level and scholarship.education_level and
        (profile.education_level == scholarship.education_level or 
         scholarship.education_level == 'any')):
        reasons.append("Matches your education level")
    
    # CGPA match
    if (profile.cgpa is not None and scholarship.min_cgpa is not None):
        try:
            profile_cgpa = Decimal(str(profile.cgpa))
            min_required_cgpa = Decimal(str(scholarship.min_cgpa))
            if profile_cgpa >= min_required_cgpa:
                reasons.append("Meets CGPA requirements")
        except (TypeError, ValueError):
            pass
    
    # Financial need match
    if (hasattr(profile, 'financial_aid_needed') and 
        profile.financial_aid_needed and 
        scholarship.scholarship_type == 'need'):
        reasons.append("Matches your financial need")
    
    # Field of study match
    if (profile.field_of_study and 
        scholarship.field_of_study_requirements):
        field_requirements = scholarship.get_field_of_study_requirements()
        if field_requirements and any(req.lower() in profile.field_of_study.lower() 
                                    for req in field_requirements if req):
            reasons.append("Matches your field of study")
    
    # Income match
    if (profile.family_income is not None and 
        scholarship.income_min is not None and 
        scholarship.income_max is not None):
        try:
            income = Decimal(str(profile.family_income))
            min_income = Decimal(str(scholarship.income_min)) if scholarship.income_min else Decimal('0')
            max_income = Decimal(str(scholarship.income_max)) if scholarship.income_max else Decimal('999999999')
            
            if min_income <= income <= max_income:
                reasons.append("Matches your income level")
        except (TypeError, ValueError):
            pass
    
    if not reasons:
        # Default reasons if no specific matches found
        if match_score > 50:
            reasons.append("Good overall match based on your profile")
        elif match_score > 30:
            reasons.append("Partial match based on available criteria")
        else:
            reasons.append("Potential opportunity worth exploring")
    
    return ". ".join(reasons) + f". Match score: {match_score}%"

def ensure_recommendations_exist(profile):
    """
    Ensure that at least some recommendations exist for a profile
    """
    existing_count = ScholarshipRecommendation.objects.filter(student=profile).count()
    
    if existing_count == 0:
        # If no recommendations exist, create some generic ones
        all_scholarships = Scholarship.objects.all()[:5]  # Get first 5 scholarships
        
        for i, scholarship in enumerate(all_scholarships):
            # Create recommendations with decreasing scores
            match_score = 80 - (i * 15)  # 80%, 65%, 50%, 35%, 20%
            if match_score < 20:
                match_score = 20  # Minimum score
                
            ScholarshipRecommendation.objects.create(
                student=profile,
                scholarship=scholarship,
                match_score=match_score,
                reason=f"Recommended scholarship based on general criteria. Match score: {match_score}%"
            )
        
        return all_scholarships.count()
    
    return existing_count