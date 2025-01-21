import support

### Screen
resolution = screen_width, screen_height = 1200, 650
screen_half_width = screen_width // 2
screen_half_height = screen_height // 2
fps = 30

### Menu Text
menu_font_size = screen_height // 10

### Cards
card_width_to_screen = 0.075
card_height_to_width = 1.5
card_width = int(card_width_to_screen * screen_width)
card_height = int(card_height_to_width * card_width)

# Proportional to card size
card_suit_center = support.XY(0.18, 0.3)
card_suit_size = 0.13
card_value_center = support.XY(0.18, 0.15)
card_value_size_ratio = 0.2
card_rounded_corner = 0.05
card_back_border = 0.1

# derived sizes
card_back_border_width = int(card_back_border * card_width)
card_rounded_corner_size = int(card_rounded_corner * card_width)
card_value_size = int(card_value_size_ratio * card_height)
card_suit_dimensions = support.XY(int(card_suit_size * card_width), int(card_suit_size * card_height))

### Deck
deck_face_up_shift = 0.5
deck_face_down_shift = 0.05
deck_face_down_draw_card_skip = 3

### Battle
battle_sky_proportion = 0.6
battle_sky_height = int(battle_sky_proportion * screen_height)

### Player
player_deck_margin_ratio = 0.05
player_deck_margin = int(player_deck_margin_ratio * screen_width)
player_hand_size = 3
player_hand_and_draw_deck_buffer_ratio = 0.05
player_hand_and_draw_deck_buffer = int(player_hand_and_draw_deck_buffer_ratio * screen_width)
player_left_draw_deck_left = player_deck_margin
player_right_draw_deck_left = screen_width - player_deck_margin - card_width
player_draw_deck_top = screen_height - player_deck_margin - card_height
player_discard_pile_top = player_deck_margin
player_left_hand_left = player_left_draw_deck_left + card_width + player_hand_and_draw_deck_buffer
# figure out the 2.5 magic 
player_right_hand_left = player_right_draw_deck_left - player_hand_and_draw_deck_buffer - int((1 + deck_face_up_shift * (player_hand_size - 1)) * card_width)

player_hp_size_ratio = 0.1
player_hp_size = int(player_hp_size_ratio * screen_height)
player_hp_rect_center_ratio = support.XY(0.25, 0.35)