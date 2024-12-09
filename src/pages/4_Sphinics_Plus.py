import pyspx.shake_128f as sphincs
import streamlit as st
import base64, os

# session state initialization
session_keys = ['sh_pk', 'sh_sk', 'sh_message', 'sh_signature']
for key in session_keys:
    if key not in st.session_state:
        st.session_state[key] = b''

# Streamlit UI
st.title('SPHINCS+')
st.subheader('A Practical stateless hash-based signature')
st.write('\n\n\n')

keygen_tab, sign_tab, verify_tab = st.tabs(["Key generation", "Sign", "Verification"])
seed = os.urandom(sphincs.crypto_sign_SEEDBYTES)

# Key generation
with keygen_tab:
    if st.button("Generate verification & signature keys"):
        st.session_state['sh_pk'], st.session_state['sh_sk'] = sphincs.generate_keypair(seed)
    with st.container(border=True):
        st.text_area(label='Verification (public) key', value=base64.b64encode(st.session_state['sh_pk']).decode('utf-8'))
        st.download_button(label="Download verification key", data=st.session_state['sh_pk'], file_name="verification_key.pub")
    with st.container(border=True):
        st.text_area(label='Signature (private) key', value=base64.b64encode(st.session_state['sh_sk']).decode('utf-8'))
        st.download_button(label="Download signature key", data=st.session_state['sh_sk'], file_name="signature_key")

# Sign
with sign_tab:
    with st.container(border=True):
        st.session_state['sh_message'] = st.text_input("Enter message to sign")
        sign_key_file = st.file_uploader("Choose signature (private) key")
        if st.button("Sign"):
            try:
                st.session_state['sh_signature'] = sphincs.sign(st.session_state['sh_message'].encode("utf-8"), sign_key_file.getvalue())
            except Exception as e:
                st.error(f"Error: {e}")
    with st.container(border=True):
        st.text_area(label="Signature", value=base64.b64encode(st.session_state['sh_signature']).decode("utf-8"))
        st.download_button(label="Download signature", data=st.session_state['sh_signature'], file_name="signature")

# Verification
with verify_tab:
    with st.container(border=True):
        st.session_state['sh_message'] = st.text_input("Enter message to verify", value=st.session_state['sh_message'])
        signature_file = st.file_uploader("Choose signature")
        verify_key_file = st.file_uploader("Choose verification (public) key")
    if st.button("Verify signature"):
        try:
            verification = sphincs.verify(st.session_state['sh_message'].encode("utf-8"), signature_file.getvalue(), verify_key_file.getvalue())

            if verification:
                st.success("Signature is valid")
            else:
                st.error("Signature is invalid")
        except Exception as e:
            st.error(f"Error: {e}")