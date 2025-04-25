import streamlit as st
from rembg import remove
from PIL import Image
import io
import base64

def get_image_download_link(img, filename, text):
    """Generate a link to download an image"""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

def main():
    st.set_page_config(page_title="InvisiBG", page_icon="✂️")

    st.title("🔲 InvisiBG")
    st.write("Upload an image to remove the background!")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display original image
        image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(image, use_column_width=True)

        # Add a button to process the image
        if st.button("Remove Background"):
            with st.spinner("Processing image..."):
                # Remove background
                output = remove(image)

                # Display result
                with col2:
                    st.subheader("Background Removed")
                    st.image(output, use_column_width=True)

                # Download button
                st.markdown(
                    get_image_download_link(output, "bg_removed.png", "Download Processed Image"),
                    unsafe_allow_html=True
                )

                # Technical details expander
                with st.expander("Technical Details"):
                    st.write("""
                    This app uses the `rembg` library, which implements a deep learning model to identify
                    and remove backgrounds from images. The model is based on U^2-Net architecture trained
                    specifically for salient object detection and segmentation.
                    """)

if __name__ == "__main__":
    main()
