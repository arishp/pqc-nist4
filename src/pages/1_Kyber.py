import streamlit as st
import base64
from kyber_py.ml_kem import ML_KEM_512

# session state initialization
session_keys = ['ky_ek', 'ky_dk', 'ky_K', 'ky_c', 'ky_K2']
for key in session_keys:
    if key not in st.session_state:
        st.session_state[key] = b''

@st.dialog("CRYSTALS Kyber Demo")
def decaps_button():
    if st.session_state['ky_K2'] == st.session_state['ky_K']:
        st.success('SECRET KEYS MATCH!!!')
    else:
        st.write('SECRET KEYS MISMATCH...')

# Streamlit UI

st.title('CRYSTALS-Kyber')
st.subheader('A Module Lattice-based Key Encapsulation Mechanism')
st.write('\n\n\n')

keygen_tab, encaps_tab, decaps_tab = st.tabs(["Key generation", "Encapsulation", "Decapsulation"])

with keygen_tab:
    # st.subheader('Alice generates encapsulation key (public key) and decapsulation key (private key).')
    if st.button('Generate encaps & decaps keys'):
        st.session_state['ky_ek'], st.session_state['ky_dk'] = ML_KEM_512.keygen()
    with st.container(border=True):
        st.text_area(label='Encapsulation (public) key', value=base64.b64encode(st.session_state['ky_ek']).decode('utf-8'))
        st.download_button(label="Download encapsulation key", data=st.session_state['ky_ek'], file_name="encaps.pub")
    with st.container(border=True):
        st.text_area(label='Decapsulation (private) key', value=base64.b64encode(st.session_state['ky_dk']).decode('utf-8'))
        st.download_button(label="Download decapsulation key", data=st.session_state['ky_dk'], file_name="decaps")

with encaps_tab:
    # st.subheader('Bob uses Alice\'s encapsulation key to generate a secret key K and ciphertext c, and sends c to Alice.')
    with st.container(border=True):
        encaps_file = st.file_uploader("Choose encapsulation (public) key")
        if st.button('Generate secret key & ciphertext'):
            try:
                st.session_state['ky_K'], st.session_state['ky_c'] = ML_KEM_512.encaps(encaps_file.getvalue())
            except Exception as e:
                st.error(f"Error: {e}")
    with st.container(border=True):
        st.text_area(label='Secret key', value=base64.b64encode(st.session_state['ky_K']).decode('utf-8'))
        st.download_button(label="Download secret key", data=st.session_state['ky_K'], file_name="secret")
    with st.container(border=True):
        st.text_area(label='Cipher text', value=base64.b64encode(st.session_state['ky_c']).decode('utf-8'))
        st.download_button(label="Download cipher text", data=st.session_state['ky_c'], file_name="cipher")

with decaps_tab:
    # st.subheader('Alice uses her decapsulation key to recover K from the ciphertext c.')
    with st.container(border=True):
        cipher_file = st.file_uploader("Choose cipher text")
        decaps_file = st.file_uploader("Choose decapsulation (private) key")
        if st.button('Generate secret key'):
            try:
                st.session_state['ky_K2'] = ML_KEM_512.decaps(decaps_file.getvalue(), cipher_file.getvalue())
                decaps_button()
            except Exception as e:
                st.error(f"Error: {e}")
    with st.container(border=True):
        st.text_area(label='Secret key received', value=base64.b64encode(st.session_state['ky_K2']).decode('utf-8'))