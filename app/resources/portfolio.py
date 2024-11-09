import pandas as pd
import chromadb
import uuid
import os


class Portfolio:
    def __init__(self, file_path="D:\Coldmail_Generator\my_portfolio.csv"):
        self.file_path = file_path
        
        # Check if the file exists before loading
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"CSV file not found at: {self.file_path}")

        self.data = pd.read_csv(file_path)

        # Validate required columns
        required_columns = ['Techstack', 'Links']
        for column in required_columns:
            if column not in self.data.columns:
                raise ValueError(f"Required column '{column}' is missing in the CSV file.")

        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        # Only load data if the collection is empty
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        # Query the collection for relevant links based on skills
        results = self.collection.query(query_texts=skills, n_results=2)
        return results.get('metadatas', [])  # Return metadata (links)


if __name__ == "__main__":
    try:
        # Initialize and load portfolio
        portfolio = Portfolio("app/resource/my_portfolio.csv")
        portfolio.load_portfolio()

        # Example query for links based on skills
        skills = "Python, Machine Learning"
        links = portfolio.query_links(skills)
        print("Matching Links:", links)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
