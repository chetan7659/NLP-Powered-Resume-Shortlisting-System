import streamlit as st

# Page Config must be the first Streamlit command
st.set_page_config(page_title="AI Resume Shortlister", layout="wide")

import pandas as pd
from parsing import resume_parser, jd_parser
from matching import skill_matcher, scorer
from explanation import gemini_explainer
from sklearn.metrics.pairwise import cosine_similarity

def main():
    st.title("AI Resume Shortlister 🚀")
    st.markdown("---")

    # 1. Inputs: JD & Skills
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Job Description (Compulsory)")
        jd_text = st.text_area("Paste the Job Description here", height=300, key="jd_input")
    
    with col2:
        st.subheader("2. Required Skills (Compulsory)")
        manual_skills = st.text_input("Enter key skills (comma-separated)", placeholder="Python, SQL, Project Management...", key="skills_input")
        st.caption("These will be merged with skills extracted from the JD.")
        
        st.subheader("3. Upload Resumes")
        uploaded_files = st.file_uploader("Upload PDF or DOCX files", type=["pdf", "docx"], accept_multiple_files=True)

    # 2. Action
    if st.button("Evaluate Candidates", type="primary"):
        if not jd_text:
            st.error("❌ Please ensure Job Description is provided.")
            return
        
        if not manual_skills:
            st.error("❌ Please ensure required skills are entered.")
            return

        if not uploaded_files:
            st.error("❌ Please upload at least one resume.")
            return

        # 3. Processing
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Parse JD
        status_text.text("Parsing Job Description...")
        try:
            parsed_jd = jd_parser.parse_jd(jd_text)
            input_skill_list = [s.strip() for s in manual_skills.split(",") if s.strip()]
            parsed_jd["required_skills"] = list(set(parsed_jd["required_skills"] + input_skill_list))
            
            # Encode JD for similarity
            jd_embedding = skill_matcher.model.encode(jd_text)
            
        except Exception as e:
            st.error(f"Error parsing JD: {e}")
            return

        total_files = len(uploaded_files)
        
        for idx, file in enumerate(uploaded_files):
            status_text.text(f"Processing {file.name} ({idx+1}/{total_files})...")
            
            try:
                # A. Parse Resume Text
                resume_text = resume_parser.extract_resume_text(file)
                
                # B. Extract Data from Resume (Reusing JD logic for consistency)
                resume_skills = jd_parser.extract_skills(resume_text)
                resume_exp = jd_parser.extract_experience(resume_text)
                
                # C. Compute Semantic Similarity (Whole Text)
                resume_embedding = skill_matcher.model.encode(resume_text)
                jd_similarity = cosine_similarity([jd_embedding], [resume_embedding])[0][0]
                
                # Project Score (New)
                proj_score = scorer.calculate_project_score(resume_text)
                
                parsed_resume = {
                    "text": resume_text,
                    "skills": resume_skills,
                    "experience_years": resume_exp,
                    "jd_similarity": jd_similarity,
                    "project_score": proj_score
                }
                
                # D. Match Skills
                match_result = skill_matcher.match_skills(parsed_resume["skills"], parsed_jd["required_skills"])
                
                # E. Score
                score_data = scorer.score_resume(parsed_resume, parsed_jd, match_result)
                
                # F. Explain (Gemini)
                explanation = gemini_explainer.generate_explanation(score_data)
                
                results.append({
                    "Name": file.name,
                    "Score": score_data["final_score"],
                    "Match Ratio": score_data["skill_match"],
                    "Experience": score_data["experience_match"],
                    "Explanation": explanation,
                    "Details": score_data,
                    "Text Preview": resume_text[:500] + "..." # Preview
                })
                
            except Exception as e:
                st.warning(f"Failed to process {file.name}: {e}")
            
            progress_bar.progress((idx + 1) / total_files)

        status_text.text("Analysis Complete!")
        
        # 4. Display Results
        if results:
            st.markdown("### 🏆 Ranked Candidates")
            
            df = pd.DataFrame(results).sort_values(by="Score", ascending=False)
            
            # Highlight top candidate
            st.metric("Top Candidate", df.iloc[0]["Name"], f"{df.iloc[0]['Score']} / 100")
            
            # Bar Chart of Scores
            st.bar_chart(df.set_index("Name")["Score"])
            
            # Display Summary Table
            st.dataframe(
                df[["Name", "Score", "Match Ratio", "Experience"]],
                use_container_width=True,
                hide_index=True
            )
            
            # Detailed Explanations
            st.markdown("### 📝 Detailed Insights")
            for _, row in df.iterrows():
                with st.expander(f"**{row['Name']}** - Score: {row['Score']}"):
                    st.markdown(f"**Why shortlisted:**")
                    st.write(row["Explanation"])
                    
                    st.markdown("---")
                    
                    # Columns for details
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown("**✅ Matched Skills**")
                        st.caption(", ".join(row["Details"]["matched_skills"]))
                    with c2:
                        st.markdown("**⚠️ Missing Skills**")
                        st.caption(", ".join(row["Details"]["missing_skills"]))
                    with c3:
                        st.markdown("**📄 Quick Preview**")
                        st.text(row["Text Preview"])
            
            # Detailed Explanations
            st.markdown("### 📝 Detailed Insights")
            for _, row in df.iterrows():
                with st.expander(f"**{row['Name']}** - Score: {row['Score']}"):
                    st.markdown(f"**Why shortlisted:**")
                    st.write(row["Explanation"])
                    
                    st.markdown("---")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write("**Matched Skills:**")
                        st.write(", ".join(row["Details"]["matched_skills"]))
                    with col_b:
                        st.write("**Missing Skills:**")
                        st.write(", ".join(row["Details"]["missing_skills"]))
        else:
            st.info("No resumes processed successfully.")

if __name__ == "__main__":
    main()
