from dilithium_py.ml_dsa import ML_DSA_44
import streamlit as st
import base64

# session state initialization
session_keys = ['di_pk', 'di_sk', 'di_message', 'di_signature']
for key in session_keys:
    if key not in st.session_state:
        st.session_state[key] = b''

# Streamlit UI

st.title('CRYSTALS-Dilithium')
st.subheader('A Module Lattice-Based Digital Signature Standard')
st.write('\n\n\n')

keygen_tab, sign_tab, verify_tab = st.tabs(["Key generation", "Sign", "Verification"])

algorithm = ML_DSA_44

# Key generation
with keygen_tab:
    if st.button("Generate verification & signature keys"):
        st.session_state['di_pk'], st.session_state['di_sk'] = ML_DSA_44.keygen()
    with st.container(border=True):
        st.text_area(label='Verification (public) key', value=base64.b64encode(st.session_state['di_pk']).decode('utf-8'))
        st.download_button(label="Download verification key", data=st.session_state['di_pk'], file_name="verification_key.pub")
    with st.container(border=True):
        st.text_area(label='Signature (private) key', value=base64.b64encode(st.session_state['di_sk']).decode('utf-8'))
        st.download_button(label="Download signature key", data=st.session_state['di_sk'], file_name="signature_key")

# Sign
with sign_tab:
    with st.container(border=True):
        st.session_state['di_message'] = st.text_input("Enter message to sign")
        sign_key_file = st.file_uploader("Choose signature (private) key")
        if st.button("Sign"):
            try:
                st.session_state['di_signature'] = ML_DSA_44.sign(sk_bytes=sign_key_file.getvalue(),
                                                                  m=st.session_state['di_message'].encode("utf-8"))
            except Exception as e:
                st.error(f"Error: {e}")
    with st.container(border=True):
        st.text_area(label="Signature", value=base64.b64encode(st.session_state['di_signature']).decode("utf-8"))
        st.download_button(label="Download signature", data=st.session_state['di_signature'], file_name="signature")

# Verification
with verify_tab:
    with st.container(border=True):
        st.session_state['di_message'] = st.text_input("Enter message to verify", value=st.session_state['di_message'])
        signature_file = st.file_uploader("Choose signature")
        verify_key_file = st.file_uploader("Choose verification (public) key")
    if st.button("Verify signature"):
        try:
            verification = algorithm.verify(pk_bytes=verify_key_file.getvalue(), 
                                            m=st.session_state['di_message'].encode("utf-8"), 
                                            sig_bytes=signature_file.getvalue())
            if verification:
                st.success("Signature is valid")
            else:
                st.error("Signature is invalid")
        except Exception as e:
            st.error(f"Error: {e}")
