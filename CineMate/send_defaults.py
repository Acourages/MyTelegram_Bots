import pandas as pd
import ast
from telebot import TeleBot, types

# Load the dataset
data = pd.read_csv("movies_metadata.csv")

# Function to extract genre names from the 'genres' column in the dataset
def extract_genres(genres_str):
    genres_list = ast.literal_eval(genres_str)  # Safely evaluate string to Python object
    return [genre['name'] for genre in genres_list]  # Extract genre names

# Apply the function to the 'genres' column and flatten the list
all_genres = data['genres'].apply(extract_genres).explode()

main_categories = [
    'Animation 🎨', 'Comedy 😂', 'Family 👨‍👩‍👧‍👦', 'Adventure 🌍', 'Fantasy 🧚‍♂️', 'Romance ❤️',
    'Drama 🎭', 'Action ⚔️', 'Crime 🕵️‍♂️', 'Thriller 😱', 'Horror 👻', 'History 📜',
    'Science Fiction 🚀', 'Mystery 🔍', 'War ⚔️', 'Foreign 🌏', 'Music 🎶', 'Documentary 📽️',
    'Western 🤠', 'TV Movie 📺'
]

text = "🎬 Choose a Movie Category: 🎬\nPlease select a genre from the options below to find your perfect movie! 🍿✨\nJust click on your preferred category!"

# Function to send the inline keyboard with genre options to the user
def send_category(bot, user_id):
    keyboard = types.InlineKeyboardMarkup()
    # Create buttons for each genre in main_categories
    buttons = [
        types.InlineKeyboardButton(genre, callback_data=genre) for genre in main_categories
    ]
    # Add buttons in rows of 3
    for i in range(0, len(buttons), 3):
        keyboard.add(*buttons[i:i+3])
    
    bot.send_message(user_id, text, reply_markup=keyboard)
