import streamlit as st
import requests
from io import BytesIO

# Function to remove background using remove.bg API
def remove_background(api_key, image_bytes):
    url = "https://api.remove.bg/v1.0/removebg"
    headers = {
        "X-Api-Key": api_key
    }
    files = {
        "image_file": image_bytes
    }
    params = {
        "size": "auto"
    }
    
    try:
        response = requests.post(url, headers=headers, files=files, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Save the result to a file
        result_image = BytesIO(response.content)
        
        return result_image  # Return the image bytes
    except requests.exceptions.RequestException as e:
        st.error(f"Error removing background: {e}")
        st.error(f"Status code: {response.status_code}")
        st.error(f"Response text: {response.text}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

# Streamlit app
st.title("Background Remover")

st.write("Upload an image and click 'Remove Background'")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Original Image", use_column_width=True)
    if st.button("Remove Background"):
        st.write("Removing background...")
        api_key = "JPjpw56N9aAGzVdcfd37ijJr"  # Replace with your remove.bg API key
        result_image = remove_background(api_key, uploaded_file.read())
        if result_image:
            st.image(result_image, caption="Image with Background Removed", use_column_width=True)
            st.success("Background removed successfully!")
        else:
            st.error("Failed to remove background. Please check your API key and try again.")
