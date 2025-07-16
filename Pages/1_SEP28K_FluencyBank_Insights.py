import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Fluency Bank/Sep 28k Analysis')

st.sidebar.write("""
**Overview:**

This page presents a comprehensive analysis of the FluencyBank and SEP-28k datasets, which have been combined to offer insights into the frequency and distribution of stuttering-related disfluencies. It includes aggregated counts of disfluency types and a time-series trend analysis. Users can filter the SEP-28k dataset by podcast show using the dropdown filter located beneath the page title.
""")
selectbox_placeholder = st.empty()

# Stuttering Events Analysis
def stuttering_events_analysis():
    #Read Data
    fluency_b_data = pd.read_csv("Pages/fluencybank_labels.csv")
    sep_data = pd.read_csv("Pages/SEP-28k_labels.csv")

    # Concatenate Data
    final_data = pd.concat([fluency_b_data,sep_data],ignore_index = True) 
    final_data.index.name = "ID"

    # Convert Start and Stop to seconds
    final_data['Start'] = (final_data['Start']/1000).astype(int)
    final_data['Stop'] = (final_data['Stop']/1000).astype(int)
    cols = ['Prolongation','Block','SoundRep','WordRep','Interjection','NaturalPause']

    # Calculate Total and Mean
    Total = final_data[cols].sum()
    Mean = final_data[cols].mean()
    Count_analysis = pd.concat([Total,Mean],axis = 1)
    Count_analysis.columns = ['Total Count','Mean']

    # Visualize Data - Stuttering Events Analysis
    fig, ax1 = plt.subplots(figsize = (14,6))

    ax1.bar(
        Count_analysis.index,
        Count_analysis['Total Count'],
        color = 'steelblue',
        label = 'Total Count')

    ax2 = ax1.twinx()
    ax2.plot(
        Count_analysis.index,
        Count_analysis['Mean'],
        color = 'orange',
        label = 'Mean',
        marker = 'o',
        linewidth = 2,
        alpha = 1,
        markersize = 8,
        )

    ax1.set_ylabel('Amount of Time Stuttering Type(Seconds)', fontsize = 12)
    ax2.set_ylabel('Mean of Stuttering Type(Seconds)', fontsize = 12)
    ax1.set_ylim(0,32000)
    ax2.set_ylim(0,1)

    ax1.set_xlabel('Stuttering Type', fontsize = 12)
    ax1.set_title('Stuttering Events Analysis', fontsize = 15, fontweight = 'bold')

    plt.setp(ax1.get_xticklabels(), rotation=0)
    plt.tight_layout()
    ax1.legend(loc = 'upper left')
    ax2.legend(loc = 'upper right')
    st.pyplot(fig)

