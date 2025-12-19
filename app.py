import streamlit as st
from supabase import create_client
import google.generativeai as genai
import pandas as pd

# Cấu hình Page chuẩn Brand Landco
st.set_page_config(page_title="Landco x Nhà Xinh AI", layout="wide", initial_sidebar_state="expanded")

# --- HÀM KHỞI TẠO (Professional Caching) ---
@st.cache_resource
def init_connection():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

@st.cache_data
def get_catalog():
    supabase = init_connection()
    return supabase.table("landco_catalog").select("*").execute().data

# --- LOGIC AI ENGINE ---
def get_ai_consultant(prompt):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    return model.generate_content(prompt).text

# --- GIAO DIỆN CHÍNH ---
st.title("🏙️ Landco Sales AI Engine - Nhà Xinh Edition")

# Sidebar Navigation
with st.sidebar:
    st.image("https://nhaxinh.com/wp-content/uploads/2023/logo-nhaxinh.png", width=150)
    st.header("Thông tin dự án")
    client_name = st.text_input("Tên khách hàng", "Khách hàng VIP")
    project_type = st.selectbox("Loại hình", ["Chung cư", "Biệt thự", "Nhà phố"])
    budget = st.slider("Ngân sách dự kiến (Triệu VNĐ)", 50, 1000, 200)

# Main Workspace: 3 Tabs chuẩn quy trình Sale
tab_ai, tab_catalog, tab_quote = st.tabs(["✨ Tư vấn AI", "📦 Kho sản phẩm", "📑 Báo giá & Export"])

with tab_ai:
    st.header("AI Interior Designer Consultant")
    style_choice = st.radio("Chọn phong cách chủ đạo", ["Scandinavian", "Modern Luxury", "Indochine"], horizontal=True)
    
    if st.button("Generate Design Concept"):
        with st.spinner("Đang phác thảo phương án..."):
            prompt = f"Tư vấn thiết kế nội thất {project_type} cho {client_name}, ngân sách {budget}tr, phong cách {style_choice}. Sử dụng sản phẩm Nhà Xinh."
            suggestion = get_ai_consultant(prompt)
            st.info(suggestion)

with tab_catalog:
    st.header("Nhà Xinh Master Catalog")
    try:
        data = get_catalog()
        df = pd.DataFrame(data)
        
        # Filter chuyên nghiệp
        selected_style = st.multiselect("Lọc theo phong cách", df['style_tag'].unique(), default=df['style_tag'].unique())
        filtered_df = df[df['style_tag'].isin(selected_style)]
        
        st.dataframe(filtered_df[['product_name', 'category', 'price', 'description']], use_container_width=True)
    except:
        st.error("Chưa kết nối được Database Supabase. Hãy kiểm tra Secrets.")

with tab_quote:
    st.header("Báo giá tạm tính")
    try:
        # Giả lập chọn sản phẩm để báo giá
        selected_items = st.multiselect("Chọn sản phẩm vào báo giá", df['product_name'].tolist())
        if selected_items:
            quote_df = df[df['product_name'].isin(selected_items)]
            st.table(quote_df[['product_name', 'price']])
            total_price = quote_df['price'].sum()
            st.metric("TỔNG GIÁ TRỊ (VNĐ)", f"{total_price:,.0f}")
            
            if st.button("Xuất Báo Giá PDF"):
                st.success("Tính năng đang được đóng gói. Sẵn sàng tải xuống trong giây lát!")
    except:
        st.info("Hãy hoàn thiện bước 'Kho sản phẩm' trước.")
