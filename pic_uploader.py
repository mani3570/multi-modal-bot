import google.generativeai as genai
from dotenv import load_dotenv
import os
import gradio as gr
from PIL import Image
import numpy as np

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def generate_response(text_input, file_input, chat_history=None):
    # Upload the file and print a confirmation.
    if file_input is not None:
        image_pil = Image.fromarray(np.uint8(file_input))
        image_path = "website.jpg"
        image_pil.save(image_path)
        
        sample_file = genai.upload_file(path=image_path,
                                        display_name="website image")
        print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

        file = genai.get_file(name=sample_file.name)
        print(f"Retrieved file '{file.display_name}' as: {file.uri}")
    else:
        sample_file = None
    
    # Choose a Gemini API model.
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    
    # Initialize chat history if None
    if chat_history is None:
        chat_history = []
    
    chat = model.start_chat(history=chat_history)

    # Prompt the model with text and the uploaded image if available
    if sample_file:
        response = chat.send_message([sample_file, text_input])
    else:
        response = chat.send_message(text_input)

    # Append the new message to chat history
    chat_history.append((text_input, response.text))

    return "",None, chat_history

# Create a Gradio interface with Blocks
with gr.Blocks(title="Gemini pro / pro vision") as demo:
    gr.Markdown("# Chat Bot M1N9")

    # Define the Chatbot component
    chatbot = gr.Chatbot([], elem_id="chatbot", height=700, show_share_button=True, show_copy_button=True)

    # Define the Textbox and Image components
    msg = gr.Textbox(show_copy_button=True, placeholder="Type your message here...")
    img = gr.Image()
    btn = gr.Button("Submit")

    # Define the ClearButton component
    clear = gr.ClearButton([msg, img, chatbot])

    # Set the submit function for the Textbox and Image
    # def submit_message(msg, img, chat_history):
    #     response, chat_history = generate_response(msg, img, chat_history)
    #     return "", None, chat_history  # Clear input fields after submission

    msg.submit(generate_response, [msg, img, chatbot], [msg, img, chatbot])
    btn.click(generate_response, [msg, img, chatbot], [msg, img, chatbot])

# Launch the Gradio interface
demo.launch(debug=True, share=True)
