from telebot import TeleBot, types
import pandas as pd
import random
from movies.send_defaults import send_category  # Importing the function from send_defaults

bot = TeleBot("") #your token

# Load the dataset
data = pd.read_csv("movies_metadata.csv")

start_text = "🎉 Welcome to CineMateBot! 🎬\nIf you want movie suggestions, just press /suggest to get personalized recommendations!"

main_categories = [
    'Animation 🎨', 'Comedy 😂', 'Family 👨‍👩‍👧‍👦', 'Adventure 🌍', 'Fantasy 🧚‍♂️', 'Romance ❤️',
    'Drama 🎭', 'Action ⚔️', 'Crime 🕵️‍♂️', 'Thriller 😱', 'Horror 👻', 'History 📜',
    'Science Fiction 🚀', 'Mystery 🔍', 'War ⚔️', 'Foreign 🌏', 'Music 🎶', 'Documentary 📽️',
    'Western 🤠', 'TV Movie 📺'
]

@bot.message_handler(commands=['start', 'suggest'])
def send_welcome(message):
    user_id = message.from_user.id
    if message.text == "/start":
        bot.send_message(message.chat.id, start_text)
    elif message.text == "/suggest":
        send_category(bot, user_id)  # Call send_category function from send_defaults.py

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    genre_with_emoji = call.data
    # Split the emoji from the genre name
    genre = genre_with_emoji.rsplit(' ', 1)[0]  # Get the genre without the emoji

    # Filter movies by the selected genre
    filtered_movies = data[data['genres'].str.contains(genre, na=False)]

    if not filtered_movies.empty:
        # Select a random movie from the filtered list
        random_movie = filtered_movies.sample()
        original_title = random_movie['original_title'].values[0]
        overview = random_movie['overview'].values[0]

        # Send the movie details back to the user
        bot.send_message(call.message.chat.id, f"🎬 Movie: {original_title}\n\n\n📝 Overview: {overview}")
    else:
        bot.send_message(call.message.chat.id, "No movies found for this genre. Please try another category.")

    bot.delete_message(call.message.chat.id, call.message.message_id)

bot.infinity_polling()
