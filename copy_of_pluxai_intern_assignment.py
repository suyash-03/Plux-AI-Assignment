# -*- coding: utf-8 -*-
"""Copy of PluxAI Intern Assignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HMQcaBAo6fhsCjcMtMf7nTeeYVeK2R_O
"""

#@title PluxAI Intern Assignment (May 22, 2024)

# @markdown ### Please enter your details:
# @markdown #### Full Name
name = 'Suyash Singh' # @param {type:"string"}

# @markdown #### Email  (please enter the same email as mentioned in the Plux AI application form)
email = 'f20201540@pilani.bits-pilani.ac.in' # @param {type:"string"}

# @markdown #### Graduation Year
graduation_year = '2024' # @param ["2022", "2023", "2024", "2025", "2026"] {allow-input: true}

"""# Assignment Details:

This assignment involves building an end-to-end question answering (Q&A) system that operates on a provided dataset containing information about investment funds and their investments. Your goal is to develop a pipeline that accurately answers user queries based on the data from two CSV files: filer.csv and investment.csv. You will implement this project in  notebook.


### Dataset description

The dataset contains two CSV files:

##### filer.csv: Contains information about investment funds.
    name: Name of the fund.
    cik: Unique identifier for each fund.
    series: Series of the fund.
    series_id: Unique identifier for each series.
    total_assets: Total assets of the fund.
    total_liabilities: Total liabilities of the fund.

##### investment.csv: Contains information about individual investments made by each fund.
    cik: Unique identifier of the fund that made the investment.
    investment_name: Name of the investment.
    value_usd: Value of the investment in USD.
    percentage_investment: Percentage of the fund's total assets invested in this particular investment.

### Assignment Breakdown:
The assignment is divided into four sections with increasing complexity:
1. Test Setup (10 points)
2. Basic data analysis (15 points)
3. Basic QnA (25 points)
4. Complex QnA (50 points)

### Notes
- If full implementation is challenging, you may provide a detailed textual description of your proposed approach and logic.
- You are encouraged to utilize LLMs like Gemini 1.5 Pro to enhance your QnA system for this section.
- While handling a variety of questions is valuable, your primary focus should be on the accuracy of the answers provided by your Q&A system.

### Assignment Feedback

P.S. Here is an anonymous [feedback link](https://forms.gle/2aLVTQU28zV2fHnF6) for the assignment. It'd be great if you can provide your feedback about the assignment as we are continuously looking to improve our recruiting process.

"""

from google.colab import drive
drive.mount('/content/drive')

#@title Test Setup (10 points)

#@markdown ## Test basic understanding of pandas.

#@markdown ###Complete the following tasks:
#@markdown 1. Download filer.csv and investment.csv from [Kaggle.](https://www.kaggle.com/datasets/robotgames/sec-edgar-archive-nport-form-data-2020-quarter-1)
#@markdown 2. Load the data into two dataframes -> filer_df and investment_df
#@markdown 3. Implement a function which takes a firm name from filer_df and lists down all the investements made by that firm from investment_df.

#@markdown > def get_investments(filer_df, investment_df, firm_name):
#@markdown >    #Implement your code here
#@markdown
import pandas as pd

filer_df = pd.read_csv('/content/drive/MyDrive/Plux AI Dataset/filer.csv')
investment_df = pd.read_csv('/content/drive/MyDrive/Plux AI Dataset/investment.csv')

columns_filer = filer_df.columns.tolist()
columns_investment = investment_df.columns.tolist()


print(columns_filer)
print(columns_investment)

#@markdown complete the above tasks and implement this function
  #@markdown > get_investments(filer_df, investment_df, "1290 Funds")
  #@markdown > should return ['Garda World Security Corp.', 'Tempo Acquisition LLC', ...and so on]
def get_investments(filer_df, investment_df, firm_name):
  firm_cik = filer_df.loc[filer_df['name'] == firm_name, 'cik']
  if firm_cik.empty:
    return f"No firm found with the name {firm_name}"
  firm_cik = firm_cik.iloc[0]
  firm_investments = investment_df[investment_df['cik'] == firm_cik]
  if firm_investments.empty:
    return f"No investments found for the firm {firm_name}"
  return firm_investments
  pass

firm_investments = get_investments(filer_df,investment_df,'1290 Funds')
print(firm_investments)

#@title Basic data analysis (15 points)

#@markdown ###Implement the following functionality:
#@markdown 1. Get highest individual investment_name for each cik.
#@markdown 2. Get investment_name which has occurred the most across a cik.
#@markdown 3. Give total positive and negative investment for each cik.

def get_highest_individual_investment(filer_df, investment_df, cik):
  firm_investments = investment_df[investment_df['cik'] == cik]
  if firm_investments.empty:
    return f"No investments found for the cik {cik}"

  highest_investment = firm_investments.loc[firm_investments['value_USD'].idxmax()]
  return (highest_investment['cik'], highest_investment['investment_name'], highest_investment['value_USD'], highest_investment['percentage_investment'])

  pass

def get_most_occurred_investment_name(filer_df, investment_df, cik):
  firm_investments = investment_df[investment_df['cik'] == cik]
  if firm_investments.empty:
    return f"No investments found for the cik {cik}"

  most_occurred_investment = firm_investments['investment_name'].mode()
  if most_occurred_investment.empty:
    return f"No investment names found for the cik {cik}"

  return most_occurred_investment.iloc[0]
  pass

