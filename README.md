# QuizBot

QuizBot is an interactive quiz bot that automates the process of extracting questions and options from images/screenshots and uses OpenAI's GPT models to predict the correct answers. It's designed to assist in quickly obtaining answers for quiz questions presented in a visual format.

## Features

- Screenshot capture of quiz questions and options
- OCR (Optical Character Recognition) to extract text from images
- Integration with OpenAI's GPT models for generating answers
- Simple and intuitive GUI for easy interaction

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or later
- pip for installing dependencies

## Installation

To install QuizbBot, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/yourusername/kvizbot.git
cd quizbot
```

2. Install the required python packages:

```bash
pip install -r requirements.txt
```

## Setup

Before using the application, you must obtain an API key from OpenAI and set it up for use with the app.

1. Obtain an API key from OpenAI.
2. Place the API key in a file named .env in the root directory of the project, with the following content: (alternatively, you can hardcode your API key)

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

3. Ensure pytesseract is correctly set up for OCR. You might need to install Tesseract OCR and set the path to the executable in your environment variables or within utils.py.

You can modify prompt text in take_screenshot function so that it mathces your language for better accuracy.

## Usage

```bash
python src/main.py
```

Once the application is running, follow these steps to use it:

1. Click on the "Question" button to select the screen region containing the quiz question.
2. Use the "Option 1", "Option 2", etc., buttons to select the regions for each of the possible answers.
3. After selecting the question and answer options, click on "Show answer" to capture, process, and display the generated answer based on the question and options provided. Only repeat this step once you have setup "Question" and "Options" regions.

![Show answer demonstration](https://github.com/matejaaj/quizbot/assets/117997165/1db6a4ae-0767-4371-b9d7-1c3fb77a1837)
![Select area demonstration](https://github.com/matejaaj/quizbot/assets/117997165/5733b314-f777-4201-a62e-6e6f9a92d1ab)

## Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, feel free to fork the repository, make changes, and submit a pull request.

