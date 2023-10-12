import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io

def add_caption(image, caption, font_size, font_color, position):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    lines = caption.split('\n')
    y_text = position[1]
    for line in lines:
        width, height = draw.textsize(line, font)
        # Draw text
        draw.text(((image.size[0] - width) / 2, y_text), line, font=font, fill=font_color)
        y_text += height
    return image



st.title("Caption Creator")

uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    
    caption = st.text_input("Caption:", "Type here...")
    
    font_size = st.slider("Font Size:", 10, 100, 40)
    font_color = st.color_picker("Pick A Font Color:", "#000000")
    
    position = st.slider("Caption Position (X, Y):", 0, image.size[1], (0, int(image.size[1]*0.9)))
    
    if st.button("Add Caption"):
        image_with_caption = add_caption(image.copy(), caption, font_size, font_color, position)
        st.image(image_with_caption, caption="Image with Caption.", use_column_width=True)
        
        # Prepare image download
        buffered = io.BytesIO()
        image_with_caption.save(buffered, format="JPEG")
        image_bytes = buffered.getvalue()
        
        st.download_button(
            label="Download Image with Caption",
            data=image_bytes,
            file_name="image_with_caption.jpg",
            mime="image/jpeg",
        )
