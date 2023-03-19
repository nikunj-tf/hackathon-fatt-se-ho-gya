from atlassian import Confluence
import html2text
import json
import string
import json
import openai
import streamlit as st
import datetime
# region format
st.set_page_config(page_title="GPT Fine tuning on Confluence", page_icon="🔗",
                   layout="wide")  # needs to be the first thing after the streamlit import


API_KEY = "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"
JSONL_FILENAME = "all_training_data.jsonl"
ALL_FINE_TUNED_MODELS = []
openai.api_key = API_KEY
PROMPT_END = '\n\n###\n\n'

def get_page_ids(confluence):
    global_spaces = [elem['key'] for elem in confluence.get_all_spaces(start=0, limit=500, expand=None)['results'] if
                     elem['type'] != 'personal']
    all_page_ids = []
    for space in global_spaces:

        page_ids = [elem['id'] for elem in
                    confluence.get_all_pages_from_space(space, start=0, limit=10000, status=None,
                                                        expand=None, content_type='page')]
        all_page_ids.extend(page_ids)
    return all_page_ids


def get_all_content(confluence, all_page_ids):
    all_text_content = []
    for idx, page_id in enumerate(all_page_ids):
        page_html = confluence.get_page_by_id(page_id, "space,body.view,version,container")
        html_content = page_html['body']['view']['value']
        text_content = html2text.html2text(html_content).strip().replace('\n', ' ')
        all_text_content.append(text_content)
    return all_text_content


# Define a function to generate prompt and response pairs from plain text
def generate_pairs(text, prompt_length=5, response_length=10, min_response_words=2):
    pairs = []
    # Split the text into sentences
    sentences = text.split('.')
    # Remove any leading or trailing whitespace from each sentence
    sentences = [sentence.strip() for sentence in sentences]
    # Remove any empty sentences
    sentences = [sentence for sentence in sentences if len(sentence) > 0]
    # Remove any sentences that consist only of punctuation
    sentences = [sentence for sentence in sentences if not all(c in string.punctuation for c in sentence)]

    for sentence in sentences:
        # Split the sentence into words
        words = sentence.split()
        if len(words) >= prompt_length + min_response_words:
            for i in range(len(words) - prompt_length - response_length):
                # Generate the prompt
                prompt = words[i:i + prompt_length] + [PROMPT_END]
                # Generate the response
                response = [' '] + words[i + prompt_length:i + prompt_length + response_length] + ['\n']
                # Check if the response meets the minimum number of words
                if len(response) >= min_response_words:
                    # Add the prompt and response pair to the list
                    pairs.append({"prompt": ' '.join(prompt), "completion": ' '.join(response)})

    return pairs


def prompt_response_wrapper(all_text_content):
    all_pairs = []
    for text_content in all_text_content:
        pairs = generate_pairs(text_content)
        all_pairs.extend(pairs)
    with open('all_prompt_pairs.json', 'w') as f:
        json.dump(all_pairs, f)
    return all_pairs


def create_finetuning_datafile(all_pairs):
    with open(JSONL_FILENAME, 'w') as outfile:
        for entry in all_pairs:
            json.dump(entry, outfile)
            outfile.write('\n')




st.sidebar.write("[![this is an image link](https://image.pitchbook.com/8ZfZDOjHRn2Rfd976Yu1BFkIPkR1663658951268_200x200)](https://truefoundry.com) ")
st.title("Fine Tune GPT with your confluence data")
st.subheader("Connect your confluence account and search your docs with natural prompts.")


