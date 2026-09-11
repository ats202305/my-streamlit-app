import streamlit as st
import random
 
st.set_page_config(page_title="Color Match Game", page_icon="🎨", layout="centered")
 
 
def random_hex_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)
 
 
def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"
 
 
def calc_similarity(target, guess):
    # Max possible distance across RGB space
    max_dist = (255 ** 2 + 255 ** 2 + 255 ** 2) ** 0.5
    dist = (
        (target[0] - guess[0]) ** 2
        + (target[1] - guess[1]) ** 2
        + (target[2] - guess[2]) ** 2
    ) ** 0.5
    similarity = max(0.0, 100 * (1 - dist / max_dist))
    return round(similarity, 2)
 
 
# --- Initialize session state ---
if "target_color" not in st.session_state:
    st.session_state.target_color = random_hex_color()
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "result" not in st.session_state:
    st.session_state.result = None
if "best_score" not in st.session_state:
    st.session_state.best_score = None
 
 
def new_round():
    st.session_state.target_color = random_hex_color()
    st.session_state.submitted = False
    st.session_state.result = None
    st.session_state.r = 128
    st.session_state.g = 128
    st.session_state.b = 128
 
 
st.title("🎨 Color Match Game")
st.write(
    "Match the hex color below using the RGB sliders. "
    "Get as close as you can, then hit **Submit** to see your score!"
)
 
target_hex = rgb_to_hex(*st.session_state.target_color)
 
# --- Display target color swatch ---
st.markdown(
    f"""
    <div style="
        width: 100%;
        height: 150px;
        background-color: {target_hex};
        border-radius: 12px;
        border: 2px solid #333;
        margin-bottom: 10px;
    "></div>
    """,
    unsafe_allow_html=True,
)
st.markdown(f"**Target Hex Code:** `{target_hex}`")
 
st.divider()
 
if "r" not in st.session_state:
    st.session_state.r = 128
if "g" not in st.session_state:
    st.session_state.g = 128
if "b" not in st.session_state:
    st.session_state.b = 128
 
# --- Sliders ---
r = st.slider("Red", 0, 255, key="r")
g = st.slider("Green", 0, 255, key="g")
b = st.slider("Blue", 0, 255, key="b")
 
guess_hex = rgb_to_hex(r, g, b)
 
# --- Display guess swatch ---
st.markdown(
    f"""
    <div style="
        width: 100%;
        height: 100px;
        background-color: {guess_hex};
        border-radius: 12px;
        border: 2px solid #333;
        margin-top: 10px;
        margin-bottom: 10px;
    "></div>
    """,
    unsafe_allow_html=True,
)
 
st.divider()
 
col1, col2 = st.columns(2)
 
with col1:
    if st.button("✅ Submit Guess", use_container_width=True):
        score = calc_similarity(st.session_state.target_color, (r, g, b))
        st.session_state.result = score
        st.session_state.submitted = True
        if st.session_state.best_score is None or score > st.session_state.best_score:
            st.session_state.best_score = score
 
with col2:
    st.button("🔄 Try a New Color", use_container_width=True, on_click=new_round)
 
# --- Show result ---
if st.session_state.submitted and st.session_state.result is not None:
    score = st.session_state.result
    if score >= 95:
        st.success(f"🎉 Amazing! You matched {score}% of the color!")
    elif score >= 80:
        st.info(f"👍 Nice job! You got {score}% close.")
    elif score >= 50:
        st.warning(f"🙂 Not bad — {score}% close. Keep tweaking!")
    else:
        st.error(f"😅 {score}% close. Give it another shot!")
 
if st.session_state.best_score is not None:
    st.caption(f"Best score this session: {st.session_state.best_score}%")
