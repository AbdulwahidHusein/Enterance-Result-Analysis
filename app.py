import streamlit as st
import pandas as pd
import ast
import matplotlib.pyplot as plt

st.set_page_config(page_title='Gedebano School Results and Analytics', layout='wide')
st.title('Gedebano School Entrance Exam Results and Analytics')

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv('results_unique.csv')

df = load_data()

# Define subjects for each stream
social_science_subjects = ['English', 'Mathematics', 'Geography', 'Scholastic Aptitude Test', 'Economics', 'History']
natural_science_subjects = ['Chemistry', 'English', 'Mathematics', 'Physics', 'Biology', 'Scholastic Aptitude Test']

# Function to get student results
def get_student_results(admission_number):
    try:
        student = df[df['admission_number'].astype(str) == admission_number]
        if not student.empty:
            student = student.iloc[0]
            scores = ast.literal_eval(student['subject_scores'])
            return {
                'Name': student['name'],
                'Gender': student['gender'],
                'Stream': student['stream'],
                'School': student['school'],
                'Total Score': student['total_score'],
                'Subject Scores': scores
            }
        else:
            return None
    except Exception as e:
        st.error(f"Error retrieving student data: {e}")
        return None

# Function to get analytics
def get_analytics():
    # Ranking by stream
    rankings = {}
    for stream in df['stream'].unique():
        stream_df = df[df['stream'] == stream]
        stream_df = stream_df.sort_values(by='total_score', ascending=False).reset_index(drop=True)
        rankings[stream] = stream_df.head(10)[['admission_number', 'name', 'total_score']].reset_index(drop=True)

    # Top scores by subject
    top_scores = {}
    for stream, subjects in [('Social Sc.', social_science_subjects), ('Natural Sc.', natural_science_subjects)]:
        stream_df = df[df['stream'] == stream]
        for subject in subjects:
            subject_scores = []
            for index, row in stream_df.iterrows():
                scores = ast.literal_eval(row['subject_scores'])
                score = int(scores.get(subject, 0))
                subject_scores.append((row['admission_number'], row['name'], score))
            top_scores[subject] = pd.DataFrame(sorted(subject_scores, key=lambda x: x[2], reverse=True)[:5], columns=['Admission Number', 'Name', 'Score'])

    # Calculate average scores and percentage of students scoring >= 50%
    avg_scores = {}
    above_50_percent = {}
    for stream, subjects in [('Social Sc.', social_science_subjects), ('Natural Sc.', natural_science_subjects)]:
        stream_df = df[df['stream'] == stream]
        for subject in subjects:
            subject_scores = []
            for index, row in stream_df.iterrows():
                scores = ast.literal_eval(row['subject_scores'])
                score = int(scores.get(subject, 0))
                subject_scores.append(score)
            avg_scores[subject] = (sum(subject_scores) / len(subject_scores)) if subject_scores else 0
            above_50_percent[subject] = sum(score >= 50 for score in subject_scores) / len(subject_scores) * 100 if subject_scores else 0

    return rankings, top_scores, avg_scores, above_50_percent

# Create the Streamlit app

# Input for student ID
col1, col2 = st.columns([3, 1])
with col1:
    admission_number = st.text_input('Enter Admission Number:', key='admission_number', placeholder='e.g., 12345')
with col2:
    st.write('')  # Just an empty space to align the button

# Button to submit
if st.button('Get Results'):
    if admission_number:
        results = get_student_results(admission_number)
        if results:
            st.subheader('Student Results')
            st.markdown(f"**Name:** {results['Name']}")
            st.markdown(f"**Gender:** {results['Gender']}")
            st.markdown(f"**Stream:** {results['Stream']}")
            st.markdown(f"**School:** {results['School']}")
            st.markdown(f"**Total Score:** {results['Total Score']}")
            st.markdown("**Subject Scores:**")
            for subject, score in results['Subject Scores'].items():
                st.markdown(f"- {subject}: {score}")
        else:
            st.warning("No results found for this admission number.")
    else:
        st.warning("Please enter an admission number.")

# Show analytics
st.subheader('Analytics')

# Display rankings
rankings, top_scores, avg_scores, above_50_percent = get_analytics()

# Display top scores
st.write('### Top Scores by Stream')
for stream, ranking_df in rankings.items():
    st.write(f"**{stream}**")
    st.dataframe(ranking_df.style.set_properties(**{'text-align': 'center'}).background_gradient(cmap='Blues'))

# Display top scores by subject
st.write('### Top Scores by Subject')
for subject, top_df in top_scores.items():
    st.write(f"**{subject}**")
    st.dataframe(top_df.style.set_properties(**{'text-align': 'center'}).background_gradient(cmap='Greens'))

# Display average scores and percentage of students scoring >= 50%
st.write('### Average Scores per Subject')
avg_scores_df = pd.DataFrame(list(avg_scores.items()), columns=['Subject', 'Average Score'])
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(avg_scores_df['Subject'], avg_scores_df['Average Score'], color='skyblue')
ax.set_xlabel('Subject')
ax.set_ylabel('Average Score (Out of 100)')
ax.set_title('Average Score per Subject')
ax.set_xticklabels(avg_scores_df['Subject'], rotation=45, ha='right')
for i, v in enumerate(avg_scores_df['Average Score']):
    ax.text(i, v + 1, f"{v:.1f}", ha='center', va='bottom')
st.pyplot(fig)

st.write('### Percentage of Students with Score more than or equal to 50% per Subject')
above_50_df = pd.DataFrame(list(above_50_percent.items()), columns=['Subject', 'Percentage >= 50%'])
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(above_50_df['Subject'], above_50_df['Percentage >= 50%'], color='salmon')
ax.set_xlabel('Subject')
ax.set_ylabel('Percentage >= 50%')
ax.set_title('Percentage of Students Scoring >= 50%')
ax.set_xticklabels(above_50_df['Subject'], rotation=45, ha='right')
for i, v in enumerate(above_50_df['Percentage >= 50%']):
    ax.text(i, v + 1, f"{v:.1f}%", ha='center', va='bottom')
st.pyplot(fig)
