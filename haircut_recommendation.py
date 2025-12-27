import streamlit as st
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="髮型建議助手", page_icon="✂️")

st.title("✂️ AI 髮型建議助手")
st.write("影張相，等 AI 幫你搵返個最襯你嘅髮型！")

# Initialize OpenAI client for Poe
api_key = os.getenv("API_KEY")
if not api_key:
    st.error("請在 .env 檔案中設置 POE_API_KEY")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.poe.com/v1",
)

def encode_image(image_file):
    """Encode image to base64."""
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

def get_haircut_recommendation(image_base64):
    """Get haircut recommendation from Poe API."""
    try:
        response = client.chat.completions.create(
            model="Claude-3.5-Sonnet",  # Using GPT-4o for vision capabilities
            messages=[
                {
                    "role": "system",
                    "content": "你是一位專業的髮型師。請分析用戶的面型、五官特徵，並用廣東話（Cantonese）提供 3 個適合的髮型建議。請解釋點解呢啲髮型適合佢，並給予一些打理建議。"
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "請幫我分析呢張相，並提供髮型建議。"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"發生錯誤: {str(e)}"

# Camera input
img_file = st.camera_input("影張相先")

if img_file:
    # Display processing message
    with st.spinner("AI 正在分析緊你嘅面型，請稍等..."):
        # Encode image
        base64_image = encode_image(img_file)
        
        # Get recommendation
        recommendation = get_haircut_recommendation(base64_image)
        
        # Display recommendation
        st.subheader("🤖 AI 髮型建議：")
        st.markdown(recommendation)

