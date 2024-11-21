import pygame
import random
import time
pygame.init()
pygame.mixer.init

game_over_sound = pygame.mixer.Sound("game_over sound.wav")
Food_collection_sound= pygame.mixer.Sound("food colection sound.wav")
box_len = 1500
box_height = 1000
color_1 = (0, 0, 0)  # white (keep as is)
color_2 = (255, 87, 51)  # vibrant red-orange
color_3 = (255, 255, 255)  # white (keep as is)
color_4 = (247, 215, 0)  # bright yellow
color_5 = (40, 180, 99)  # vibrant green
color_6 = (255, 59, 48)  # bright red

add_caption = pygame.display.set_mode((box_len, box_height))
pygame.display.set_caption("SNAKE GAME")

timer = pygame.time.Clock()
snake_block = 10
snake_speed = 15

display_style = pygame.font.SysFont("arial", 30, "bold")
score_font = pygame.font.SysFont("arial", 45, "bold")

def final_score(score):
    value = score_font.render("Enjoy the snake game -------- Your score is: " + str(score), True, color_2)
    add_caption.blit(value, [20, 20])

def make_snake(snake_block, list_snake):
    for x in list_snake:
        pygame.draw.rect(add_caption, color_3, [x[0], x[1], snake_block, snake_block])

def display_msg(msg, color):
    mssg = display_style.render(msg, True, color)
    add_caption.blit(mssg, [box_len / 6, box_height / 3])

