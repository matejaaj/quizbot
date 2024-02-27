import tkinter as tk
from PIL import ImageGrab
from utils import process_region, process_image, get_completion, load_api_key
from openai import OpenAI

class QuizBotApp:
    def __init__(self, root):
        """
        Initializes the QuizBotApp instance with a root window and sets up the UI components.
        
        Parameters:
        - root: A tk.Tk() instance that serves as the main window for the application.
        """
        self.root = root
        self.start_x, self.start_y, self.temp_region, self.current_selection = 0, 0, None, 0
        self.regions = {i: None for i in range(1, 6)}  # Dictionary to store the coordinates of selected regions
        self.client = OpenAI()  # Initialize the OpenAI client
        self.client.api_key = load_api_key()  # Load and set the OpenAI API key
        self.setup_ui()  # Setup the user interface

    def on_button_press(self, event):
        """
        Records the starting coordinates of a region selection when the mouse button is pressed.
        
        Parameters:
        - event: The event object containing details of the mouse button press.
        """
        self.start_x, self.start_y = self.root.winfo_pointerx(), self.root.winfo_pointery()

    def on_drag(self, event):
        """
        Updates the temporary region coordinates as the mouse is dragged, indicating the selection area.
        
        Parameters:
        - event: The event object containing details of the mouse movement.
        """
        end_x, end_y = self.root.winfo_pointerx(), self.root.winfo_pointery()
        self.temp_region = (self.start_x, self.start_y, end_x, end_y)

    def on_button_release(self, event):
        """
        Finalizes the region selection when the mouse button is released, and closes the selection window.
        
        Parameters:
        - event: The event object containing details of the mouse button release.
        """
        self.regions[self.current_selection] = self.temp_region
        self.close_selection_window()
        self.display_text("Region set.\n")

    def close_selection_window(self):
        """
        Closes the selection window used for region selection.
        """
        self.selection_window.quit()
        self.selection_window.destroy()

    def select_window(self, selection_number):
        """
        Initiates the region selection process for a specified selection number.
        
        Parameters:
        - selection_number: An integer indicating the selection number (e.g., 1 for question, 2-5 for options).
        """
        self.current_selection = selection_number
        selection_type = "Question" if selection_number == 1 else f"Option {selection_number-1}"
        self.display_text(f"Selecting {selection_type}...\nPlease select the region on the screen.\n")
        self.create_selection_window()

    def create_selection_window(self):
        """
        Creates a transparent, full-screen window for easy region selection.
        """
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes("-alpha", 0.3)  # Make window transparent
        self.selection_window.attributes("-fullscreen", True)  # Fullscreen for easy region selection
        # Bind mouse events to handlers
        self.selection_window.bind("<ButtonPress-1>", self.on_button_press)
        self.selection_window.bind("<B1-Motion>", self.on_drag)
        self.selection_window.bind("<ButtonRelease-1>", self.on_button_release)
        self.selection_window.mainloop()

    def display_text(self, text):
        """
        Displays text in the text display area of the application.
        
        Parameters:
        - text: The string to be displayed.
        """
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert(tk.END, text)

    def take_screenshots(self):
        """
        Captures screenshots of the selected regions, performs OCR to extract text, and uses OpenAI to generate answers.
        """
        ocr_results = []
        for region in self.regions.values():
            if region:
                try:
                    x1, y1, x2, y2 = process_region(region)  # Process the region to get correct coordinates
                    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))  # Capture screenshot of the region
                    ocr_results.append(process_image(screenshot))  # Perform OCR on the screenshot
                except Exception as e:
                    self.display_text(f"Error taking screenshot: {e}\n")
                    return
        # Prepare the prompt for OpenAI based on the OCR results
        prompt = "Question: " + "\n" + "\n".join(ocr_results) + "\nOnly write correct asnwer."
        answer = get_completion(prompt, self.client)  # Get the answer from OpenAI
        self.display_text(answer)  # Display the answer

    # UI setup methods: setup_ui, setup_question_button, setup_option_buttons, setup_screenshot_button, setup_text_display
    # These methods create and configure UI components like buttons and text display area.
    def setup_ui(self):
        """
        Sets up the user interface for the application, including buttons and a text display area.
        """
        self.setup_question_button()
        self.setup_option_buttons()
        self.setup_screenshot_button()
        self.setup_text_display()

    def setup_question_button(self):
        """
        Creates and places the button for selecting the question area.
        """
        question_button = tk.Button(self.root, text="Question", command=lambda: self.select_window(1))
        question_button.grid(row=0, column=0, columnspan=2)
    
    def setup_option_buttons(self):
        """
        Creates and places buttons for selecting the option areas for answers.
        """
        for i in range(2, 6):
            button_text = f"Option {i-1}"
            row = 1 if i < 4 else 2  # First two options on the second row, next two on the third
            column = 0 if i % 2 == 0 else 1  # Alternating columns for each button
            # Use a lambda function to ensure the correct value of i is used when the button is pressed
            select_button = tk.Button(self.root, text=button_text, command=lambda i=i: self.select_window(i))
            select_button.grid(row=row, column=column, padx=5)
    
    def setup_screenshot_button(self):
        """
        Creates and places a button to initiate the screenshot process and display the answer.
        """
        screenshot_button = tk.Button(self.root, text="Show answer", command=self.take_screenshots)
        screenshot_button.grid(row=3, column=0, columnspan=2)
    
    def setup_text_display(self):
        """
        Creates and places a text field for displaying information or answers.
        """
        self.text_display = tk.Text(self.root, height=10, width=50)
        self.text_display.grid(row=4, column=0, columnspan=2)