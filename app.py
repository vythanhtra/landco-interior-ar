import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Landco Interior AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === CUSTOM CSS ===
st.markdown("""
<style>
.main {background-color: #f5f5f5;}
.stButton>button {
    width: 100%;
    background-color: #007bff;
    color: white;
    border-radius: 5px;
    height: 3em;
}
</style>
""", unsafe_allow_html=True)

# === SIDEBAR ===
st.sidebar.title("🏠 Landco Digital")
st.sidebar.markdown("### AI-Powered Interior Platform")

menu = st.sidebar.radio(
    "Menu",
    ["🏘️ Tổng quan", "📏 Catalog 3D", "🎨 AI Planner", "📊 Financial", "📄 Research"]
)

st.sidebar.markdown("---")
st.sidebar.info("🚀 **MVP Phase 1**\\nStreamlit + AI\\nProduction Ready")

# === MAIN CONTENT ===
if menu == "🏘️ Tổng quan":
    st.title("🎉 Hệ Sinh Thái Nội Thất Thông Minh Landco 2025")
    st.write("Giải pháp Phygital - Kết nối online và offline")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("SKUs", "300+", "+20% AI")
    col2.metric("Reach", "75M+", "Zalo Users")
    col3.metric("Cost Save", "90%", "AI Pipeline")
    
    st.image("https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=800",
             caption="Tầm nhìn không gian số", use_container_width=True)

elif menu == "📏 Catalog 3D":
    st.title("📏 3D Asset Management")
    st.subheader("WebAR - Scene Viewer & AR Quick Look")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400",
                 caption="Sofa Góc L - 15.9M VND")
        if st.button("Xem AR", key="sofa"):
            st.success("🔗 AR Link ready!")
    
    with col2:
        st.image("https://images.unsplash.com/photo-1533090368676-1fd25485db88?w=400",
                 caption="Bàn Trà - 3.5M VND")
        if st.button("Xem AR", key="table"):
            st.success("🔗 AR Link ready!")
    
    with col3:
        st.image("https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400",
                 caption="Tủ Kệ - 8M VND")
        if st.button("Xem AR", key="cabinet"):
            st.success("🔗 AR Link ready!")

elif menu == "🎨 AI Planner":
    st.title("🎨 AI Interior Planner")
    st.write("Upload phòng của bạn, AI sẽ gợi ý thiết kế")
    
    file = st.file_uploader("Tải ảnh phòng", type=["jpg", "png"])
    
    if file:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(file, caption="Input", use_container_width=True)
        
        style = st.selectbox("Phong cách", 
                            ["Minimalist", "Cozy", "Luxury", "Modern"])
        
        if st.button("Run AI Staging"):
            with st.spinner("🤖 AI đang xử lý..."):
                import time
                time.sleep(2)
                with col2:
                    st.image("https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=800",
                             caption=f"AI Result - {style}", use_container_width=True)
                st.success("✅ Hoàn thành!")

elif menu == "📊 Financial":
    st.title("💰 Lộ Trình Tài Chính MVP")
    
    data = {
        "Hạng mục": ["UI/UX", "Mini App", "Flutter App", "Backend AI", "3D Assets"],
        "Budget (USD)": [14000, 6500, 20000, 10000, 3500]
    }
    df = pd.DataFrame(data)
    
    fig = px.bar(df, x="Hạng mục", y="Budget (USD)", 
                 title="Phân Bổ Ngân Sách",
                 color="Budget (USD)")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📈 Timeline")
    timeline = {
        "Phase": ["Research", "MVP", "Launch"],
        "Duration": ["2 tuần", "6 tuần", "2 tuần"],
        "Status": ["✅ Done", "🔄 In Progress", "⏳ Pending"]
    }
    st.table(pd.DataFrame(timeline))

else:  # Research
    st.title("🔍 Phân Tích Arcway.ai")
    st.write("So sánh giải pháp kiến trúc 3D")
    
    st.markdown("""
    | Feature | Arcway.ai | Landco |
    |---------|-----------|--------|
    | Tương tác | CAD-focus | Photorealism |
    | Công nghệ | Cloud | WebGPU + R3F |
    | AI | Limited | Full Pipeline |
    """)
    
    st.info("⚡ Khuyến nghị: AI Sales Agent + 3D Context Understanding")

# === FOOTER ===
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
🎉 <b>Landco Interior AR - MVP 2025</b><br>
Powered by Streamlit + AI | Made with ❤️ for VN Market<br>
<a href='https://github.com/vythanhtra/landco-interior-ar'>GitHub</a>
</div>
""", unsafe_allow_html=True)
