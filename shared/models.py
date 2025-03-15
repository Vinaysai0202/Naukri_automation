from pydantic import BaseModel
from typing import Union
import re

def extract_resume_info(row_resume_text):
    
    pattern = r'(?i)(duration|rate|experience|experienced|months|years|month|year|yrs)'
    replacement = r' \1 '
    new_text = re.sub(pattern, replacement, row_resume_text,flags=re.IGNORECASE)
    resume_text = re.sub(r'\s+', ' ', new_text).strip()

    experience_pattern = re.compile(r'''
        (\d+\+\s*years?) | (\d+\s*-\s*\d+\s*years?) | (\d+\+\s*year) |
        (\d+\s*years?) | (\d+\s*-\s*\d+\s*year) |(\d+\s*year) |(\d+\s*yrs)
    ''', re.VERBOSE | re.IGNORECASE)
    
    duration_pattern = re.compile(r'''
        \b(?:(?:Duration|Length)\s*(?::\s*|\s+) |)(\d+\+?\s*month(?:'s)?|\d+\+?\s*months|\d+\+?\s*year
        (?:'s)?|\d+\+?\s*years)\b(?!\s*(?:experience|experienced))  
    ''', re.VERBOSE | re.IGNORECASE)
    
    rate_pattern = re.compile(r'\$\s*\d{1,4}(?:\.\d{2})?\s*(?:\/hr)?|\d{1,4}\s*\$\s*(?:\/hr)?|\d{1,4}\s*\$\s*(?:\/hr)?', re.IGNORECASE)
  
    extracted_experience = re.findall(experience_pattern, resume_text)
    experience_list =  list(set([item for sublist in extracted_experience for item in sublist if item]))
   
    duration_matches = re.findall(duration_pattern, resume_text)
    duration_list = list(set([match.strip() for match in duration_matches]))
   
    rate_matches = re.findall(rate_pattern, resume_text)
    rate = list(set([match.strip() for match in rate_matches]))

    def parse_experience(exp):
        if '+' in exp:
            num = int(re.search(r'\d+', exp).group())
            return {"min": num, "max": None}
        elif '-' in exp:
            nums = list(map(int, re.findall(r'\d+', exp)))
            return {"min": nums[0], "max": nums[1]}
        else:
            num = int(re.search(r'\d+', exp).group())
            return {"min": None, "max": num}
    
    def normalize_duration(durations):
        """Normalize the duration format to 'x years'."""
        result = []
        for duration in durations:
            # Handle singular "1 year" separately
            if re.match(r'\s*(0|1)\s*year\s*$', duration):
                result.append(re.sub(r'\s+', ' ', duration))
            else:   
                duration = duration.strip().lower()
                duration = re.sub(r'(\d+)\s*-\s*(\d+)\s*years?', r'\1-\2 years', duration)
                duration = re.sub(r'(\d+)\s*years?', r'\1 years', duration)
                result.append(duration)
        return result

    def extract_durations_from_patterns(experience):
        """Extract all individual durations from experience patterns."""
        exp_ranges = []
        experience_patterns = normalize_duration(experience)
        for exp in experience_patterns:
            match = re.match(r'(\d+)-(\d+) years', exp)
            if match:
                end = int(match.group(2))
                exp_ranges.append(f"{end} years") if end >1 else exp_ranges.append(f"{end} year")
                
        return exp_ranges
        
    def remove_matching_durations(experience, durations):
        """Remove all durations that match the experience patterns."""
        items_to_remove = extract_durations_from_patterns(experience)
        normalized_durations = normalize_duration(durations) 

        return [item for item in normalized_durations if item not in items_to_remove]
    
    durations = [d for d in duration_list if d not in  experience_list]
    
    filtered_duration = remove_matching_durations(experience_list, durations)
    
    parsed_experience = [parse_experience(exp) for exp in experience_list]
    
    experience = parsed_experience[0] if parsed_experience else {"min": None, "max": None}
    duration = filtered_duration[0] if filtered_duration else None
    rate = rate[0] if rate else None
    
    return {   
        "Parsed Experience:" : experience,
        "Duration:" : duration,
        "Rate:": rate
    }
    
class VMsExtractRequest(BaseModel):

    login_email: str=None
    login_password: str=None


def extract_project_location(address):
    """
    This function will return the project location along with address
    """
    try:
        project_location = ""
        if "remote" in str(address).lower():
            project_location = "Remote"
            if str(address).lower() == "remote":
                address = None
        elif "hybrid" in str(address).lower():
            project_location = "Hybrid"
            if str(address).lower() == "hybrid":
                address = None
        elif "onsite" in str(address).lower():
            project_location = "Onsite"
            if str(address).lower() == "onsite":
                address = None
        else:
            project_location = None
        return address,project_location
    except Exception as e:
        return None,None