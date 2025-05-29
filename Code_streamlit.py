# terminal을 통해 pip install streamlit pandas requests beautifulsoup4 plotly 설치

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.express as px

st.set_page_config(page_title="Title")
st.title("Title")

def fetch_jobkorea_jobs():
    url = "https://www.jobkorea.co.kr/Search/?stext=데이터분석"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    job_list = soup.select("div.h7nnv10")

    data = []
    for job in job_list:
        company_tag = job.select_one('a > span.Typography_variant_size16__344nw26')
        company = company_tag.get_text(strip=True) if company_tag else ''

        title_tag = job.select_one('a.h7nnv12 > span.Typography_variant_size18__344nw25')
        title = title_tag.get_text(strip=True) if title_tag else ''

        detail_tags = job.select('div.Flex_direction_row__i0l0hl3 > span')
        detail = [tag.get_text(strip=True) for tag in detail_tags] if detail_tags else []

        link_tag = job.select_one('a.h7nnv12')
        link = link_tag.get("href") if link_tag else ""
        full_url = link if link else ""

        if company and title:
            data.append({
                "Site": "Job_Korea",
                "Col_Company": company,
                "Col_Recruit": title,
                "Col_detail": detail,
                "Col_url": full_url
            })

    return pd.DataFrame(data)


def fetch_incruit_jobs():
    url = "https://search.incruit.com/list/search.asp?col=job&kw=%B5%A5%C0%CC%C5%CD%BA%D0%BC%AE"  # 데이터분석
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    job_list = soup.select("ul.c_row")

    data = []
    for job in job_list:
        company_tag = job.select_one("a.cpname")
        company = company_tag.get_text(strip=True) if company_tag else ''

        title_tag = job.select_one("div.cell_mid a")
        title = title_tag.get_text(strip=True) if title_tag else ''

        detail_tags = job.select("div.cl_md span")
        job_field_tags = job.select("div.cl_btm span")

        detail = [tag.get_text(strip=True) for tag in detail_tags + job_field_tags]

        link = title_tag.get("href") if title_tag else ""
        full_url = link if link else ""

        if company and title:
            data.append({
                "Site": "인크루트",
                "Col_Company": company,
                "Col_Recruit": title,
                "Col_detail": detail,
                "Col_url": full_url
            })

    return pd.DataFrame(data)


if st.button("Recruit Searching"):
    df_jobkorea = fetch_jobkorea_jobs()
    df_incruit = fetch_incruit_jobs()

    if not df_jobkorea.empty and not df_incruit.empty:
        df_merged = pd.concat([df_jobkorea, df_incruit], ignore_index=True)
        st.dataframe(df_merged)

        # summary
        site_counts = df_merged['Site'].value_counts()
        site_ratio = (site_counts / site_counts.sum() * 100).round(2)
        df_summary = pd.DataFrame({
            'Site': site_counts.index,
            'Count': site_counts.values,
            'Ratio': site_ratio.values
        })

        st.dataframe(df_summary)

        # 파이차트
        fig = px.pie(
            df_summary,
            names='Site',
            values='Count',
            title='Recruitment Ratio',
            hole=0
        )
        st.plotly_chart(fig)

    elif not df_jobkorea.empty:
        st.write("인크루트 데이터가 없습니다. 잡코리아 데이터만 표시합니다.")
        st.dataframe(df_jobkorea)

    elif not df_incruit.empty:
        st.write("잡코리아 데이터가 없습니다. 인크루트 데이터만 표시합니다.")
        st.dataframe(df_incruit)

    else:
        st.write("잡코리아와 인크루트 모두 데이터가 없습니다.")


# 실행
# terminal에 streamlit run Code_streamlit.py 입력