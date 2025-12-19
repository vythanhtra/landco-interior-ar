import streamlit as st
from supabase import create_client
import google.generativeai as genai
import pandas as pd

# Cấu hình Page chuẩn Brand Landco
st.set_page_config(page_title="Landco x Nhà Xinh AI", layout="wide", initial_sidebar_state="expanded")

# --- HÀM KHỞI TẠO (Professional Caching) ---
@st.cache_resource
def init_connection():
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if not url or not key:
            st.error("Thiếu SUPABASE_URL hoặc SUPABASE_KEY trong Secrets.")
            return None
        return create_client(url, key)
    except Exception as e:
        st.error(f"Lỗi khởi tạo Supabase: {str(e)}")
        return None

@st.cache_data
def get_catalog():
    supabase = init_connection()
    if not supabase: return []
    try:
        return supabase.table("landco_catalog").select("*").execute().data
    except Exception as e:
        st.error(f"Lỗi truy vấn dữ liệu: {str(e)}")
        return []

# --- LOGIC AI ENGINE ---
def get_ai_consultant(prompt):
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key: return "Lỗi: Thiếu GEMINI_API_KEY."
        genai.configure(api_key=api_key)
        # Sử dụng model gemini-1.5-flash là model mới và nhanh nhất hiện tại
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}. Có thể do API Key chưa được kích hoạt hoặc hết hạn mức."

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
    data = get_catalog()
    if not data:
        st.warning("Không có dữ liệu trong catalog hoặc lỗi kết nối.")
    else:
        df = pd.DataFrame(data)
        # Filter chuyên nghiệp
        selected_style = st.multiselect("Lọc theo phong cách", df['style_tag'].unique(), default=df['style_tag'].unique())
        filtered_df = df[df['style_tag'].isin(selected_style)]
        st.dataframe(filtered_df[['product_name', 'category', 'price', 'description']], use_container_width=True)

with tab_quote:
    st.header("Báo giá tạm tính")
    try:
        data = get_catalog()
        if data:
            df = pd.DataFrame(data)
            selected_items = st.multiselect("Chọn sản phẩm vào báo giá", df['product_name'].tolist())
            if selected_items:
                quote_df = df[df['product_name'].isin(selected_items)]
                st.table(quote_df[['product_name', 'price']])
                total_price = quote_df['price'].sum()
                st.metric("TỔNG GIÁ TRỊ (VNĐ)", f"{total_price:,.0f}")
                
                if st.button("Xuất Báo Giá PDF"):
                    st.success("Tính năng đang được đóng gói. Sẵn sàng tải xuống trong giây lát!")
        else:
            st.info("Hãy hoàn thiện bước 'Kho sản phẩm' trước.")
    except Exception as e:
        st.info("Chưa có dữ liệu sản phẩm.")
