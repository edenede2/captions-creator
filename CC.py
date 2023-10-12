from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
import streamlit as st

def add_caption(image, captions):
    for caption in captions:
        draw = ImageDraw.Draw(image)
        font_path, font_size, font_color, position = caption['font'], caption['size'], caption['color'], caption['position']
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            font = ImageFont.load_default()

        lines = caption['text'].split('\n')
        x, y = position
        for line in lines:
            width, height = font.getsize(line)
            draw.text((x, y), line, font=font, fill=font_color)
            y += height
    return image

st.title("Caption Creator")

uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

    num_captions = st.slider("Number of captions:", 1, 5, 1)

    captions = []
    for i in range(num_captions):
        st.subheader(f"Caption {i+1}")
        caption_text = st.text_area(f"Caption {i+1} Text:", "Type here...")
        font_choice = st.selectbox(
            f"Caption {i+1} Font:",
            [
                "PermanentMarker-Regular.ttf",
                "ArchitectsDaughter-Regular.ttf",
                "Lumanosimo-Regular.ttf"
            ]
        )
        font_size = st.slider(f"Caption {i+1} Font Size:", 10, 100, 40)
        font_color = st.color_picker(f"Caption {i+1} Font Color:", "#000000")
        alpha = st.slider(f"Caption {i+1} Transparency:", 0, 255, 255)
        font_color += hex(alpha)[2:]  # Add alpha (transparency) to color
        x = st.slider(f"Caption {i+1} X Position:", 0, image.size[0], 0)
        y = st.slider(f"Caption {i+1} Y Position:", 0, image.size[1], 0)

        captions.append({
            'text': caption_text,
            'font': font_choice,
            'size': font_size,
            'color': font_color,
            'position': (x, y)
        })

    if st.button("Add Captions"):
        image_with_captions = add_caption(image.copy(), captions)
        st.image(image_with_captions, caption="Image with Captions.", use_column_width=True)

        # Prepare image download
        buffered = io.BytesIO()
        image_with_captions.save(buffered, format="PNG")  # Save as PNG to keep transparency
        image_bytes = buffered.getvalue()

        st.download_button(
            label="Download Image with Captions",
            data=image_bytes,
            file_name="image_with_captions.png",
            mime="image/png",
        )


