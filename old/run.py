
import pygame
from class_data import Class
import telebot
import threading
from collections import deque
from queue import Queue

# Telegram Bot Token
TOKEN = '7471389599:AAHs5JDdVqWIYgMQkLqNkUTwgGQO2IuCOnc'
bot = telebot.TeleBot(TOKEN)

# Initialize the student selector table
lecture3 = Class("lecture_list.csv")
selected_queue = deque(maxlen=10)  # Store up to 5 selected students

# Queue for communicating between Telegram thread and Pygame thread
message_queue = Queue()

def flash_result_in_pygame():
    pygame.init()
    screen = pygame.display.set_mode((1200, 900))
    pygame.display.set_caption("Student Selector")

    # Bold font for better visibility
    font = pygame.font.SysFont(None, 36, bold=True)
    running = True
    clock = pygame.time.Clock()
    selected_student = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check if a new selected student is available in the queue
        if not message_queue.empty():
            selected_student = message_queue.get()

            # Add the selected student to the queue of past selections
            selected_queue.appendleft(selected_student)

        screen.fill((0, 0, 0))  # Clear screen with black

        # Calculate maximum weight for normalization
        max_weight = lecture3.data['Weights'].max()

        # Display the student table with colored blocks
        y_offset = 50
        for index, row in lecture3.data.iterrows():
            name = row['Name']
            talk_count = row['Talk Count']
            weight = row['Weights']

            # Normalize weight to a range of 0 to 255 for color intensity
            normalized_weight = int((weight / max_weight) * 255)
            background_color = (normalized_weight, 255 - normalized_weight, 0)  # Red for high weight, green for low

            # Create a rectangle for the background block
            block_rect = pygame.Rect(50, y_offset, 700, 40)
            pygame.draw.rect(screen, background_color, block_rect)

            # Highlight the selected student with a thicker border
            if name == selected_student:
                pygame.draw.rect(screen, (255, 255, 255), block_rect, 4)  # White border for the selected student

            # Render the student's data as bold text
            text = font.render(f"{name}: {talk_count} talks (Weight: {weight:.2f})", True, (0, 0, 0))
            screen.blit(text, (60, y_offset + 5))  # Add padding inside the block
            y_offset += 50
        
        # Side panel showing the queue of selected students
        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(800, 50, 350, 500))  # Draw panel background
        side_panel_text = font.render("Selection History", True, (255, 255, 255))
        screen.blit(side_panel_text, (850, 60))

        y_queue_offset = 120  # Starting point for the queue under the heading
        for idx, student in enumerate(selected_queue):
            queue_text = font.render(f"{idx + 1}. {student}", True, (255, 255, 0))  # Yellow for selected names
            screen.blit(queue_text, (850, y_queue_offset))
            y_queue_offset += 40 
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Telegram handler for any incoming message
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Select a student when a message is received
    selected_student = lecture3.choose_random()

    # Send the selected student's name back to the user
    bot.send_message(message.chat.id, f"Selected student: {selected_student}")

    # Put the selected student in the queue for Pygame to process
    message_queue.put(selected_student)

# Function to run the Telegram bot in a separate thread
def run_telegram_bot():
    bot.polling()

# Start the Telegram bot in a separate thread
telegram_thread = threading.Thread(target=run_telegram_bot)
telegram_thread.start()

# Run the Pygame display on the main thread
flash_result_in_pygame()


