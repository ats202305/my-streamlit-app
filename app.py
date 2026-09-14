
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
    # Max possible distance across RGB space in Euclidean distance
    # so the distance between (0,0,0) and (255,255,255) to normalize the score 
    maxDist = (255 ** 2 + 255 ** 2 + 255 ** 2) ** 0.5
    # Euclidean distance between the target color and the guess one 
    # acting as if it is one dimension in the 3d space 
    dist = (
        (target[0] - guess[0]) ** 2      # squared difference in the red channel
        + (target[1] - guess[1]) ** 2    # squared difference in the green channel
        + (target[2] - guess[2]) ** 2    # squared difference in the blue channel
    ) ** 0.5                             # squared root to get the actual distance 
    # making a similarity percentage - 0 is 100% similar, the maxDistance is 0% similar
    similarity = max(0.0, 100 * (1 - dist / maxDist))
    # returning that percentage rounding to 2 places 
    return round(similarity, 2)
 
 
# streamlit session state persists values across the reruns - happens with every interaction
# if no target color has been set, then pick a new random one and store it 
if "targetColor" not in st.session_state:
    st.session_state.targetColor = randomHexColor()
# Track if the use has submitted a guess 
if "submitted" not in st.session_state:
    st.session_state.submitted = False
# store the most recent similarity score result, if there isn't one, then it just stores none
if "result" not in st.session_state:
    st.session_state.result = None
# tracking the highest score achieved in the run
if "bestScore" not in st.session_state:
    st.session_state.bestScore = None
 
 
def newRound():
    # when "Try a New Color" is hit, it picks a new color
    st.session_state.targetColor = randomHexColor()
    # resetting the submission state so no result is shown for this new round
    st.session_state.submitted = False
    st.session_state.result = None
    # Resetting the sliders back to the middle
    st.session_state.r = 128
    st.session_state.g = 128
    st.session_state.b = 128
 
# rendering the title and the description of what to do 
st.title("Color Match Game")
st.write(
    "Match the hex color below using the RGB sliders. "
    "Get as close as you can, then hit **Submit** to see your score!"
)

# taking the stored target and converting it to a string for the display - * unpacks the tuple into three separate arguments for rbg to hex
targetHex = rgbToHex(*st.session_state.targetColor)
 
# displaying the target color swatch - this will render raw html to draw a colored rectangle
# width: rectangle spans the full width of its container
# height: height of rectangle - fixed
# background color - target color 
# border radius and border - making it have rounded corners and a thin dark border
# margin-bottom - to have some space below the ox 
st.markdown(
    f"""
    <div style="
        width: 100%;        
        height: 150px;
        background-color: {targetHex};
        border-radius: 12px;
        border: 2px solid #333;
        margin-bottom: 10px;
    "></div>
    """,
    unsafe_allow_html = True,      # required for streamlit to render raw HTML instead of escaping
)
# shows the tagret hex code at the bottom of the box 
st.markdown(f"**Target Hex Code:** `{targetHex}`")

# makes a little divider line 
st.divider()

#initializing the sliders in session state if they dont exist 
#will set each red, green, blue sliders to default position 
if "r" not in st.session_state:
    st.session_state.r = 128
if "g" not in st.session_state:
    st.session_state.g = 128
if "b" not in st.session_state:
    st.session_state.b = 128
 
# sliders - each ranges from 0-255 and the key binds it to the st.session_state.r/g/b 
# this means itll update automatically for that sesson state value 
r = st.slider("Red", 0, 255, key = "r")
g = st.slider("Green", 0, 255, key = "g")
b = st.slider("Blue", 0, 255, key = "b")

#converting the sldier values to hex string format
guessHex = rgbToHex(r, g, b)
 
# displaying the guess swatch
# basically the same as the target guess swatch box, just a bit shorter and fills with the guess color
st.markdown(
    f"""
    <div style="
        width: 100%;
        height: 100px;
        background-color: {guessHex};
        border-radius: 12px;
        border: 2px solid #333;
        margin-top: 10px;
        margin-bottom: 10px;
    "></div>
    """,
    unsafe_allow_html = True,
)

# another little divider line 
st.divider()

# splitting the layout into two side-by-side columns
col1, col2 = st.columns(2)

# with the first column:
with col1:
    # renders the submit button - use_container_width makes it fill the column we made 
    if st.button("✅ Submit Guess", use_container_width = True):
        # computes the similarity score from the target and current guess 
        score = calcSimilarity(st.session_state.targetColor, (r, g, b))
        # stores the score for display
        st.session_state.result = score
        # marking the guess has in fact been submitted 
        st.session_state.submitted = True
        # if this new score is none or better than a previous score, then it'll update that with this new score 
        if st.session_state.bestScore is None or score > st.session_state.bestScore:
            st.session_state.bestScore = score

# with the second column: 
with col2:
    # renders the try again button - on_click will run the new round when activated 
    st.button("🔄 Try a New Color", use_container_width = True, on_click = newRound)
 
# Showing the results 
#this will show a different message based off the similarity score you received and will show your final hexcode you got with the message. 
if st.session_state.submitted and st.session_state.result is not None:
    score = st.session_state.result
    if score >= 95:
        st.success(f"🎉 Amazing! You matched {score}% of the color!  (**Your Hex Code:** '{guessHex}')")
    elif score >= 80:
        st.info(f"👍 Nice job! You got {score}% close.  (**Your Hex Code:** '{guessHex}')")
    elif score >= 50:
        st.warning(f"🙂 Not bad — {score}% close. Keep tweaking!  (**Your Hex Code:** '{guessHex}')")
    else:
        st.error(f"😅 {score}% close. Give it another shot! (**Your Hex Code:** '{guessHex}')")

#shows the best score from this session, if any guesses have been made
if st.session_state.bestScore is not None:
    st.caption(f"Best score this session: {st.session_state.bestScore}%")
