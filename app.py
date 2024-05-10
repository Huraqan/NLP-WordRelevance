import streamlit as st
import requests
from pandas import DataFrame

default_text = "The Minkowski distance or Minkowski metric is a metric in a normed vector space which can be considered as a generalization of both the Euclidean distance and the Manhattan distance. It is named after the Polish mathematician Hermann Minkowski."

def request_api(all_inputs):
    with st.spinner('In progress...'):
        try:
            r = requests.post('http://127.0.0.1:8000/process_text/', json=all_inputs)
            if r.status_code == 200:
                response_data = r.json()
                
                st.dataframe(DataFrame(response_data)[['labels', 'scores']])
            else:
                st.error(f"Status code: {r.status_code}")
                st.error(f"Error: {r.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")


st.title("How relevant?")

text_input = st.text_area("Enter Text Here:", height=100, value=default_text)

words = []
word_inputs = st.number_input("Number of single-word fields:", min_value=1, max_value=10, value=1)

for i in range(word_inputs):
    word = st.text_input(f"Word {i+1}:")
    words.append(word)

if st.button("Find relevance"):
    all_inputs = {
        "text": text_input,
        "words": words
    }
    
    if text_input and len(words) > 0 and len(words[0]) > 0:
        request_api(all_inputs)
    else:
        st.warning("Please enter some text.")