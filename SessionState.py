import streamlit as st

# Example function that loads some initial data and is cached
@st.cache_data
def load_initial_data():
    # Simulate loading or processing some data
    return {'user_name': '', 'favorite_color': 'black'}

class SessionState(object):
    def __init__(self, **kwargs):
        """A new SessionState object.
        Parameters
        ----------
        **kwargs : any
            Default values for the session state.
        """
        # Load initial data (example function with caching)
        initial_data = load_initial_data()
        for key, val in initial_data.items():
            if key not in st.session_state:
                st.session_state[key] = val

        for key, val in kwargs.items():
            if key not in st.session_state:
                st.session_state[key] = val

    def __setattr__(self, key, value):
        st.session_state[key] = value

    def __getattr__(self, key):
        if key in st.session_state:
            return st.session_state[key]
        raise AttributeError(f"'{key}' not found in session state")

def get(**kwargs):
    """Gets a SessionState object for the current session.
    Creates a new object if necessary.
    Parameters
    ----------
    **kwargs : any
        Default values you want to add to the session state, if we're creating a
        new one.
    """
    for key, default_value in kwargs.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

    return SessionState()
'''
# Example Usage
session_state = get(user_name='', favorite_color='black')
if st.button("Set user_name to 'Mary'"):
    session_state.user_name = 'Mary'
st.write("User Name:", session_state.user_name)
st.write("Favorite Color:", session_state.favorite_color)
'''
