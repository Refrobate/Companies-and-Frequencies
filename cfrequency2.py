from collections import Counter, defaultdict
import re

# Define the list of acceptable companies (case-insensitive) and their variations
approved_companies = {
    "accenture": ["acc", "acenture"],
    "alix partners": ["alixpartners"],
    "bain": [
        "bain & company", "bain (bain & company)", "bain and company", "bain capital private equity", "bain company", "bain&company", "bane"
    ],
    "bcg": [
        "boston", "boston consulting", "boston consulting company", "boston consulting group", "boston consulting group (bcg)", "bcp"
    ],
    "booz allen hamilton": ["booz", "booz allen", "booze", "allen"],
    "capgemini": ["capgemeni", "capgemini invent", "cap gemini"],
    "cognizant": ["cogningent"],
    "deloitte": ["delloite", "delloitte", "deloutte", "deouitte", "deliotte"],
    "ey": [
        "e&y", "ey (ernst & young)", "ernst & young", "ernst & young (ey)", "ernst and young", "ernst young", "earnst and young", "ey advisory (ernst & young)", "ernst & young (ey) advisory", "eny"
    ],
    "ibm": ["ibm consulting", "ibm global services"],
    "kearney": ["a.t. kearney", "kearny"],
    "kpmg": ["kpmg advisory"],
    "l.e.k consulting": ["lek", "lekzs" "l.e.k"],
    "mckinsey": [
        "mc kinsey", "mckensey", "mckensy", "mckinnsey", "mckinley", "mckinsey & co", "mckinsey & company", "mckinsey and company", "mckinsy", "kinsey", "mikensy"
    ],
    "north highland": [],
    "oliver wyman": ["oliver"],
    "pwc": [
        "pwc advisory (pricewaterhousecoopers)", "price water house coopers", "pricewater cooper", "pricewaterhousecooper", "pricewaterhousecoopers", "pricewaterhousecoopers (pwc)",
        "pwc (pricewaterhousecoopers)", "pwc advisory services", "pwc advisory/strategy&", "pwc strategy", "Pricewaterhousecoopers (Pwc)", "Pwc (Pricewaterhousecoopers)", "p&w", "p&c", "Price Waterhouse Coopers", "pricewater", "pricewater cooper"
    ],
    "slalom": []
}

def preprocess_response(response, approved_companies):
    # Replace multi-word company names with underscores
    for company in approved_companies.keys():
        if " " in company:
            # Create a single-token version for temporary replacement
            single_token = company.replace(" ", "_")
            # Use regex for a case-insensitive replacement in the response
            response = re.sub(r'\b' + re.escape(company) + r'\b', single_token, response, flags=re.IGNORECASE)
    return response

def read_responses_from_file(file_path):
    responses = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.rsplit(',', 1)
            if len(parts) == 2:
                response = parts[0].strip()
                try:
                    frequency = int(parts[1].strip())
                    responses.append((response, frequency))
                except ValueError:
                    print(f"Invalid frequency in line: '{line.strip()}'")
    return responses

def count_companies(responses, approved_companies):
    mention_counter = Counter()
    frequency_counter = defaultdict(int)
    unapproved_mention_counter = Counter()
    unapproved_frequency_counter = defaultdict(int)
    
    for response, frequency in responses:
        # Preprocess to replace multi-word companies with single tokens
        processed_response = preprocess_response(response.lower(), approved_companies)
        
        # Split by commas or spaces
        companies = re.split(r'[,\s]+', processed_response)
        
        for company in companies:
            # Replace underscores back with spaces to match the original names
            company = company.replace("_", " ")
            matched = False
            for approved_name, variations in approved_companies.items():
                if company == approved_name or company in variations:
                    proper_name = approved_name.title() if approved_name not in {"ibm", "bcg", "ey", "pwc"} else approved_name.upper()
                    mention_counter[proper_name] += 1
                    frequency_counter[proper_name] += frequency
                    matched = True
                    break
            
            if not matched:
                unapproved_mention_counter[company] += 1
                unapproved_frequency_counter[company] += frequency
    
    return mention_counter, frequency_counter, unapproved_mention_counter, unapproved_frequency_counter

# Path to your responses file
file_path = 'formatted_responses.txt'

# Read responses from the file
responses = read_responses_from_file(file_path)

# Count the companies
approved_mentions, approved_frequencies, unapproved_mentions, unapproved_frequencies = count_companies(responses, approved_companies)

# Display the tallies for approved companies
print("Approved Companies Tally:")
for company in approved_mentions:
    print(f"{company}: {approved_mentions[company]} mentions, {approved_frequencies[company]} frequency")

# Display the tallies for unapproved companies
print("\nUnapproved Companies Tally:")
for company in unapproved_mentions:
    print(f"{company}: {unapproved_mentions[company]} mentions, {unapproved_frequencies[company]} frequency")
