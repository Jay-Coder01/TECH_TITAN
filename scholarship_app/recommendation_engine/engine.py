from . import rules
from scholarship_app.models import ScholarshipRecommendation
from django.utils import timezone

class RecommendationEngine:
    def __init__(self, student_profile):
        self.student = student_profile
        self.scholarships = None
    
    def get_eligible_scholarships(self):
        """Get all scholarships that the student is eligible for"""
        from scholarship_app.models import Scholarship
        
        self.scholarships = Scholarship.objects.filter(deadline__gte=timezone.now().date())
        recommendations = []
        
        for scholarship in self.scholarships:
            score, reasons = self.calculate_match_score(scholarship)
            
            if score > 0:  # Only include scholarships with positive match score
                recommendations.append({
                    'scholarship': scholarship,
                    'score': score,
                    'reasons': reasons
                })
        
        # Sort by match score (descending)
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations
    
    def calculate_match_score(self, scholarship):
        """Calculate match score for a single scholarship"""
        total_score = 100  # Start with perfect score
        reasons = []
        
        for rule in rules.ALL_RULES:
            passed, reason = rule(self.student, scholarship)
            
            if not passed:
                # Deduct points for failed requirements
                # Different rules have different weights
                weight = self.get_rule_weight(rule)
                total_score -= weight
                
                # If a critical requirement fails, set score to 0
                if self.is_critical_rule(rule) and not passed:
                    total_score = 0
                    reasons.append(f"CRITICAL: {reason}")
                    break
            else:
                reasons.append(reason)
        
        # Ensure score is within 0-100 range
        total_score = max(0, min(100, total_score))
        
        return total_score, reasons
    
    def get_rule_weight(self, rule):
        """Define weights for different rules"""
        weights = {
            rules.check_age_requirement: 25,  # Critical
            rules.check_education_level: 25,  # Critical
            rules.check_cgpa_requirement: 20,  # Changed from GPA to CGPA
            rules.check_citizenship: 20,      # Important
            rules.check_field_of_study: 15,   # Medium
            rules.check_financial_need: 10,   # Medium
            rules.check_scholarship_type: 10, # Medium
            rules.check_minority_preferences: 5,  # Bonus
            rules.check_disability_preferences: 5,  # Bonus
        }
        
        return weights.get(rule, 10)  # Default weight
    
    def is_critical_rule(self, rule):
        """Define which rules are critical (if failed, scholarship is ineligible)"""
        critical_rules = {
            rules.check_age_requirement,
            rules.check_education_level,
            rules.check_citizenship,
        }
        
        return rule in critical_rules
    
    def save_recommendations(self):
        """Save recommendations to database"""
        recommendations = self.get_eligible_scholarships()
        
        # Delete existing recommendations for this student
        ScholarshipRecommendation.objects.filter(student=self.student).delete()
        
        # Create new recommendations
        for rec in recommendations:
            reason_text = "\n".join(rec['reasons'])
            ScholarshipRecommendation.objects.create(
                student=self.student,
                scholarship=rec['scholarship'],
                match_score=rec['score'],
                reason=reason_text
            )
        
        return len(recommendations)