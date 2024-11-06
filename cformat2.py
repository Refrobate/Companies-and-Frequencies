import re
from collections import defaultdict

# Define the list of acceptable companies (case-insensitive) and their variations
approved_companies = {
    "accenture": ["acc"],
    "alix partners": ["alixpartners"],
    "bain": [
        "bain & company", "bain (bain & company)", "bain and company", "bain capital private equity", "bain company", "bain&company"
    ],
    "bcg": [
        "boston", "boston consulting", "boston consulting company", "boston consulting group", "boston consulting group (bcg)"
    ],
    "booz allen hamilton": ["booz", "booz allen", "booze"],
    "capgemini": ["capgemeni", "capgemini invent", "cap gemini"],
    "cognizant": ["cogningent"],
    "deloitte": ["delloite", "delloitte", "deloutte", "deouitte"],
    "ey": [
        "e&y", "ey (ernst & young)", "ernst & young", "ernst & young (ey)", "ernst and young", "ernst young"
    ],
    "ibm": ["ibm consulting", "ibm global services"],
    "kearney": ["a.t. kearney", "kearny"],
    "kpmg": ["kpmg advisory"],
    "l.e.k consulting": ["lek", "lekzs"],
    "mckinsey": [
        "mc kinsey", "mckensey", "mckensy", "mckinnsey", "mckinley", "mckinsey & co", "mckinsey & company", "mckinsey and company", "mckinsy", "ey advisory (ernst & young)"
    ],
    "north highland": [],
    "oliver wyman": ["oliver"],
    "pwc": [
        "pwc advisory (pricewaterhousecoopers)", "price water house coopers", "pricewater cooper", "pricewaterhousecooper", "pricewaterhousecoopers", "pricewaterhousecoopers (pwc)",
        "pwc (pricewaterhousecoopers)", "pwc advisory services", "pwc advisory/strategy&", "pwc strategy"
    ],
    "slalom": []
}

def read_responses_from_file(file_path):
    responses = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split by comma and strip whitespace
            parts = line.strip()
            if len(parts) > 0:
                responses.append(parts)
    return responses

def format_responses(responses, approved_companies):
    formatted_responses = defaultdict(int)

    # Correct formatting issues
    for response in responses:
        # If no commas exist, assume the companies are listed without commas
        if ' ' not in response and len(response.split()) > 1:
            response = re.sub(r'([a-zA-Z])([A-Z])', r'\1, \2', response)
        
        # Split by commas and clean whitespace
        companies = [company.strip().lower() for company in response.split(',')]

        # Process each company in the response
        for company in companies:
            matched = False
            for approved_name, variations in approved_companies.items():
                # Check if company matches any of the variations (case insensitive)
                if any(variation.lower() == company for variation in variations):
                    formatted_responses[approved_name] += 1
                    matched = True
                    break

            # If no match is found, it is considered an unapproved company
            if not matched:
                formatted_responses[company] += 1

    return formatted_responses

def write_formatted_responses(file_path, formatted_responses):
    with open(file_path, 'w') as file:
        for company, frequency in formatted_responses.items():
            file.write(f"{company.title()}, {frequency}\n")

# Path to your raw responses file
raw_responses_path = 'raw_responses.txt'
# Path to your formatted responses output file
formatted_responses_path = 'formatted_responses.txt'

# Read responses from the raw file
responses = read_responses_from_file(raw_responses_path)

# Format the responses and correct issues
formatted_responses = format_responses(responses, approved_companies)

# Write the formatted responses to the output file
write_formatted_responses(formatted_responses_path, formatted_responses)

print("Formatted responses have been written to", formatted_responses_path)
