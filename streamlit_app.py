import streamlit as st

# 設定頁面標題與圖示
st.set_page_config(
    page_title="肥力計算",
    page_icon="🌱",
    layout="centered"
)

# 大標題
st.title("🌱 肥力計算")

# 小標題說明
st.subheader("使用 TDS 與水溫計算出概略 EC 值並加上 pH 值")
st.subheader("檢測土壤肥力與適合栽種的蔬果")

# 空行分隔
st.markdown("---")

# 製作者資訊
st.markdown("**製作者：** Ramon  \n📧 ramon20221108@gmail.com")
import streamlit as st

def classify_ph_ec(ph, ec):
    if ph < 5.5:
        ph_status = "低 pH"
    elif ph > 7.0:
        ph_status = "高 pH"
    else:
        ph_status = "最適 pH"

    if ec < 1.0:
        ec_status = "低 EC"
    elif ec > 3.0:
        ec_status = "高 EC"
    else:
        ec_status = "最適 EC"

    return ph_status, ec_status

def recommend_crops(ph_status, ec_status):
    if ph_status == "高 pH" and ec_status == "高 EC":
        return [
            "蘆筍（鹼性耐鹽）",
            "甜菜（耐鹽）",
            "石蓮花（耐鹼性土壤）"
        ], "鹼性＋鹽害，建議酸化水源並進行灌溉淋洗"

    elif ph_status == "高 pH" and ec_status == "低 EC":
        return [
            "羽衣甘藍（可耐弱鹼）",
            "黑麥草（耐鹼耐貧瘠）",
            "洋蔥（適中耐鹼）"
        ], "鹼性＋缺肥，建議使用酸性肥料並補充微量元素"

    elif ph_status == "低 pH" and ec_status == "高 EC":
        return [
            "野薑花（耐酸＋部分耐鹽）",
            "蘭花（偏酸性＋可控濃肥）",
            "高麗菜（育苗期避免鹽害）"
        ], "酸性＋鹽害，建議調高 pH 並淋洗鹽分"

    elif ph_status == "低 pH" and ec_status == "低 EC":
        return [
            "藍莓（最適 pH 4.5-5.5）",
            "茶樹（喜酸性土壤）",
            "蕨類（耐酸且需低鹽環境）"
        ], "酸性＋缺肥，適合酸性植物，但仍需補充養分"

    else:
        return [
            "番茄",
            "小黃瓜",
            "萵苣"
        ], "pH 與 EC 均正常，可廣泛種植大多數蔬果"

def temperature_compensated_ec(tds, temperature_c):
    return (tds / 640) / (1 + 0.02 * (temperature_c - 25))

# Streamlit UI
st.title("🌱 土壤分析與作物推薦工具")
st.markdown("輸入 TDS、溫度與 pH 值，我們會計算 EC 並推薦適合的作物")

tds = st.number_input("🔬 TDS (ppm)", min_value=0.0, step=0.1)
temperature = st.number_input("🌡️ 溫度 (°C)", min_value=0.0, max_value=50.0, value=25.0, step=0.1)
ph = st.number_input("🧪 pH 值", min_value=0.0, max_value=14.0, step=0.1)

if st.button("分析並推薦作物"):
    ec = temperature_compensated_ec(tds, temperature)
    ph_status, ec_status = classify_ph_ec(ph, ec)
    crops, advice = recommend_crops(ph_status, ec_status)

    st.success(f"🔎 判定結果：{ph_status} / {ec_status}")
    st.info(f"📊 計算後 EC 值（已溫度補償）：{ec:.2f} dS/m")
    st.write(f"🌿 適合種植：{', '.join(crops)}")
    st.warning(f"📌 建議：{advice}")
