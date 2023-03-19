import openai
import streamlit as st
# region format
st.set_page_config(page_title="GPT Fine tuning on Sales Notes Data.", page_icon="🔗",
                   layout="wide")  # needs to be the first thing after the streamlit import

st.title("Note Navigation App- Sath Me Smart")

API_KEY = "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"
openai.api_key = API_KEY
PROMPT_END = ' \n\n###\n\n'

with st.form("Enter Prompt"):
    prompt = st.text_input('Prompt', value='How are the code and dependencies across multiple cloud providers managed and abstracted?')
    prompt_submitted = st.form_submit_button("Submit")

if prompt_submitted:
    if not prompt.endswith(PROMPT_END):
        prompt = ' '.join([prompt, PROMPT_END])

    st.subheader('Ada Model')
    original_model_side, fine_tuned_model_side = st.columns(2)
    with original_model_side:
        st.caption("Original Model")
        answer = openai.Completion.create(
            model='ada',
            prompt=prompt,
            temperature=0.5,
        )
        st.text_area("response_original-ada", f"{answer['choices'][0]['text']}", height=500)
        # st.text_area("response_original", f"Daily Stand-ups are a common practice in Agile development methodologies that involve short daily meetings among team members to provide status updates, discuss progress, and identify any roadblocks that need to be addressed.", height=500)

    with fine_tuned_model_side:
        st.caption("Fine Tuned Model")
        # st.info(f"Using the model {last_successful_model.split(':')[-1]}")
        answer = openai.Completion.create(
            # model=last_successful_model,
            model='ada:ft-truefoundry-2023-03-17-21-22-33',
            prompt=prompt,
            temperature=0.5,
            max_tokens=100
        )
        st.text_area("response_tuned-ada", f"{answer['choices'][0]['text']}", height=500)

    st.subheader('Curie Model')
    original_model_side, fine_tuned_model_side = st.columns(2)
    with original_model_side:
        st.caption("Original Model")
        answer = openai.Completion.create(
            model='curie',
            prompt=prompt,
            temperature=0.5,

        )
        st.text_area("response_original-curie", f"{answer['choices'][0]['text']}", height=500)
        # st.text_area("response_original", f"Daily Stand-ups are a common practice in Agile development methodologies that involve short daily meetings among team members to provide status updates, discuss progress, and identify any roadblocks that need to be addressed.", height=500)

    with fine_tuned_model_side:
        st.caption("Fine Tuned Model")
        answer = openai.Completion.create(
            # model=last_successful_model,
            model='curie:ft-truefoundry-2023-03-18-08-33-03',
            prompt=prompt,
            temperature=0.5,
            max_tokens=100
        )
        st.text_area("response_tuned-curie", f"{answer['choices'][0]['text']}", height=500)

    st.subheader('Davinci Model')
    original_model_side, fine_tuned_model_side = st.columns(2)
    with original_model_side:
        st.caption("Original Model")
        answer = openai.Completion.create(
            model='davinci',
            prompt=prompt,
            temperature=0.5
        )
        st.text_area("response_original-davinci", f"{answer['choices'][0]['text']}", height=500)
        # st.text_area("response_original", f"Daily Stand-ups are a common practice in Agile development methodologies that involve short daily meetings among team members to provide status updates, discuss progress, and identify any roadblocks that need to be addressed.", height=500)

    with fine_tuned_model_side:
        st.caption("Fine Tuned Model")
        answer = openai.Completion.create(
            # model=last_successful_model,
            model='davinci:ft-truefoundry-2023-03-18-09-30-45',
            prompt=prompt,
            temperature=0.5,
            max_tokens=100

        )
        st.text_area("response_tuned-davinci", f"{answer['choices'][0]['text']}", height=500)













        # st.text_area("response_tuned", f" Our team found that they need to iterate and adapt their approach to Daily Stand-ups to make them more effective. Here are some common iterations that we tried: \n"
        #                                f"1. Changing the Time and Place. \n"
        #                                f"2. Time-boxing. \n"
        #                                f"3. Rotating Facilitators. \n"
        #                                f"4. Adding a 'Parking Lot'. \n"
        #                                f"5. Limiting Updates. \n"
        #                                f"6. Standing Only. \n"
        #                                f"7. Virtual Stand-ups.", height=500)



