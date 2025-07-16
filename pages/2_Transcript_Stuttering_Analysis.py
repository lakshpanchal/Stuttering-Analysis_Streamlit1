import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



st.set_page_config(layout = 'wide')
st.title('Transcript Stuttering Analysis')

st.sidebar.write("""
**Overview:**

This page presents a comprehensive analysis of the stuttering patterns in the transcript dataset. 
It includes aggregated counts of disfluency types and a time-series trend analysis. Users can filter the 
transcript dataset by clip ID using the dropdown filter located beneath the page title.
""")

#Data Loading
transcript =pd.read_excel("pages/Letter Transcription.xlsx")
clip_options = transcript['Clip ID'].unique()
selected_clip = st.selectbox('Select A Clip ID', sorted(clip_options))
filtered_transcript = transcript[transcript['Clip ID'] == selected_clip] 

#KPI1 - total people
total_people = transcript['Clip ID'].nunique()

#KPI2 - Average Stutter Duration
transcript['duration'] = transcript['Stop'] - transcript['Start']
avg_duration = transcript['duration'].mean()

#KPI3 - Max Stutter Duration per clip
max_duration = filtered_transcript['Stop'] - filtered_transcript['Start']
max_duration_value = max_duration.max()

#KPI4 - Avergae Stutter Rate per Minute(Per clip)
clip_duration_sec = filtered_transcript['Stop'].max() - filtered_transcript['Start'].min()
clip_duration_min = clip_duration_sec/60
stutter_rate = filtered_transcript['Disfluency Type'].count()/clip_duration_min

#Visualizing KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('Total People', total_people)
with col2:
    st.metric('Average Stutter Duration', f'{round(avg_duration,2)} sec')
with col3:
    st.metric(f'Max Stutter Duration({selected_clip})', round(max_duration_value,2))
with col4:
    st.metric(f'Stutter Rate Per Minute({selected_clip})', round(stutter_rate,2))

# Macro - Letter Count Bar Chart
def draw_letter_count_bar_chart():
    letter_counts = transcript['Letter(s)'].value_counts()
    fig, ax = plt.subplots(figsize = (10,4))
    ax.bar(letter_counts.index, letter_counts.values)
    ax.set_xlabel('Letter', fontsize = 15)
    ax.set_ylabel('Total Count', fontsize = 15)
    ax.set_title('Stuttered Letter Count (All Clips)', fontsize = 16, fontweight = 'bold')
    ax.set_xticklabels(letter_counts.index, rotation = 0)
    fig.tight_layout()
    st.pyplot(fig)

# Micro - Disfluency Type Bar Chart(By Clip)
def draw_disfluency_type_bar_chart():
    disfluency_counts = filtered_transcript['Disfluency Type'].value_counts()
    fig,ax = plt.subplots(figsize = (10,4))
    ax.bar(disfluency_counts.index,disfluency_counts.values)
    ax.set_xlabel('Dislfuency Types', fontsize = 15)
    ax.set_ylabel('Total Count', fontsize = 15)
    ax.set_title(f'Disfluency Type Bar Chart for Clip # {selected_clip}', fontsize = 16, fontweight = 'bold')
    ax.set_xticklabels(disfluency_counts.index, rotation=0)
    fig.tight_layout()
    st.pyplot(fig)

# Micro -Trend Analysis Chart
def draw_trend_analysis_chart():
    bins = pd.cut(filtered_transcript['Start'],bins = 10)
    time_bins= filtered_transcript.groupby(bins)['Start'].count()
    midpoints = [round(interval.mid,2) for interval in time_bins.index]
    fig,ax = plt.subplots(figsize = (10,4))
    ax.plot(midpoints,time_bins.values, marker = 'o', linestyle = '-', color = 'blue')
    ax.set_xlabel('Time(sec)', fontsize = 15)
    ax.set_ylabel('Total Count', fontsize = 15)
    ax.set_title(f"Trend Analysis Chart for Clip # {selected_clip}", fontsize = 16, fontweight = 'bold')
    ax.set_xticks(midpoints)
    ax.set_xticklabels(midpoints, rotation = 0, fontsize = 12)
    fig.tight_layout()
    st.pyplot(fig)

# Macro Trend Analysis Chart - needs to be normalized
def micro_letter_count_analysis_chart():
    letter_counts = filtered_transcript['Letter(s)'].value_counts()
    fig,ax = plt.subplots(figsize = (10,4))
    ax.bar(letter_counts.index,letter_counts.values)
    ax.set_xlabel('Letter', fontsize = 15)
    ax.set_ylabel("Total Count", fontsize = 15)
    ax.set_title(f'Letter Count Analysis for Clip # {selected_clip}', fontsize = 16, fontweight = 'bold')
    ax.set_xticklabels(letter_counts.index, rotation = 0, fontsize = 12)
    fig.tight_layout()
    st.pyplot(fig)

# Final Analysis
st.subheader('Letter Count Analysis')
col1, col2 = st.columns(2)
with col1:
    draw_letter_count_bar_chart()
with col2:
    micro_letter_count_analysis_chart()
st.subheader('Disfluency Over Time')
col1, col2, = st.columns(2)
with col1:
    draw_disfluency_type_bar_chart()
with col2:
    draw_trend_analysis_chart()

st.write("""
**Final Insights:**

This portion of the project stemmed from a personal hypothesis: that stuttering most often occurs on vowel-initiated words. 
As someone who personally struggles with vowel sounds during speech, I was curious to explore whether this pattern held true across other speakers. 
To test this, I built a dataset using Whisper AI for transcription and added manual annotations of stuttered letters across multiple interview clips.

However, the data revealed a surprising insight. Contrary to my expectations, the most frequently stuttered-on letter was "S", followed by "I",
with other consonants like "M", "TH", and "F" also appearing prominently. While vowels such as "A" and "I" were present, other vowels
like "U" and "O" were not the dominant triggers of disfluency. This challenges my assumption that vowels are the primary difficulty for 
people who stutter and highlights the individualized nature of stuttering patterns.
""")

# Visualizing Data per Clip
st.subheader(f"Dataset Used for Analysis - Clip # {selected_clip}")
st.dataframe(filtered_transcript[['Clip ID','Start','Stop','Disfluency Type','Age Range','Letter(s)','Link']])