def draw_button(text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(add_caption, hover_color, (x, y, width, height))
        if mouse_click[0]:  # Left mouse button clicked
            return True  
    else:
        pygame.draw.rect(add_caption, color, (x, y, width, height))

    
    button_text = display_style.render(text, True, color_1)  # Use a contrasting text color
    text_rect = button_text.get_rect(center=(x + width / 2, y + height / 2))
    add_caption.blit(button_text, text_rect)

    return False

def fade_in_text(text, y, color):
    alpha = 0
    while alpha < 255:
        add_caption.fill(color_1)  # Clear the screen
        menu_text = display_style.render(text, True, color)
        menu_text.set_alpha(alpha)
        add_caption.blit(menu_text, (box_len / 6, y))
        pygame.display.update()
        alpha += 5
        timer.tick(30)

def main_menu():
    fade_amount = 5
    color_value = 0
    increasing = True
    button_width = 300
    button_height = 50

    circles = [{'pos': [random.randint(0, box_len), random.randint(0, box_height)], 'radius': random.randint(20, 50), 'speed': [random.choice([-2, 2]), random.choice([-2, 2])]} for _ in range(10)]

    while True:
        add_caption.fill(color_1)

        for circle in circles:
            circle['pos'][0] += circle['speed'][0]
            circle['pos'][1] += circle['speed'][1]
            if circle['pos'][0] < 0 or circle['pos'][0] > box_len:
                circle['speed'][0] *= -1
            if circle['pos'][1] < 0 or circle['pos'][1] > box_height:
                circle['speed'][1] *= -1
            pygame.draw.circle(add_caption, color_3, circle['pos'], circle['radius'])

        if increasing:
            color_value += fade_amount
            if color_value >= 255:
                color_value = 255
                increasing = False
        else:
            color_value -= fade_amount
            if color_value <= 0:
                color_value = 0
                increasing = True

        animated_color = (color_value, color_value, 255)

        
        if draw_button("Welcome to Snake game", box_len / 6, box_height / 3 - 60, button_width, button_height, color_5, (0, 200, 0)):
            print("Welcome button clicked")
        if draw_button("Press P to Play", box_len / 6, box_height / 3, button_width, button_height, color_2, (200, 100, 0)):
            game_start() 
        if draw_button("Controls", box_len / 6, box_height / 3 + 120, button_width, button_height, color_5, (220, 200, 0)):
            print("movement = wsad or arrowkeys press, p for play/pause menu")
        if draw_button("Press Q to Quit", box_len / 6, box_height / 3 + 60, button_width, button_height, color_4, (200, 200, 0)):
            pygame.quit()
            quit()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_start()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        timer.tick(30)
def spawn_food():
    food_x = round(random.randrange(0, box_len - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, box_height - snake_block) / 10.0) * 10.0
    return food_x, food_y

def draw_food(foodx_pos, foody_pos):
    
    food_color = (color_5)  
    glow_color = (255, 255, 100) 

   
    for radius in range(20, 0, -5):  
        pygame.draw.circle(add_caption, glow_color, (int(foodx_pos + snake_block / 2), int(foody_pos + snake_block / 2)), radius)

    
    pygame.draw.rect(add_caption, food_color, [foodx_pos, foody_pos, snake_block, snake_block])

def move_enemy_chase(enemy_position, player_position):
    # Basic chasing behavior: move towards the player's position
    if enemy_position[0] < player_position[0]:
        enemy_position[0] += snake_block
    elif enemy_position[0] > player_position[0]:
        enemy_position[0] -= snake_block

    if enemy_position[1] < player_position[1]:
        enemy_position[1] += snake_block
    elif enemy_position[1] > player_position[1]:
        enemy_position[1] -= snake_block

    return enemy_position

def draw_button_with_effects(text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(add_caption, hover_color, (x, y, width, height), border_radius=15)
        if mouse_click[0]:  # Left mouse button clicked
            return True  
    else:
        pygame.draw.rect(add_caption, color, (x, y, width, height), border_radius=15)
    
    # Text rendering
    button_text = display_style.render(text, True, color_1)  # Use a contrasting text color
    text_rect = button_text.get_rect(center=(x + width / 2, y + height / 2))
    add_caption.blit(button_text, text_rect)

    return False

def pause_menu():
    paused = True
    while paused:
        add_caption.fill(color_1)  # Clear the screen

        # Add a semi-transparent background effect to make the menu stand out
        overlay = pygame.Surface((box_len, box_height))
        overlay.set_alpha(150)  # 150 out of 255 for transparency
        overlay.fill((0, 0, 0))  # Black overlay
        add_caption.blit(overlay, (0, 0))

        # Draw PAUSED text with more style
        paused_text = display_style.render("PAUSED", True, color_5)
        paused_rect = paused_text.get_rect(center=(box_len / 2, box_height / 4))
        add_caption.blit(paused_text, paused_rect)

        # Draw "Resume" and "Quit" buttons with enhanced styling
        if draw_button_with_effects("Resume", box_len / 6, box_height / 2 - 60, 300, 50, color_2, (255, 140, 0)):
            paused = False  # Unpause the game
        if draw_button_with_effects("Quit", box_len / 6, box_height / 2 + 20, 300, 50, color_4, (255, 255, 0)):
            pygame.quit()
            quit()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # If the user presses P to unpause
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                    
def game_start():
    global snake_speed

    default_snake_speed = 14

    default_enemy_move_delay = 25
    
    boosted_speed = 30       
    is_boosting = False       

    snake_speed = default_snake_speed
    enemy_move_delay = default_enemy_move_delay
    
    game_over = False
    game_close = False

    value_x1 = box_len / 2
    value_y1 = box_height / 2
    new_x1 = 0
    new_y1 = 0

    list_snake = []
    snake_len = 1
    food_collected = 0  # Count of food collected

    foodx_pos, foody_pos = spawn_food()  # Spawn initial food

    enemy_position = None  # Enemy starts as None

    enemy_move_delay = 10  # Delay in frames for enemy movement
    enemy_move_timer = 0  # Timer to keep track of enemy movement delay

    while not game_over:
        while game_close:
            game_over_sound.play()
            add_caption.fill(color_1)
            display_msg("You lost!", color_4)
            final_score(snake_len - 1)

            # Draw buttons for Restart and Quit
            if draw_button("Restart", box_len / 6, box_height / 2 - 40, 200, 50, color_5, (0, 200, 0)):
                game_start()  # Restart the game
            if draw_button("Quit", box_len / 6, box_height / 2 + 20, 200, 50, color_4, (200, 200, 0)):
                pygame.quit()
                quit()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        snake_speed = 10
                        game_start()
                        return

                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and new_x1 == 0:  # Left (A or Arrow Left)
                    new_x1 = -snake_block
                    new_y1 = 0
                elif event.key == pygame.K_d and new_x1 == 0:  # Right (D or Arrow Right)
                    new_x1 = snake_block
                    new_y1 = 0
                elif event.key == pygame.K_w and new_y1 == 0:  # Up (W or Arrow Up)
                    new_y1 = -snake_block
                    new_x1 = 0
                elif event.key == pygame.K_s and new_y1 == 0:  # Down (S or Arrow Down)
                    new_y1 = snake_block
                    new_x1 = 0
                # Arrow key controls
                elif event.key == pygame.K_LEFT and new_x1 == 0:  # Left Arrow
                    new_x1 = -snake_block
                    new_y1 = 0
                elif event.key == pygame.K_RIGHT and new_x1 == 0:  # Right Arrow
                    new_x1 = snake_block
                    new_y1 = 0
                elif event.key == pygame.K_UP and new_y1 == 0:  # Up Arrow
                    new_y1 = -snake_block
                    new_x1 = 0
                elif event.key == pygame.K_DOWN and new_y1 == 0:  # Down Arrow
                    new_y1 = snake_block
                    new_x1 = 0
                elif event.key == pygame.K_p:  # Press P to Pause the game
                    pause_menu()
                elif event.key == pygame.K_SPACE:  # Press space to activate boost
                    is_boosting = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:  # Release space to deactivate boost
                    is_boosting = False

        # Apply boosted speed if boosting, else use default speed
        current_speed = boosted_speed if is_boosting else default_snake_speed

        value_x1 += new_x1
        value_y1 += new_y1

        
        if value_x1 >= box_len or value_x1 < 0 or value_y1 >= box_height or value_y1 < 0:
            game_over_sound.play()
            game_close = True

        # Update enemy position if it exists
        if enemy_position:
            enemy_move_timer += 1  # Increment enemy move timer
            if enemy_move_timer >= enemy_move_delay:
                enemy_position = move_enemy_chase(enemy_position, [value_x1, value_y1])
                enemy_move_timer = 0  # Reset timer after moving enemy

        add_caption.fill(color_1)
        pygame.draw.rect(add_caption, color_5, [foodx_pos, foody_pos, snake_block, snake_block])
        snake_head = [value_x1, value_y1]
        list_snake.append(snake_head)

        if len(list_snake) > snake_len:
            del list_snake[0]

        for x in list_snake[:-1]:
            if x == snake_head:
                game_close = True

        make_snake(snake_block, list_snake)
        final_score(snake_len - 1)

        # Check if snake collects food
        if value_x1 == foodx_pos and value_y1 == foody_pos:
            foodx_pos, foody_pos = spawn_food()
            snake_len += 1  
            food_collected += 1 
            Food_collection_sound.play()
            snake_speed += 2

            if food_collected == 5:
                enemy_position = [random.randrange(0, box_len, snake_block), random.randrange(0, box_height, snake_block)]


        if enemy_position:
            pygame.draw.rect(add_caption, color_6, [enemy_position[0], enemy_position[1], snake_block, snake_block])
            # Check for collision with enemy
            if snake_head == enemy_position:
                game_close = True

        pygame.display.update()
        timer.tick(snake_speed)

main_menu()