# Normalized Data Analysis
def normalized_data_analysis():
    # Convert from timestamps to minutes
    fluency_b_data = pd.read_csv("Pages/fluencybank_labels.csv")
    fluency_b_data[['Start','Stop']] = (fluency_b_data[['Start','Stop']]/(16000)).astype(float)
    fluency_b_data[['Start','Stop']] = (fluency_b_data[['Start','Stop']]//60)
    fluency_b_data['Total'] = fluency_b_data[['Prolongation','Block','SoundRep','WordRep','Interjection','NaturalPause']].sum(axis=1)

    # Normalize Data
    count_data = fluency_b_data.groupby('Start').count()
    sum_data = fluency_b_data.groupby('Start').sum()

    Normalized_data = sum_data['Total']/count_data['Total']

    # Visualize Data - Normalized Data
    fig, ax = plt.subplots(figsize = (15,8))
    ax.plot(Normalized_data, color = 'steelblue', linewidth = 2)
    ax.set_ylim(2,4)
    ax.set_xlim(0,18)
    ax.set_xlabel('Minutes into the Interview', fontsize = 15)
    ax.set_ylabel('Average Number of Disfluencies', fontsize = 15)
    ax.set_title('Number of Disfluencies over Time(Fluency_Bank Dataset)', fontsize = 16, fontweight = 'bold')
    st.pyplot(fig)

# Number of Disfluencies Analysis
def Num_disfluencies_analysis():
    #Read Data
    sep_data = pd.read_csv('Pages/SEP-28k_labels.csv')
    
    #Convert from timestamps to minutes
    sep_data[['Start','Stop']] = (sep_data[['Start','Stop']]/16000).astype(float)
    sep_data[['Start','Stop']] = (sep_data[['Start','Stop']]//60).astype(int)
    
    #Calculate Total and Normalized Data
    sep_data['Total'] = sep_data[['Prolongation','Block','SoundRep','WordRep','Interjection','NaturalPause']].sum(axis = 1)
    Sum_data = sep_data.groupby(['Show','Start'])['Total'].sum()
    Count_data = sep_data.groupby(['Show','Start'])['Total'].count()

    #Normalize Data
    Normalized_data = (Sum_data/Count_data).reset_index(name = "Normalized")

    #Visualize Data
    podcast_options = ["ALL"] + list(Normalized_data['Show'].unique())
    selected_show = selectbox_placeholder.selectbox('Select a Podcast Show', podcast_options)
    if selected_show != 'ALL':
        filtered_data = Normalized_data[Normalized_data['Show'] == selected_show]
        fig,ax = plt.subplots(figsize = (15,8))
        ax.plot(
            filtered_data['Start'],
            filtered_data['Normalized'],
            color = 'steelblue',
            label = selected_show,
        )

        ax.set_xlabel('Minutes into the Interview', fontsize = 15)
        ax.set_ylabel('Average Number of Disfluencies', fontsize = 15)
        ax.set_title('Number of Disfluencies over Time(Sep - 28k Dataset)', fontsize = 16, fontweight ='bold')
        ax.legend(loc = 'upper left', title = 'Podcast Shows', fontsize= 10, framealpha = 0.8)
        st.pyplot(fig)
    else:
        color_dict = {'HVSA':'red', 'WomenWhoStutter': 'blue', 'HeStutters':'orange', 'StutterTalk': 'green', 'StutteringIsCool': 'purple' , 'IStutterSoWhat': 'teal', 'StrongVoices': 'black'}
        fig, ax = plt.subplots(figsize = (15,8))
        for show, color in color_dict.items():
            show_data = Normalized_data[Normalized_data['Show'] == show]
            sep_plot = ax.plot(
            show_data['Start'],
            show_data['Normalized'],
            color = color,
            label = show, 
            linewidth = 2, 
            alpha = 0.5
                )
        ax.set_xlabel('Minutes into the Interview', fontsize = 15)
        ax.set_ylabel('Average Number of Disfluencies', fontsize = 15)
        ax.set_xlim(0,110)
        ax.set_title('Number of Disfluencies over Time(Sep - 28k Dataset)', fontsize = 16, fontweight ='bold')
        ax.legend(loc = 'upper left', title = 'Podcast Shows', fontsize= 10, framealpha = 0.8)
        st.pyplot(fig)



# Calling Functions
stuttering_events_analysis()
col1, col2 = st.columns(2)
with col1:
    Num_disfluencies_analysis()
with col2:
    normalized_data_analysis()

st.write("""
**Final Insights:**

The visualizations suggest that interjections are the most common type of disfluency across both datasets, followed closely by blocks.
Interjections such as “um,” “uh,” and “ah” are often used by individuals who stutter as a subconscious mechanism to delay speech when 
anticipating a block. While filler words are common in everyday conversation, their frequency is notably higher in stuttered speech.

The temporal trend analysis reveals a relatively stable rate of disfluencies at the beginning of the interviews. However, as the 
conversation progresses, particularly toward the end, there is a marked increase in variability. This includes sharp peaks and drops 
in the number of disfluencies, which may indicate growing cognitive load, fatigue, or changes in speaker confidence over time.
""")


# Visualizing Data per Clip
st.subheader('Dataset Used for Analysis (Fluency Bank/Sep 28k)')
fluency_b_data = pd.read_csv("Pages/fluencybank_labels.csv")
sep_data = pd.read_csv("Pages/SEP-28k_labels.csv")
final_data = pd.concat([fluency_b_data,sep_data],ignore_index = True)
st.write(final_data)