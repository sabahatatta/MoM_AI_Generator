import os
import re
import openai 
import gradio as gr
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from the environment
api_key = os.getenv("OPENAI_API_KEY")
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")

# Ensure the API key is present
if not api_key:
    raise ValueError("API key not found. Please set OPENAI_API_KEY in your .env file.")

# Set the OpenAI API key
openai.api_key = api_key

def generate_prompt(meeting_description):
    """Creates a structured prompt for generating MOM and Action Items."""
    return (
        f"As a Natural Language Processing expert, please generate a structured summary from the following meeting notes. "
        f"The summary should include both Minutes of Meeting (MOM) and Action Items, adhering to the following guidelines:\n\n"
        f"1. **Concise Output:**\n"
        f"   - Ensure that the total length of the MOM and Action Items is concise and focused on the key points.\n"
        f"   - Provide a brief yet comprehensive summary without unnecessary details or explanations.\n\n"
        f"2. **Minutes of Meeting (MOM):**\n"
        f"   - List only the essential outcomes, decisions, and agreements reached in the meeting.\n"
        f"   - Omit lengthy discussion points and provide only final conclusions or results.\n\n"
        f"3. **Action Items:**\n"
        f"   - Provide specific, actionable tasks that arose from the meeting, clearly outlining responsibilities.\n"
        f"   - Tie each action item directly to the decisions or outcomes noted in the MOM.\n\n"
        f"4. **Additional Details to Include:**\n"
        f"   - **Meeting Title**\n"
        f"   - **Date and Time**\n"
        f"   - **Location / Platform**\n"
        f"   - **Attendees**\n"
        f"   - **Agenda**\n"
        f"   - **Follow-up Meeting Details (if applicable)**\n\n"
        f"The output should begin with 'MOM:' followed by numbered points for each item. "
        f"After MOM, provide 'Action Items:' as a separate list, also with numbered points.\n\n"
        f"Meeting Notes:\n{meeting_description}\n\n"
        f"Generate the MOM and Action Items based on these instructions."
    )

def query_gpt(prompt):
    """Query GPT-4 Turbo using OpenAI's ChatCompletion API."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a machine learning expert."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

def generate_output(meeting_description):
    """Generates MOM with detailed attributes."""
    prompt = generate_prompt(meeting_description)
    output = query_gpt(prompt)

    if output.startswith("Error:"):
        return output  # Display the error if one occurs

    # Return the output formatted as Markdown for better display
    return f"### Extracted MOM and Action Items:\n\n{output.strip()}"

def extract_meeting_details(output):
    """Extract the meeting title and date from the generated MOM output."""
    title = "Meeting Summary"  # Default title if not found
    date = "No Date Provided"  # Default date if not found

    # Split the output into lines for processing
    lines = output.splitlines()

    # Use regex to match "Meeting Title" and "Date/Time" with flexible patterns
    title_pattern = re.compile(r"meeting title\s*:\s*(.*)", re.IGNORECASE)
    date_pattern = re.compile(r"(date\s*(and time)?\s*:\s*(.*))", re.IGNORECASE)

    for line in lines:
        # Check if the line contains the meeting title
        title_match = title_pattern.match(line.strip())
        if title_match:
            title = title_match.group(1).strip()  # Extract and clean the title

        # Check if the line contains the date or date and time
        date_match = date_pattern.match(line.strip())
        if date_match:
            date = date_match.group(3).strip()  # Extract and clean the date/time

    return title, date

def send_email(subject, body, recipient):
    """Send an email using Gmail's SMTP server."""
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = recipient
    msg['Subject'] = subject

    # Attach the body of the email as HTML
    msg.attach(MIMEText(body, 'html'))

    try:
        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(email_address, email_password)  # Login using your credentials
            server.send_message(msg)  # Send the email

        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {str(e)}"

def format_output_as_html(output):
    """Convert the generated MOM and Action Items into HTML for email."""
    # Replace Markdown-style headings and bullet points with HTML tags
    html_output = output.replace("\n", "<br>")  # Line breaks
    html_output = html_output.replace("#", "").replace("*", "")  # Remove symbols if any remain
    return f"<html><body>{html_output}</body></html>"

def send_output_via_email(meeting_description, recipient_email):
    """Generate output and send it via email with formatted subject and body."""
    output = generate_output(meeting_description)
    if output.startswith("Error:"):
        return output  # Return the error if one occurs

    # Extract the meeting title and date from the output
    title, date = extract_meeting_details(output)

    # Create the subject with the meeting title and date
    subject = f"MOM and Action Items: {title} ({date})"

    # Format the output as HTML for the email body
    html_body = format_output_as_html(output)

    # Send the email
    return send_email(subject, html_body, recipient_email)

def enable_generate_button(meeting_description):
    """Check if meeting description is entered and enable/disable the button."""
    if meeting_description.strip():
        return gr.update(interactive=True), ""  # Enable the button and clear warning
    else:
        return gr.update(interactive=False), "Please enter a meeting description to generate MOM and Action Items."

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Automated MOM & Action Items Generator")

    # Step 1: Input meeting description
    meeting_description = gr.Textbox(
        label="Enter Meeting Description", 
        placeholder="Paste your meeting notes here...",
        lines=10
    )

    # Warning message if the meeting description is not entered
    warning_message = gr.Label(value="Please enter meeting description to generate the MoM and Action Items", visible=False)

    # Step 2: Button to generate MOM and action items (initially disabled)
    generate_button = gr.Button("Generate MOM and Action Items", interactive=False)
    output_box = gr.Markdown()  # Use Markdown for nicely formatted output

    # Step 3: Collect email at the end
    recipient_email = gr.Textbox(
        label="Enter Recipient's Email", 
        placeholder="Enter the recipient's email address"
    )
    send_email_button = gr.Button("Send Output via Email")

    # Set up interactions
    meeting_description.change(
        enable_generate_button, 
        inputs=[meeting_description], 
        outputs=[generate_button, warning_message]
    )

    generate_button.click(
        generate_output, 
        inputs=[meeting_description], 
        outputs=[output_box]
    )

    send_email_button.click(
        send_output_via_email, 
        inputs=[meeting_description, recipient_email], 
        outputs=[output_box]
    )

# Launch the interface
demo.launch()
