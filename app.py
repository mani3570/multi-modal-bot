import google.generativeai as genai
from dotenv import load_dotenv
import os
import gradio as gr
from PIL import Image
import numpy as np

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def save_image(file_input, image_name):
    # Convert the input to a PIL image
    image_pil = Image.fromarray(np.uint8(file_input))
    
    # Define the directory where the image will be saved
    save_directory = "images"
    
    # Check if the directory exists, create it if not
    if not os.path.exists(save_directory):
        os.makedirs(save_directory, exist_ok=True)
    
    # Define the full path to save the image
    image_path = os.path.join(save_directory, image_name)
    
    # Save the image
    image_pil.save(image_path)

    return image_path

def generate_response(text_input, file_inputs=None, chat_history=None):
    # Upload the files (images) and print a confirmation.
    image_paths = []
    if file_inputs is not None:
        for idx, file_input in enumerate(file_inputs):
            image_name = f"image_{idx + 1}.jpg"
            image_path = save_image(file_input, image_name)
            image_paths.append(image_path)

    # Choose a Gemini API model.
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Initialize chat history if None
    if chat_history is None:
        chat_history = []

    # Convert chat history into the required format for Gemini API
    chat_history_content = []
    for user_message, bot_response in chat_history:
        chat_history_content.append({"role": "user", "parts": [{"text": user_message}]})
        chat_history_content.append({"role": "model", "parts": [{"text": bot_response}]})

    chat = model.start_chat(history=chat_history_content)

    # Open images and pass them with text_input if available
    images = [Image.open(image_path) for image_path in image_paths] if image_paths else None

    # Prompt the model with text and the uploaded images if available
    if images:
        response = chat.send_message([*images, text_input])
    else:
        response = chat.send_message(text_input)

    # Append the new message to chat history in Gradio format (user, bot)
    chat_history.append((text_input, response.text))

    return "", chat_history

# Create a Gradio interface with Blocks
with gr.Blocks(title="Gemini vision") as demo:
    gr.Markdown("# Chat Bot M1N9")

    # Define the Chatbot component
    chatbot = gr.Chatbot([], elem_id="chatbot", height=700, show_share_button=True, show_copy_button=True)

    # Define the Textbox and Image components
    msg = gr.Textbox(show_copy_button=True, placeholder="Type your message here...")

    # Row for multiple image inputs
    with gr.Row():
        img1 = gr.Image()
        img2 = gr.Image()
        img3 = gr.Image()
        img4 = gr.Image()
    
    btn = gr.Button("Submit")

    # Define the ClearButton component
    clear = gr.ClearButton([msg, img1, img2, img3, img4, chatbot])

    # Set the submit function for the Textbox and Image
    def submit_message(msg, img1, img2, img3, img4, chat_history):
        # Collect all images into a list
        image_list = [img1, img2, img3, img4]
        # Filter out None values in case fewer than 4 images are uploaded
        image_list = [img for img in image_list if img is not None]
        
        # Call the generate_response with the list of images
        response, chat_history = generate_response(msg, image_list, chat_history)
        
        # Return the updated chat history and clear input fields
        return "", None, None, None, None, chat_history

    # Bind the submit function to both the submit action of Textbox and the button click
    msg.submit(submit_message, [msg, img1, img2, img3, img4, chatbot], [msg, img1, img2, img3, img4, chatbot])
    btn.click(submit_message, [msg, img1, img2, img3, img4, chatbot], [msg, img1, img2, img3, img4, chatbot])

# Launch the Gradio interface
demo.launch(debug=True, share=True)
