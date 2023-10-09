""" stauth - Authenticator for Streamlit using pydal to save user info in database.
"""
import streamlit as st
from .stauth import STAuth
__AUTHOR = "Eduardo S. Pereira"
__EMAIL = "eduardo.spereira@sp.senai.br"
__DATE = "09/10/2023"

__version__ = "0.1.0"


class STAuthView:
    def __init__(self, dbinfo, folder):
        self._stauth = STAuth(dbinfo, folder)

        self._login_section = st.container()
        self._logout_section = st.container()

        self._session_state = st.session_state
        self._start()

    def _start(self):
        if 'loggedIn' not in self._session_state:
            self._session_state['loggedIn'] = False

        if 'sigin' not in self._session_state:
            self._session_state['sigin'] = False

    def login_button(self, username, password):
        if self._stauth.login(username, password):
            st.empty()
            self._session_state['loggedIn'] = True
        else:
            st.error("Wrong User or Password")

    def logout_button(self):
        st.empty()
        self._session_state['sigin'] = False
        self._session_state['loggedIn'] = False
        st.rerun

    def sigin_button(self):
        if self._session_state['loggedIn'] is False:
            self._session_state['sigin'] = True

    def create_user(self, username, email, password, rpassword):
        if password != rpassword:
            st.error("Password is not equals!")
        elif len(password) < 8:
            st.error("Password must have at least 8 characters!")
        else:
            pass

        new_user = self._stauth.create_user(username, password, email)

        if new_user["error"] is None:
            self._session_state['sigin'] = False
            self._session_state['loggedIn'] = True

        else:
            st.error(new_user["error"])

    def sigin_page(self):

        if self._session_state['sigin'] is True:

            with st.form("login-form"):
                username = st.text_input(
                    label="Name", value="", placeholder="Enter your user name")

                email = st.text_input(
                    label="e-mail", value="", placeholder="Enter your e-mail")

                password = st.text_input(
                    label="Password", value="", placeholder="Enter password", type="password")

                rpassword = st.text_input(
                    label="Password", value="", placeholder="Repit the password", type="password")

                st.form_submit_button("Create",
                                      on_click=self.create_user,
                                      args=(username, email,
                                            password, rpassword)
                                      )

    def login_page(self):

        with self._login_section:
            if self._session_state['loggedIn'] is False and self._session_state['sigin'] is False:

                #with st.form("login-form"):
                username = st.text_input(
                    label="Name", value="", placeholder="Enter your user name")
                password = st.text_input(
                    label="Password", value="", placeholder="Enter password", type="password")

                cols = st.columns(5)

                with cols[2]:
                    st.button("Login",
                                            on_click=self.login_button,
                                            args=(username, password)
                                            )

                    st.button("Sigin",
                                            on_click=self.sigin_button
                                            )

            elif self._session_state['sigin'] is True:
                self.sigin_page()

    def logout_page(self):

        with self._logout_section:
            cols = st.columns(5)

            with cols[4]:
                st.button("Logout",
                          on_click=self.logout_button
                          )
                

    @property
    def database(self):
        return self._stauth.database

    @property
    def session_state(self):
        return self._session_state

    @property
    def login_section(self):
        return self._login_section

    @property
    def logout_section(self):
        return self._logout_section
