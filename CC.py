from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
import streamlit as st

def add_caption(image, captions):
    for caption in captions:
        font_path, font_size, font_color, position = caption['font'], caption['size'], caption['color'], caption['position']
        
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            font = ImageFont.load_default()

        lines = caption['text'].split('\n')
        x, y = position

        # Create a new image with alpha channel for the text
        txt = Image.new('RGBA', image.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(txt)

        for line in lines:
            # Draw text
            d.text((x, y), line, fill=font_color, font=font)
            y += font.getsize(line)[1]

        # Composite the text image with the original image
        image = Image.alpha_composite(image.convert("RGBA"), txt)
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
        # Convert the hex color to RGBA
        r, g, b = int(font_color[1:3], 16), int(font_color[3:5], 16), int(font_color[5:7], 16)
        font_color = (r, g, b, alpha)
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


