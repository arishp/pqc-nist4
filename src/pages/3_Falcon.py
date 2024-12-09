from pqc.sign import dilithium5
from pqc.sign import falcon_512
import streamlit as st
import base64

# session state initialization
session_keys = ['fa_pk', 'fa_sk', 'fa_message', 'fa_signature']
for key in session_keys:
    if key not in st.session_state:
        st.session_state[key] = b''

# Streamlit UI
st.title('FALCON')
st.subheader('Fast-Fourier Lattice-based Compact Signatures over NTRU')
st.write('\n\n\n')

keygen_tab, sign_tab, verify_tab = st.tabs(["Key generation", "Sign", "Verification"])

# Key generation
with keygen_tab:
    if st.button("Generate verification & signature keys"):
        st.session_state['fa_pk'], st.session_state['fa_sk'] = falcon_512.keypair()
    with st.container(border=True):
        st.text_area(label='Verification (public) key', value=base64.b64encode(st.session_state['fa_pk']).decode('utf-8'))
        st.download_button(label="Download verification key", data=st.session_state['fa_pk'], file_name="verification_key.pub")
    with st.container(border=True):
        st.text_area(label='Signature (private) key', value=base64.b64encode(st.session_state['fa_sk']).decode('utf-8'))
        st.download_button(label="Download signature key", data=st.session_state['fa_sk'], file_name="signature_key")

# Sign
with sign_tab:
    with st.container(border=True):
        st.session_state['fa_message'] = st.text_input("Enter message to sign")
        sign_key_file = st.file_uploader("Choose signature (private) key")
        if st.button("Sign"):
            try:
                st.session_state['fa_signature'] = falcon_512.sign(sk=sign_key_file.getvalue(),
                                                                  m=st.session_state['fa_message'].encode("utf-8"))
            except Exception as e:
                st.error(f"Error: {e}")
    with st.container(border=True):
        st.text_area(label="Signature", value=base64.b64encode(st.session_state['fa_signature']).decode("utf-8"))
        st.download_button(label="Download signature", data=st.session_state['fa_signature'], file_name="signature")

# Verification
with verify_tab:
    with st.container(border=True):
        st.session_state['fa_message'] = st.text_input("Enter message to verify", value=st.session_state['fa_message'])
        signature_file = st.file_uploader("Choose signature")
        verify_key_file = st.file_uploader("Choose verification (public) key")
    if st.button("Verify signature"):
        try:
            verification = falcon_512.verify(pk=verify_key_file.getvalue(), 
                                            m=st.session_state['fa_message'].encode("utf-8"), 
                                            sig=signature_file.getvalue())
            if verification is None:
                st.success("Signature is valid")
        # pqc library returns None if is valid or raises ValueError if invalid
        except ValueError as ve:
            st.error("Signature is invalid")
        except Exception as e:
            st.error(f"Error: {e}")