import logging
from concurrent.futures import ThreadPoolExecutor
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.document_loaders.csv_loader import CSVLoader
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("data_pipeline.log"), logging.StreamHandler()]
)


st.title("Chat with Customer Reviews CSV")
st.sidebar.header("Upload CSV")


uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    @st.cache_data
    def process_csv(file):
   
        logging.info("Loading CSV data...")
        try:
            loader = CSVLoader(file_path=file)
            data = loader.load()
            logging.info(f"Loaded {len(data)} records from the CSV file.")
        except Exception as e:
            logging.error(f"Error loading CSV data: {e}")
            st.error(f"Error loading CSV data: {e}")
            return None


        logging.info("Splitting documents...")
        splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
        try:
            chunked_data = splitter.split_documents(data)
            logging.info(f"Split data into {len(chunked_data)} chunks.")
        except Exception as e:
            logging.error(f"Error splitting documents: {e}")
            st.error(f"Error splitting documents: {e}")
            return None

        # Embedding setup
        embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        # Parallel encoding
        def encode_document(doc):
            return embedding_model.encode(doc.page_content)

        with ThreadPoolExecutor() as executor:
            logging.info("Encoding documents in parallel...")
            try:
                embeddings = list(executor.map(encode_document, chunked_data))
                texts = [doc.page_content for doc in chunked_data]
                text_embeddings = list(zip(texts, embeddings))
                logging.info("Documents encoded successfully.")
            except Exception as e:
                logging.error(f"Error during encoding: {e}")
                st.error(f"Error during encoding: {e}")
                return None

        # Store embeddings in FAISS VectorStore
        try:
            logging.info("Storing embeddings in FAISS VectorStore...")
            vector_store = FAISS.from_embeddings(
                text_embeddings=text_embeddings,
                embedding=embedding_model 
            )
            vector_store.save_local("customer_reviews_index_minilm")
            logging.info("FAISS VectorStore saved successfully.")
        except Exception as e:
            logging.error(f"Error storing embeddings in FAISS: {e}")
            st.error(f"Error storing embeddings in FAISS: {e}")
            return None

        return vector_store

    # Process the uploaded CSV file
    vector_store = process_csv(uploaded_file)

    if vector_store:
        llm = ChatOllama(model="llama3.2:latest")

        prompt_template = PromptTemplate(
            input_variables=["context", "question"], 
            template="Given this context: {context}\n\nQuestion: {question}\n\nAnswer:"
        )

        try:
            logging.info("Initializing QA Chain...")
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vector_store.as_retriever(),
                return_source_documents=True,
                chain_type_kwargs={
                    "prompt": prompt_template
                }
            )
            logging.info("QA Chain initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing QA Chain: {e}")
            st.error(f"Error initializing QA Chain: {e}")
            qa_chain = None

        if qa_chain:
            st.header("Ask a Question About the Reviews")
            user_question = st.text_input("Enter your question:")

            if st.button("Get Answer") and user_question:
                try:
                    result = qa_chain.invoke({"query": user_question})
                    if isinstance(result, dict):
                        answer = result.get('answer', 'No answer found')
                        st.success(f"Answer: {answer}")
                    else:
                        st.warning("No valid answer format received.")
                except Exception as e:
                    logging.error(f"Error during QA Chain invocation: {e}")
                    st.error(f"Error during QA Chain invocation: {e}")

        with open("data_pipeline.log", "r") as log_file:
            st.sidebar.text_area("Logs", log_file.read(), height=400)
    else:
        st.error("Failed to process the CSV file.")
else:
    st.info("Please upload a CSV file to get started.")
