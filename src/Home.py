import streamlit as st

st.title('Post Quantum Cryptography')

st.subheader('NIST algorithms demo')

st.write("The U.S. Department of Commerce's National Institute of Standards and Technology (NIST) has chosen \
         the first group of encryption tools that are designed to withstand the assault of a future quantum computer, \
         which could potentially crack the security used to protect privacy in the digital systems we rely on every day — \
         such as online banking and email software. The four selected encryption algorithms will become part of NIST’s \
         post-quantum cryptographic standard. These algorithms are based on structured lattices and hash functions, two \
         families of math problems that could resist a quantum computer's assault.")

st.image('./images/NIST4_chart.png')

