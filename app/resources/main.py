import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    # App title and description
    st.title("📧 Cold Mail Generator")
    st.markdown(
        """
        **Generate professional cold emails instantly!**  
        Enter the URL of a company's career page, and we'll do the rest—extract job details and generate customized cold emails for your applications.
        """
    )

    # Sidebar for navigation and user instructions
    with st.sidebar:
        st.header("📌 Instructions")
        st.markdown(
            """
            1. Paste the URL of the company's career page in the input field.
            2. Click **Submit** to generate tailored cold emails.
            3. Copy the generated email and use it for your application!
            """
        )
        st.info("🔗 Ensure the URL links directly to the job description or career page.")

    # Main input and processing section
    with st.container():
        st.subheader("Step 1: Provide the Career Page URL")
        url_input = st.text_input(
            "Enter a URL:", 
            value="https://jobs.nike.com/job/R-33460", 
            help="Paste the link to the job description or company career page."
        )

        submit_button = st.button("Generate Cold Email 🚀", help="Click to start the process.")

    # Display the results or handle errors
    if submit_button:
        with st.spinner("Generating your cold email... Please wait!"):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                st.success("✅ Job details extracted successfully!")
                st.subheader("Generated Cold Emails")

                for idx, job in enumerate(jobs, 1):
                    st.markdown(f"### Job {idx}")
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.code(email, language='markdown')
                    st.markdown("---")
            except Exception as e:
                st.error(f"An Error Occurred: {e}")

    # Footer with branding
    st.markdown("---")
    st.markdown(
        """
        🛠️ Developed with ❤️ using **Streamlit** and **LangChain**  
        ✉️ Powered by AI to simplify your job applications!
        """
    )

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
