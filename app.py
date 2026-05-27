import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


st.set_page_config(page_title="Netflix RAG App", page_icon="🎬")

st.title("Netflix RAG App")
st.write("Ställ en fråga om Netflix-datasetet.")


@st.cache_resource
def build_rag_chain():
    load_dotenv(".env", override=True)

    df = pd.read_csv("data/cleaned_data.csv")

    sweden_df = df[df["country"].str.contains("Sweden", case=False, na=False)]

    other_df = df[
        ~df["country"].str.contains("Sweden", case=False, na=False)
    ].sample(n=30, random_state=42)

    df_rag = pd.concat([sweden_df, other_df]).drop_duplicates().reset_index(drop=True)

    documents = [
        Document(
            page_content=row["rag_text"],
            metadata={
                "title": row["title"],
                "type": row["type"],
                "country": row["country"],
                "release_year": int(row["release_year"])
            }
        )
        for _, row in df_rag.iterrows()
    ]

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="vectorstore"
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    template = """
You are a helpful assistant that answers questions based only on the context below.

Use only the information in the context.
If the answer is not found in the context, say:
"I cannot find that information in the dataset."

Context:
{context}

Question:
{question}

Answer:
"""

    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


try:
    rag_chain = build_rag_chain()

    question = st.text_input(
        "Skriv din fråga här:",
        "Which titles are TV Shows from Sweden?"
    )

    if st.button("Fråga"):
        with st.spinner("Söker i datasetet och skapar svar..."):
            answer = rag_chain.invoke(question)
            st.subheader("Svar")
            st.write(answer)

except Exception as e:
    st.error("Något gick fel.")
    st.write(e)