def get_total_positive_and_negative_investment(filer_df, investment_df, cik): #check
  firm_investments = investment_df[investment_df['cik'] == cik]
  if firm_investments.empty:
    return f"No investments found for the cik {cik}"

  positive_investments = firm_investments[firm_investments['value_USD'] > 0]['value_USD'].sum()
  negative_investments = firm_investments[firm_investments['value_USD'] < 0]['value_USD'].sum()

  return {
      'cik': cik,
      'total_positive_investment': positive_investments,
      'total_negative_investment': negative_investments
  }

  # i don't understand why this method should return United States of America
  # as given in the example, i decided to do it this way
  pass

print(get_highest_individual_investment(filer_df, investment_df, 1605941))
print(get_most_occurred_investment_name(filer_df, investment_df, 1605941))
print(get_total_positive_and_negative_investment(filer_df, investment_df, 1605941))

#@title Basic QnA (25 points) - LLM begins

#@markdown #### You are responsible to compute the results for above functions itself but through natural language.
#@markdown #### Implement the following function:
#@markdown #### <code> answer_basic_query(filer_df, investment_df, query_str) </code>

#@markdown ```
#@markdown Eg. answer_basic_query(filer_df, investment_df, "What is the most occurred investment name for cik 1605941 ?") should return 'United States of America'
#@markdown ```

#@markdown Note: Basic query need to just handle queries specific to functions in Basic Data Analysis.

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_query(query_str):
    # Tokenize the query
    tokens = word_tokenize(query_str.lower())

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    return filtered_tokens

def classify_query(query_tokens):
    # Define the query types and their associated keywords
    query_types = {
        'most_occurred': ['most', 'occurred', 'investment', 'name'],
        'highest_individual': ['highest', 'individual', 'investment'],
        'total_investments': ['total', 'positive', 'negative', 'investment']
    }

    # Compute the bag-of-words representation of the query
    query_bow = Counter(query_tokens)

    # Classify the query based on keyword matches
    best_match = None
    max_score = 0
    for query_type, keywords in query_types.items():
        score = sum(query_bow[keyword] for keyword in keywords)
        if score > max_score:
            max_score = score
            best_match = query_type

    return best_match

def answer_basic_query(filer_df, investment_df, query_str):
    # Preprocess the query string
    query_tokens = preprocess_query(query_str)

    # Classify the query
    query_type = classify_query(query_tokens)

    # Extract the CIK from the query
    pattern = r'cik (\d+)'
    match = re.search(pattern, query_str)
    if match:
        cik = int(match.group(1))
    else:
        return "Please provide a CIK in the query."

    # Handle the query based on the classified type
    if query_type == 'most_occurred':
        investment_name = get_most_occurred_investment_name(filer_df, investment_df, cik)
        return investment_name
    elif query_type == 'highest_individual':
        highest_investment = get_highest_individual_investment(filer_df, investment_df, cik)
        if isinstance(highest_investment, str):
            return highest_investment
        else:
            cik, investment_name, value_usd, percentage_investment = highest_investment
            return f"The highest individual investment for CIK {cik} is '{investment_name}' with a value of {value_usd} USD ({percentage_investment}%)"
    elif query_type == 'total_investments':
        investment_totals = get_total_positive_and_negative_investment(filer_df, investment_df, cik)
        if isinstance(investment_totals, str):
            return investment_totals
        else:
            total_positive_investment = investment_totals['total_positive_investment']
            total_negative_investment = investment_totals['total_negative_investment']
            return f"For CIK {cik}, the total positive investment is {total_positive_investment} USD, and the total negative investment is {total_negative_investment} USD."
    else:
        return "I'm sorry, I couldn't understand your query. Please rephrase your question or provide more context."

answer_basic_query(filer_df, investment_df, "What are the highest investment for cik 1605941 ?")

#@title Complex QnA (50 points) - Let your creativity break free

#@markdown #### Extend the above task, but now it should answer any natural language question.
#@markdown #### Even an approach for the task in text would be good if you are unable to implement the logic.
#@markdown #### Implement the following function:
#@markdown #### <code> answer_general_query(filer_df, investment_df, query) </code>

!pip install -q -U google-generativeai

import pathlib
import re
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from google.colab import userdata

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

GOOGLE_API_KEY = userdata.get('API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat(history=[])

response = chat.send_message(
    "The columns in the investment.xlsx of which i have created an dataframe called investment_df are as follows: ['cik', 'investment_name', 'value_USD', 'percentage_investment']. Your task is to generate Pandas Query for me based on the user given sentences. Only write the pandas query, nothing more"
)

user_message = input("Enter your question: ")
response = chat.send_message(user_message)

pattern = r'```python(.*?)```'
match = re.search(pattern, response.text, re.DOTALL)
if match:
    extracted_code = match.group(1).strip()
    print('Generated Query: ', extracted_code)
    result = eval(extracted_code)
    print(result)
else:
    print("No match found")

# Test Query
top_5_investments = investment_df.groupby('investment_name')['value_USD'].sum().nlargest(5)
print(top_5_investments)