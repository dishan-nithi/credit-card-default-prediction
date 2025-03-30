import pickle
from pathlib import Path
import streamlit_authenticator as stauth

names = ['Dishan N']
usernams = ['Dishan']
Passwords = ['zxc123']

hashed_passwords = stauth.Hasher(Passwords).generate()

file_path = Path(__file__).parent / "hashed_pwd.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)