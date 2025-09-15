from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json


class Signup(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class StudentProfile(models.Model):
    user = models.OneToOneField(Signup, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    citizenship = models.CharField(max_length=100, blank=True)
    
    # Academic Information
    education_level = models.CharField(max_length=20, choices=[
        ('high_school', 'High School'),
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('phd', 'PhD'),
    ])
    field_of_study = models.CharField(max_length=100, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # Changed from gpa to cgpa
    graduation_year = models.IntegerField(null=True, blank=True)
    
    # Financial Information
    family_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    financial_aid_needed = models.BooleanField(default=False)
    
    # Additional Criteria
    extracurriculars = models.TextField(blank=True)  # JSON stored as text
    achievements = models.TextField(blank=True)      # JSON stored as text
    disabilities = models.TextField(blank=True)      # JSON stored as text
    minority_groups = models.TextField(blank=True)   # JSON stored as text
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_extracurriculars(self):
        try:
            return json.loads(self.extracurriculars) if self.extracurriculars else []
        except:
            return []
    
    def get_achievements(self):
        try:
            return json.loads(self.achievements) if self.achievements else []
        except:
            return []
    
    def get_disabilities(self):
        try:
            return json.loads(self.disabilities) if self.disabilities else []
        except:
            return []
    
    def get_minority_groups(self):
        try:
            return json.loads(self.minority_groups) if self.minority_groups else []
        except:
            return []
    
    def __str__(self):
        return f"{self.user.name}'s Profile" 

class Scholarship(models.Model):
    SCHOLARSHIP_TYPES = [
        ('merit', 'Merit-Based'),
        ('need', 'Need-Based'),
        ('athletic', 'Athletic'),
        ('creative', 'Creative Arts'),
        ('minority', 'Minority'),
        ('international', 'International'),
        ('disability', 'Disability'),
        ('field_specific', 'Field Specific'),
    ]
    
    EDUCATION_LEVELS = [
        ('high_school', 'High School'),
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('phd', 'PhD'),
        ('any', 'Any'),
    ]
    
    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    description = models.TextField()
    eligibility = models.TextField()
    application_process = models.TextField()
    website = models.URLField()
    scholarship_type = models.CharField(max_length=20, choices=SCHOLARSHIP_TYPES)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVELS)
    
    # Eligibility Rules (for rule-based engine)
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # Changed max_digits to 4
    max_age = models.IntegerField(null=True, blank=True)
    min_age = models.IntegerField(null=True, blank=True)
    citizenship_requirements = models.TextField(blank=True)  # JSON stored as text
    field_of_study_requirements = models.TextField(blank=True)  # JSON stored as text
    minority_preferences = models.TextField(blank=True)  # JSON stored as text
    disability_preferences = models.TextField(blank=True)  # JSON stored as text
    income_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    income_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_citizenship_requirements(self):
        try:
            return json.loads(self.citizenship_requirements) if self.citizenship_requirements else []
        except:
            return []
    
    def get_field_of_study_requirements(self):
        try:
            return json.loads(self.field_of_study_requirements) if self.field_of_study_requirements else []
        except:
            return []
    
    def get_minority_preferences(self):
        try:
            return json.loads(self.minority_preferences) if self.minority_preferences else []
        except:
            return []
    
    def get_disability_preferences(self):
        try:
            return json.loads(self.disability_preferences) if self.disability_preferences else []
        except:
            return []
    
    def __str__(self):
        return self.title
    
    def is_deadline_approaching(self):
        return self.deadline <= timezone.now().date() + timezone.timedelta(days=30)

class ScholarshipRecommendation(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    match_score = models.DecimalField(max_digits=5, decimal_places=2)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'scholarship')
    
    def __str__(self):
        return f"{self.student.user.username} - {self.scholarship.title} ({self.match_score}%)"

class ForumTopic(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class ForumReply(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE)
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reply to {self.topic.title} by {self.user.username}"