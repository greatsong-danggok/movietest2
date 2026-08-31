import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================
# 기본 설정
# =========================================================
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")
st.caption("출처: KOBIS 일별 박스오피스 10위권 (최근 1년치)")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# =========================================================
# 데이터 불러오기
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig", dtype={"날짜": str})
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()


# =========================================================
# 그래프 1. 영화별 날짜에 따른 일관객 변화
# =========================================================
st.header("그래프 1. 영화별 일관객 변화")

movie_list = sorted(df["영화명"].unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list)

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
    .loc[:, ["날짜", "일관객"]]
)

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    labels={"날짜": "날짜", "일관객": "일일 관객 수"},
    title=f"'{selected_movie}' 날짜별 일관객 변화",
)
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)
fig1.update_layout(hovermode="x unified")

st.plotly_chart(fig1, use_container_width=True)

# --- 이 그래프로 알 수 있는 것 (문구를 이 자리에 채워 넣으세요) ---
insight_1 = "이 그래프로 알 수 있는 것: (여기에 한 문장을 입력하세요)"
st.info(insight_1)

st.divider()


# =========================================================
# 그래프 2. 일관객 합계 상위 5편의 날짜별 일관객 비교
# =========================================================
st.header("그래프 2. 상위 5편 일관객 비교")

top5_movies = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).head(5).index
)

top5_df = (
    df[df["영화명"].isin(top5_movies)]
    .sort_values("날짜")
    .loc[:, ["날짜", "영화명", "일관객"]]
)

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    labels={"날짜": "날짜", "일관객": "일일 관객 수", "영화명": "영화명"},
    title="일관객 합계 상위 5편 날짜별 일관객",
)
fig2.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra>%{fullData.name}</extra>"
)
fig2.update_layout(hovermode="x unified", legend_title_text="영화명 (클릭해서 켜고 끄기)")

st.plotly_chart(fig2, use_container_width=True)

insight_2 = "이 그래프로 알 수 있는 것: (여기에 한 문장을 입력하세요)"
st.info(insight_2)

st.divider()


# =========================================================
# 그래프 3. (다음 그래프를 이 아래에 추가하세요)
# =========================================================
# st.header("그래프 3. ...")
#
# fig3 = px.line(...)
# st.plotly_chart(fig3, use_container_width=True)
#
# insight_3 = "이 그래프로 알 수 있는 것: (여기에 한 문장을 입력하세요)"
# st.info(insight_3)
#
# st.divider()