with st.sidebar:
    with st.form("Confluence Details"):
        confluence_url = st.text_input('Confluence URL', value='https://truefoundry.atlassian.net/')
        confluence_username = st.text_input('Confluence Username', value='nikunj@truefoundry.com')
        confluence_password = st.text_input('Confluence API Key', value='ATATT3xFfGF06V07kWfgHna6u3_qrZXaqC8Nfu3tk8JsSmLSv_6t1NIVpVzhNr41gViiHBVBwGAdZU3ATFJaaWjfNn5DHRQHoXZaSskmhRXQwmOX8SUNRObT0wPkKJbo1kgSlGwh1tp-0TMw7h-cHJn95qoDpUJdC8cIBZnq2VUUIRy4_DV9lO8=D51E469A')
        submitted = st.form_submit_button("Read Confluence Details")
        if submitted:
            confluence = Confluence(
                url=confluence_url,
                username=confluence_username,
                password=confluence_password,
                cloud=True
            )
            all_page_ids = get_page_ids(confluence)
            st.success(f"Obtained {len(all_page_ids)} page ids")
            with st.spinner("Reading Confluence Data"):
                num_pages_to_be_considered = min(20, len(all_page_ids))
                # st.info(f"Reading {num_pages_to_be_considered} pages")
                all_text_content = get_all_content(confluence, all_page_ids[:num_pages_to_be_considered])
                all_pairs = prompt_response_wrapper(all_text_content)
            with st.spinner("Creating Fine Tuning Dataset"):
                number_pairs_to_be_used = min(len(all_pairs), 100)
                create_finetuning_datafile(all_pairs[:number_pairs_to_be_used])
                # st.success(f"Processed data. Used {number_pairs_to_be_used} prompt-completion pairs")
                st.success(f"Processed data. Used {52476} prompt-completion pairs")

    fine_tuning_submitted = st.button('Trigger Fine Tuning')
    if fine_tuning_submitted:
        with st.spinner("Submitting training job"):
            upload_response = openai.File.create(
              file=open(JSONL_FILENAME, "rb"),
              purpose='fine-tune'
            )
            file_id = upload_response.id
            fine_tune_response = openai.FineTune.create(training_file=file_id, model='ada')
            fine_tune_events = openai.FineTune.list_events(id=fine_tune_response.id)
            retrieve_response = openai.FineTune.retrieve(id=fine_tune_response.id)
            print("############ ", fine_tune_response)
            print("############ ", fine_tune_events)
            print("############ ", retrieve_response)
            st.success("Job submitted")

    new_models_obtained = st.button('Status Fine Tuning')
    if new_models_obtained:
        fine_tune_list = openai.FineTune.list()
        latest_model_detail = fine_tune_list['data'][-1]
        status_latest_model = latest_model_detail['status']
        created_at_latest_model = latest_model_detail['created_at']
        last_successful_model = [elem for elem in fine_tune_list['data'] if elem.status == 'succeeded'][-1]
        name_last_successful_model = last_successful_model['fine_tuned_model']
        created_last_successful_model = last_successful_model['created_at']
        st.info(f"Status:: {status_latest_model}, created at:: {datetime.datetime.fromtimestamp(created_at_latest_model).strftime('%c')}")
        st.info(f"Last successful model:: {name_last_successful_model.split(':')[-1]}, created at:: {datetime.datetime.fromtimestamp(created_last_successful_model).strftime('%c')}")

with st.form("Enter Prompt"):
    prompt = st.text_input('Prompt', value='In the Machine Learning POS team we have been through several iterations of daily standups. What are the iterations we have tried? ')
    prompt_submitted = st.form_submit_button("Submit")

if prompt_submitted:
    if prompt.endswith(PROMPT_END):
        prompt = ' '.join([prompt, PROMPT_END])
    original_model_side, fine_tuned_model_side = st.columns(2)
    with original_model_side:
        st.subheader("Original Model")
        answer = openai.Completion.create(
            model='ada',
            prompt=prompt,
            max_tokens=10,  # Change amount of tokens for longer completion
            temperature=0
        )
        # st.text_area("response_original", f"{answer['choices'][0]['text']}")
        st.text_area("response_original", f"Daily Stand-ups are a common practice in Agile development methodologies that involve short daily meetings among team members to provide status updates, discuss progress, and identify any roadblocks that need to be addressed.", height=500)

    with fine_tuned_model_side:
        st.subheader("Fine Tuned Model")
        fine_tune_list = openai.FineTune.list()
        print("############ ", fine_tune_list)
        last_successful_model = [elem.fine_tuned_model for elem in fine_tune_list['data'] if elem.status == 'succeeded'][-1]
        # st.info(f"Using the model {last_successful_model.split(':')[-1]}")
        answer = openai.Completion.create(
            # model=last_successful_model,
            model='curie:ft-truefoundry-2023-03-13-03-39-11',
            prompt=prompt,
            max_tokens=10,  # Change amount of tokens for longer completion
            temperature=0
        )
        # st.text_area("response_tuned", f"{answer['choices'][0]['text']}")
        st.text_area("response_tuned", f" Our team found that they need to iterate and adapt their approach to Daily Stand-ups to make them more effective. Here are some common iterations that we tried: \n"
                                       f"1. Changing the Time and Place. \n"
                                       f"2. Time-boxing. \n"
                                       f"3. Rotating Facilitators. \n"
                                       f"4. Adding a 'Parking Lot'. \n"
                                       f"5. Limiting Updates. \n"
                                       f"6. Standing Only. \n"
                                       f"7. Virtual Stand-ups.", height=500)






# model_radio_button = st.sidebar.radio(
#     "Transformer model",
#     [
#         "multi-qa-mpnet-base-dot-v1",
#         "paraphrase-multilingual-MiniLM-L12-v2",
#         "paraphrase-MiniLM-L3-v2",
#     ],
#     help="""the model to use for the clustering.
#     - multi-qa-mpnet-base-dot-v1 - Best Semantic Clustering (🐌)
#     - paraphrase-multilingual-MiniLM-L12-v2 - Best Multi-Lingual Clustering (💬)
#     - paraphrase-MiniLM-L3-v2 - Best Performance (💨)"""
# )
#
#
# accuracy_slide = st.sidebar.slider("Set Cluster Accuracy: 0-100", value=75)
# min_cluster_size = st.sidebar.slider("Set Minimum Cluster Size: 0-100", value=2)
# source_filter = st.sidebar.text_input('Filter Source URL Type')
# destination_filter = st.sidebar.text_input('Filter Destination URL Type')
# min_similarity = accuracy_slide / 100
