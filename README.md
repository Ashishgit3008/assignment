# Assigment
Assignment to create a csv chatbot


Note:- The script provided is designed to run on free resources. So the LLM, vector store, embedding model etc. used are all open source and are available freely
Here's a step-by-step breakdown of the code for documentation without code snippets:

Necessary libraries are imported to handle logging, web interface (Streamlit), concurrent processing, CSV file loading, embedding generation, and QA capabilities using language models.
Logging is configured to provide real-time monitoring of the application’s behaviour. Logs include timestamps, log levels, and messages, directed to both a log file and the console for easy access.
A simple web interface is created using Streamlit. The application has a main title and a sidebar widget for uploading a CSV file containing customer reviews.
The user uploads a CSV file using the sidebar. The SQL query to add the file into the database and preprocess is kept in a different script 
A function is defined to handle the processing of the CSV file, with caching enabled to prevent redundant processing if the same file is uploaded multiple times.
The uploaded CSV is loaded into a structured format suitable for further processing.
 Logs are used to track the success or failure of the loading process.
Splitting Text Data
     1. The CSV data is split into smaller chunks to facilitate efficient embedding. This step ensures that longer texts are broken down into manageable segments.
     2. The chunk size and overlap between chunks are defined to maintain context.
Embedding Generation**:
     1.  A pre-trained language model is initialized to generate embeddings for the chunks.
     2. Embeddings are created in parallel to improve processing speed, using a multi-threaded approach.
     3. The resulting embeddings are paired with the original text for storage.


     1. The embeddings and text are stored in a vector database for efficient retrieval.
     2. The vector store is saved locally, allowing the application to quickly access the indexed data in future queries.

Initializing the QA System**
  	 1. Once the CSV data is processed, a retrieval-based QA system is set up.

A language model is loaded to handle the QA functionality.
A structured template is defined to guide the language model’s response format, ensuring clear answers based on the context extracted from the CSV data.
QA Chain Configuration:
     1.  A QA chain is initialized, integrating the language model with the vector store. This chain allows the system to retrieve context from the vector database and generate answers based on the user's input.
     2. Error handling is in place to manage any issues during this initialization.



User Interaction for Q&A
  1. A user input field is provided, allowing users to ask questions related to the uploaded customer reviews.
   2. A button triggers the retrieval and answer generation process, using the previously indexed data and the language model to provide a response.
   3. The result is displayed on the interface. If the answer format is unexpected, the user is notified.
Displaying Logs in the Interface
   1. The log file is made accessible through the Streamlit interface, allowing users to review the application’s log entries directly from the sidebar for debugging and monitoring.
Error Handling and Notifications
   	1. Comprehensive error handling is integrated at each step. If an error occurs during data loading, processing, encoding, or QA setup, appropriate error messages are logged and displayed to the user, ensuring the application remains user-friendly and informative.

