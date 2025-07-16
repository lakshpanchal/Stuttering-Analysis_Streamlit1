import streamlit as st

st.title('Project Overview')


st.write("""I’ve struggled with stuttering all my life, and this project was born out of a personal mission to better understand the patterns behind it. While researching potential datasets, I came across **FluencyBank**, 
a database of speech samples curated for the study of fluency and disfluency across age groups, and **SEP-28k**, a labeled dataset focused specifically on stuttering events in podcast interviews. Using these datasets, I built an 
analysis that explores the different types of disfluencies including blocks, repetitions, and interjections and how they evolve over time during natural speech. With tools like Pandas, Matplotlib, and Streamlit, I developed interactive visuals 
that break down stuttering trends by podcast show, time into the interview, and disfluency category.

What makes this project especially personal is my own experience with stuttering, particularly on vowel sounds. To dive deeper into that,
 I created a custom dataset by manually labeling stuttering events using video interviews. I used **Whisper AI** to transcribe speech and extract timestamped segments, 
 then reviewed each instance to identify the specific letter and type of disfluency involved. This hands-on approach allowed me to better understand the nuances of how others stutter in real-world conversations. 
 My goal was not only to explore this from a data analysis standpoint but also to make the experience of stuttering more visible, measurable, and ultimately better understood.
 
**Datasets Used** - This project draws on two key datasets to explore patterns in stuttering across different contexts and populations:

FluencyBank: A comprehensive collection of speech samples spanning children, adults, and older individuals. This dataset provides rich, real-world audio data for analyzing various disfluency patterns across age groups and demographics.

SEP-28k: A curated dataset featuring labeled speech samples from podcasts such as He Stutters, StutterTalk, and Stuttering is Cool. This dataset is especially valuable for identifying and categorizing stuttering events in more natural conversational environments.

Transcript Stuttering Analysis:
I manually trasncribed this dataset from the interviews in the FluencyBank dataset. The FluencyBank dataset had the counts of disfluency types but not the actual letters 
stuttered on so I used these interviews, whisper ai, and my knowledge of stuttering events to transcribe the interviews and label the stuttering events.

**Project Structure** - The dashboard is organized into two main pages:

FluencyBank / SEP-28k Analysis: 
This section provides insights into stuttering behavior based on the FluencyBank and SEP-28k datasets. It features visualizations and metrics focused on disfluency types, frequency, and normalized stuttering events across diverse speech samples.

Transcript Stuttering Analysis: 
This section is based on a manually transcribed dataset developed for this project. Using Whisper AI and timestamped labeling, the analysis dives into specific stuttering patterns (especially around letters), disfluency types, and duration across interviews.
 """)
