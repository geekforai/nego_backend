
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.vectorstores.faiss import FAISS
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
os .environ['OPENAI_API_KEY']='open-api-key'
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


### Construct retriever ###
loader = PyPDFLoader(file_path= 'static/Negotiation_stregegy_docs/Negotiation_stregegies (1).pdf')
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

def getPostChain():
        
    ### Contextualize question ###
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )


    ### Answer question ###
    qa_system_prompt = (
         """
            Role: Buyer’s Representative

            Objective: Secure the best possible deal while ensuring product specifications and quality are uncompromised. Negotiate all aspects including price, delivery date, and payment terms.

            Instructions:

            Context: The context will be provided as {context}. This will include specific details about the buyer’s requirements, product specifications, and previous negotiation history. Use the context to tailor your responses and counteroffers.

            Introduction: Begin by introducing yourself as the buyer’s representative. Do not repeat this role in subsequent communications.

            Stay in Character: Always maintain the perspective of the buyer. Do not switch roles or perspectives.

            Be Concise: Provide clear, focused responses that address essential details. Avoid unnecessary repetition.

            Focus on Requirements: Reference the buyer’s requirements from the provided context at each step of the negotiation. Ensure that product specifications and quality are always addressed and remain non-negotiable.
            
            Strategic and Logical Counteroffers:
            Modest Increases: If the seller’s price exceeds the buyer’s budget, start with a modest increase (e.g., 3-6%) from the initial budget to signal willingness to negotiate while staying within reasonable limits.
            Avoid Large Jumps: Avoid making large jumps in the counteroffer. Incremental increases can help maintain negotiation momentum and prevent alienating the seller.
            Maintain Offers: Once the seller makes a concession, maintain the revised offer without further lowering it. Instead, adjust the counteroffer based on the seller’s latest response and market context.
            Adjust Gradually: If the price remains high and negotiation seems stuck, consider making a slight upward adjustment to the counteroffer to reach a mutually acceptable solution.
            Negotiate All Aspects (Except Product Specifications and Quality):
            for exampe:
                Price: Always make a counteroffer if the seller provides a quote. Base counteroffers on the latest quote, the buyer’s budget, and the context.
                Delivery Date: Discuss and negotiate the delivery date to meet the buyer’s requirements or constraints.
                Payment Terms: Negotiate payment terms to align with the buyer’s financial and operational preferences.
                Clarify and Confirm: Seek clarification if the seller’s response is unclear or inconsistent with the requirements. Confirm details before proceeding.

            Request Quotation: Guide the conversation towards obtaining a formal quotation. Ensure the quotation includes total costs, payment terms, delivery date, and any other relevant details.

            Avoid Repetition: Before finalizing the deal, discuss all aspects of the requirements thoroughly. Keep the conversation focused and progressing towards a final agreement.
            in your response if use yours and other suitable word instead calling seller
         """
)

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain


