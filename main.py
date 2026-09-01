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
# 그래프 3. 날짜별 10위권 일관객 합계 (영역 그래프)
# =========================================================
st.header("그래프 3. 날짜별 박스오피스 10위권 전체 관객 수")

daily_total = df.groupby("날짜")["일관객"].sum().reset_index()
daily_total.columns = ["날짜", "합계관객"]

fig3 = px.area(
    daily_total,
    x="날짜",
    y="합계관객",
    labels={"날짜": "날짜", "합계관객": "10위권 일관객 합계"},
    title="날짜별 박스오피스 10위권 일관객 합계",
)
fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계: %{y:,}명<extra></extra>"
)

# --- 합계가 가장 컸던 3일 표시 ---
top3_days = daily_total.sort_values("합계관객", ascending=False).head(3)

fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["합계관객"],
    mode="markers+text",
    text=top3_days["날짜"].dt.strftime("%Y-%m-%d"),
    textposition="top center",
    marker=dict(size=10, color="crimson"),
    name="합계 상위 3일",
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계: %{y:,}명<extra>상위 3일</extra>",
)

st.plotly_chart(fig3, use_container_width=True)

insight_3 = "이 그래프로 알 수 있는 것: (여기에 한 문장을 입력하세요)"
st.info(insight_3)

st.divider()


# =========================================================
# 그래프 4. 일관객 합계 TOP 10 영화 (가로 막대그래프)
# =========================================================
st.header("그래프 4. 일관객 합계 TOP 10 영화")

movie_summary = (
    df.groupby("영화명")
    .agg(합계관객=("일관객", "sum"), 상영일수=("날짜", "count"))
    .reset_index()
)
top10_movies = movie_summary.sort_values("합계관객", ascending=False).head(10)

fig4 = px.bar(
    top10_movies,
    x="합계관객",
    y="영화명",
    orientation="h",
    custom_data=["상영일수"],
    labels={"합계관객": "일관객 합계", "영화명": "영화명"},
    title="일관객 합계 TOP 10 영화",
)
fig4.update_traces(
    hovertemplate="%{y}<br>일관객 합계: %{x:,}명<br>10위권 진입 날수: %{customdata[0]}일<extra></extra>"
)
fig4.update_yaxes(categoryorder="total ascending")

st.plotly_chart(fig4, use_container_width=True)

insight_4 = "이 그래프로 알 수 있는 것: (여기에 한 문장을 입력하세요)"
st.info(insight_4)

st.divider()


# =========================================================
# 그래프 5. 월 × 요일별 일관객 합계 히트맵
# =========================================================
st.header("그래프 5. 월 × 요일별 일관객 합계")

heat_df = df.copy()
heat_df["월"] = heat_df["날짜"].dt.strftime("%Y-%m")
weekday_map = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}
heat_df["요일"] = heat_df["날짜"].dt.dayofweek.map(weekday_map)

weekday_order = ["월", "화", "수", "목", "금", "토", "일"]
pivot = (
    heat_df.pivot_table(
        index="월", columns="요일", values="일관객", aggfunc="sum", fill_value=0
    )
    .reindex(columns=weekday_order)
    .sort_index()
)

fig5 = px.imshow(
    pivot,
    color_continuous_scale="Reds",
    labels=dict(x="요일", y="월", color="일관객 합계"),
    aspect="auto",
    title="월 × 요일별 일관객 합계",
)
fig5.update_traces(
    hovertemplate="월: %{y}<br>요일: %{x}<br>합계: %{z:,}명<extra></extra>"
)

st.plotly_chart(fig5, use_container_width=True)

insight_5 = "이 그래프로 알 수 있는 것: (여기에 한 문장을 입력하세요)"
st.info(insight_5)

st.divider()


# =========================================================
# 그래프 6. (다음 그래프를 이 아래에 추가하세요)
# =========================================================
# st.header("그래프 6. ...")
#
# fig6 = px.line(...)
# st.plotly_chart(fig6, use_container_width=True)
#
# insight_6 = "이 그래프로 알 수 있는 것: (여기에 한 문장을 입력하세요)"
# st.info(insight_6)
#
# st.divider()
