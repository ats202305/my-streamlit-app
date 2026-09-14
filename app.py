
# importing streamlit and random (so we can build the random RGB values
import streamlit as st
import random

# configuring the browser tab and page, so the title, icon, and the layout 
st.set_page_config(page_title = "Color Match Game", page_icon = "🎨", layout = "centered")
 
# making the random hexadecimal colors - randomizing a random red, green, and blue vlaue from 0-255 and returning the values as a tuple
def randomHexColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)
 
#formatting each value into a 2-digit uppercase hexadecimal number and putting them together as the typical RBG string
def rgbToHex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"
 
 
def calcSimilarity(target, guess):
    # Max possible distance across RGB space
    maxDist = (255 ** 2 + 255 ** 2 + 255 ** 2) ** 0.5
    dist = (
        (target[0] - guess[0]) ** 2
        + (target[1] - guess[1]) ** 2
        + (target[2] - guess[2]) ** 2
    ) ** 0.5
    similarity = max(0.0, 100 * (1 - dist / maxDist))
    return round(similarity, 2)
 
 
# --- Initialize session state ---
if "targetColor" not in st.session_state:
    st.session_state.targetColor = randomHexColor()
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "result" not in st.session_state:
    st.session_state.result = None
if "bestScore" not in st.session_state:
    st.session_state.bestScore = None
 
 
def new_round():
    st.session_state.targetColor = randomHexColor()
    st.session_state.submitted = False
    st.session_state.result = None
    st.session_state.r = 128
    st.session_state.g = 128
    st.session_state.b = 128
 
 
st.title("Color Match Game")
st.write(
    "Match the hex color below using the RGB sliders. "
    "Get as close as you can, then hit **Submit** to see your score!"
)
 
target_hex = rgbToHex(*st.session_state.targetColor)
 
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
 
guess_hex = rgbToHex(r, g, b)
 
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
        score = calcSimilarity(st.session_state.targetColor, (r, g, b))
        st.session_state.result = score
        st.session_state.submitted = True
        if st.session_state.bestScore is None or score > st.session_state.bestScore:
            st.session_state.bestScore = score
 
with col2:
    st.button("🔄 Try a New Color", use_container_width=True, on_click=new_round)
 
# --- Show result ---
if st.session_state.submitted and st.session_state.result is not None:
    score = st.session_state.result
    if score >= 95:
        st.success(f"🎉 Amazing! You matched {score}% of the color!  (**Your Hex Code:** '{guess_hex}')")
    elif score >= 80:
        st.info(f"👍 Nice job! You got {score}% close.  (**Your Hex Code:** '{guess_hex}')")
    elif score >= 50:
        st.warning(f"🙂 Not bad — {score}% close. Keep tweaking!  (**Your Hex Code:** '{guess_hex}')")
    else:
        st.error(f"😅 {score}% close. Give it another shot! (**Your Hex Code:** '{guess_hex}')")
 
if st.session_state.bestScore is not None:
    st.caption(f"Best score this session: {st.session_state.bestScore}%")
