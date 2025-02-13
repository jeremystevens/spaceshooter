import math


import pyxel

class SpaceShooter:
    def __init__(self):
        pyxel.init(160, 120, title="Space Shooter")

        # Initialize high scores with initials
        self.high_scores = [
            {"score": 1000, "initials": "AAA"},
            {"score": 750, "initials": "BBB"},
            {"score": 500, "initials": "CCC"},
            {"score": 250, "initials": "DDD"},
            {"score": 100, "initials": "EEE"}
        ]

        # Power-up types
        self.POWERUP_SPREAD = 0
        self.POWERUP_SPEED = 1
        self.POWERUP_PARTNER = 2

        # Power-up state
        self.current_powerup = None
        self.powerup_timer = 0
        self.partner_active = False
        self.partner_offset = {"x": 0, "y": -15}  # Position partner above player
        self.move_speed = 2
        self.shot_pattern = "normal"

        # Power-ups array
        self.powerups = []

        # Enemy sprite data
        # Scout (small, fast)
        pyxel.images[0].set(16, 0, [
            "0002222000",
            "0022222200",
            "0222222220",
            "2222222222"
        ])

        # Destroyer (larger, powerful)
        pyxel.images[0].set(16, 8, [
            "0033333300",
            "0333333330",
            "3333333333",
            "3333333333",
            "0333333330",
            "0033333300"
        ])

        # Cruiser (medium, wave pattern)
        pyxel.images[0].set(16, 16, [
            "0004444000",
            "0444444440",
            "4444444444",
            "0444444440",
            "0004444000"
        ])

        # Battleship (large, shoots multiple bullets)
        pyxel.images[0].set(16, 24, [
            "0055555550",
            "0555555555",
            "5555555555",
            "5555555555",
            "0555555555",
            "0055555550"
        ])

        # Drone (small, erratic movement)
        pyxel.images[0].set(16, 32, [
            "0006660000",
            "0066666000",
            "0666666600",
            "0066666000",
            "0006660000"
        ])

        # Bomber (drops projectiles)
        pyxel.images[0].set(16, 40, [
            "0007777000",
            "0777777770",
            "7777777777",
            "0777777770",
            "0007777000"
        ])

        # Tank (slow, tough)
        pyxel.images[0].set(16, 48, [
            "0088888800",
            "8888888888",
            "8888888888",
            "8888888888",
            "0088888800"
        ])

        # Level 1 Boss
        pyxel.images[0].set(48, 0, [
            "00000999999900000",
            "00099999999999000",
            "00999999999999900",
            "09999999999999990",
            "99999999999999999",
            "99999999999999999",
            "99999999999999999",
            "09999999999999990",
            "00999999999999900",
            "00099999999999000",
            "00000999999900000"
        ])

        # Power-up sprites
        pyxel.images[0].set(32, 0, [
            "0009990000",
            "0099999000",
            "9999999990",
            "0099999000",
            "0009990000"
        ])

        # Create spaceship sprite
        pyxel.images[0].set(0, 0, [
            "0000088888000000",
            "0000888888880000",
            "0088888888888800",
            "0088888888888800",
            "8888888888888888",
            "8888888888888888",
            "0088888888888800",
            "0088888888888800",
            "0000888888880000",
            "0000088888000000"
        ])

        self.game_state = "TITLE"  # TITLE, GAME, HIGHSCORE, SETTINGS
        self.player_x = 20
        self.player_y = 60
        self.player_lives = 3
        self.score = 0
        self.boss_trigger_score = 350  # Score needed to trigger first boss
        self.current_level = 1
        self.level_text_timer = 120  # Show level text for 2 seconds
        self.level_complete_timer = 0
        self.game_speed_multiplier = 1.0
        self.high_scores = [
            {"score": 1000, "initials": "AAA"},
            {"score": 750, "initials": "BBB"},
            {"score": 500, "initials": "CCC"},
            {"score": 250, "initials": "DDD"},
            {"score": 100, "initials": "EEE"}
        ]
        self.sound_enabled = True
        self.difficulty = "NORMAL"  # EASY, NORMAL, HARD
        self.settings_selection = 0  # 0: Sound, 1: Difficulty
        self.player_bullets = []
        self.scroll_x = 0
        self.stars = [(pyxel.rndi(0, 160), pyxel.rndi(0, 120)) for _ in range(30)]
        self.enemies = []
        self.enemy_bullets = []
        self.explosions = []
        self.enemy_spawn_timer = 0
        self.selected_button = 0  # 0: Start, 1: Scores, 2: Config
        self.boss = None #Added boss variable

        # Create sounds
        # Background music
        pyxel.sounds[0].set(
            "e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr" "c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
            "s", "6", "nnff", 25)

        # Player shoot sound
        pyxel.sounds[1].set("a3", "n", "7", "s", 5)

        # Enemy shoot sound
        pyxel.sounds[2].set("c2", "n", "7", "n", 5)

        # Explosion sound
        pyxel.sounds[3].set("f2d2c2", "n", "7", "nf", 10)

        # Boss battle music
        pyxel.sounds[4].set(
            "f3f3c3g2 a2a2c3f3 e3e3e3a3 a3a3rr" "d3d3b2f2 f2f2b2d3 c3c3c3f3 f3f3rr",
            "s", "6", "nnff", 30)

        # Victory tune
        pyxel.sounds[5].set("c3e3g3c4g3c4e4g4", "s", "7", "nnnn", 10)

        # Level 1 music
        pyxel.sounds[6].set(
            "e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr" "c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
            "p", "6", "nnff", 25)

        # Level 2 music
        pyxel.sounds[7].set(
            "a2a2f2c2 c2c2f2a2 g2g2g2c3 c3c3rr" "f2f2d2a1 a1a1d2f2 e2e2e2a2 a2a2rr",
            "t", "7", "nnsf", 20)

        # Level 3 music 
        pyxel.sounds[8].set(
            "d3d3b2f2 f2f2b2d3 c3c3c3f3 f3f3rr" "b2b2g2d2 d2d2g2b2 a2a2a2d3 d3d3rr",
            "s", "7", "fnff", 30)

        # Game over music (sad and dreary)
        pyxel.sounds[9].set(
            "e2c2a1f1 f1f1a1c2 g1g1g1c2 c2c2rr",
            "t", "4", "nnff", 15)

        # Start playing the background music
        pyxel.play(0, 6, loop=True)  # Start with level 1 music

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.game_state == "TITLE":
            # Button navigation
            if pyxel.btnp(pyxel.KEY_UP):
                self.selected_button = (self.selected_button - 1) % 3
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.selected_button = (self.selected_button + 1) % 3

            # Button selection
            if pyxel.btnp(pyxel.KEY_RETURN):
                if self.selected_button == 0:
                    self.game_state = "GAME"
                elif self.selected_button == 1:
                    self.game_state = "HIGHSCORE"
                elif self.selected_button == 2:
                    self.game_state = "SETTINGS"

        elif self.game_state == "GAME":
            self.update_game()
        elif self.game_state == "GAME_OVER":
            if self.is_high_score:
                if pyxel.btnp(pyxel.KEY_UP):
                    current = ord(self.initials[self.initial_index])
                    self.initials[self.initial_index] = chr((current - 65 + 1) % 26 + 65)
                if pyxel.btnp(pyxel.KEY_DOWN):
                    current = ord(self.initials[self.initial_index])
                    self.initials[self.initial_index] = chr((current - 65 - 1) % 26 + 65)
                if pyxel.btnp(pyxel.KEY_RIGHT):
                    self.initial_index = (self.initial_index + 1) % 3
                if pyxel.btnp(pyxel.KEY_LEFT):
                    self.initial_index = (self.initial_index - 1) % 3
                if pyxel.btnp(pyxel.KEY_RETURN):
                    initials_str = "".join(self.initials)
                    new_score = {"score": self.score, "initials": initials_str}
                    self.high_scores.append(new_score)
                    self.high_scores.sort(key=lambda x: x["score"], reverse=True)
                    self.high_scores = self.high_scores[:5]

            if pyxel.btnp(pyxel.KEY_SPACE):  # Play Again
                self.reset_game()
            elif pyxel.btnp(pyxel.KEY_ESCAPE):  # Back to Title
                self.game_state = "TITLE"
                self.reset_game()

        elif self.game_state == "SETTINGS":
            if pyxel.btnp(pyxel.KEY_UP):
                self.settings_selection = (self.settings_selection - 1) % 2
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.settings_selection = (self.settings_selection + 1) % 2
            if pyxel.btnp(pyxel.KEY_RETURN):
                if self.settings_selection == 0:
                    self.sound_enabled = not self.sound_enabled
                    if not self.sound_enabled:
                        pyxel.stop()
                    else:
                        pyxel.play(0, 0, loop=True)
                elif self.settings_selection == 1:
                    difficulties = ["EASY", "NORMAL", "HARD"]
                    current_idx = difficulties.index(self.difficulty)
                    self.difficulty = difficulties[(current_idx + 1) % 3]

    def spawn_enemy(self):
        enemy_type = pyxel.rndi(0, 6)
        y = pyxel.rndi(10, 110)
        if enemy_type == 0:  # Scout (fast, straight movement)
            self.enemies.append({
                "type": 0, 
                "x": 160, 
                "y": y, 
                "dx": -2, 
                "dy": 0,
                "health": 1,
                "shoot_delay": 45
            })
        elif enemy_type == 1:  # Destroyer (zigzag with burst fire)
            self.enemies.append({
                "type": 1, 
                "x": 160, 
                "y": y, 
                "dx": -1, 
                "dy": 1.5, 
                "move_counter": 0,
                "health": 3,
                "burst_counter": 0,
                "shoot_delay": 30
            })
        elif enemy_type == 2:  # Cruiser (sine wave with spread shot)
            self.enemies.append({
                "type": 2, 
                "x": 160, 
                "y": y, 
                "dx": -1.5, 
                "angle": 0,
                "health": 2,
                "shoot_delay": 60
            })
        elif enemy_type == 3:  # Battleship (slow, powerful)
            self.enemies.append({
                "type": 3, 
                "x": 160, 
                "y": y, 
                "dx": -0.5,
                "health": 4,
                "shoot_delay": 90
            })
        elif enemy_type == 4:  # Drone (erratic movement)
            self.enemies.append({
                "type": 4, 
                "x": 160, 
                "y": y, 
                "dx": -1,
                "dy": 0,
                "dir_change": 0,
                "health": 1,
                "shoot_delay": 30
            })
        elif enemy_type == 5:  # Bomber (drops projectiles)
            self.enemies.append({
                "type": 5, 
                "x": 160, 
                "y": y, 
                "dx": -1, 
                "dy": 0, 
                "health": 2, 
                "shoot_delay": 40
            })
        elif enemy_type == 6:  # Tank (slow but tough)
            self.enemies.append({
                "type": 6, 
                "x": 160, 
                "y": y, 
                "dx": -0.5, 
                "dy": 0, 
                "dir_change": 0, 
                "health": 5, 
                "shoot_delay": 120
            })

    def update_game(self):
        # Debug key to set score
        if pyxel.btnp(pyxel.KEY_F1):
            self.score = 350
            
        # Check for boss initiation
        if self.score >= self.boss_trigger_score and not self.boss:
            # Flash screen red 3 times
            for _ in range(3):
                pyxel.cls(8)  # Red flash
                pyxel.flip()
                for _ in range(10):  # Wait
                    pyxel.flip()

            # Initialize boss based on current level
            if self.current_level == 1:
                self.boss = {
                    "x": 120,
                    "y": 60,
                    "dy": 1,
                    "hp": 250,
                    "max_hp": 250,
                    "shoot_timer": 0,
                    "pattern": "straight",
                    "speed": 1,
                    "hit_flash": 0
                }
            elif self.current_level == 2:
                self.boss = {
                    "x": 120,
                    "y": 60,
                    "dy": 2,
                    "hp": 350,
                    "max_hp": 350,
                    "shoot_timer": 0,
                    "pattern": "spread",
                    "speed": 1.5,
                    "angle": 0,
                    "hit_flash": 0
                }
            else:
                self.boss = {
                    "x": 120,
                    "y": 60,
                    "dy": 3,
                    "hp": 500,
                    "max_hp": 500,
                    "shoot_timer": 0,
                    "pattern": "spiral",
                    "speed": 2,
                    "angle": 0,
                    "hit_flash": 0
                }
            # Clear existing enemies
            self.enemies.clear()
            # Start boss battle music
            if self.sound_enabled:
                pyxel.stop(0)  # Stop background music
                pyxel.play(0, 4, loop=True)  # Play boss music
            return

        # Only spawn enemies if boss is not active
        if not self.boss:
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer >= 60:  # Spawn enemy every 60 frames
                self.spawn_enemy()
                self.enemy_spawn_timer = 0

        # Update enemies
        for enemy in self.enemies[:]:
            enemy["shoot_delay"] -= 1

            if enemy["type"] == 0:  # Scout
                # Calculate distance to player
                dx = self.player_x - enemy["x"]
                dy = self.player_y - enemy["y"]
                distance = math.sqrt(dx * dx + dy * dy)

                if distance < 50:  # Within range for kamikaze behavior
                    # Normalize direction and apply speed
                    speed = 2
                    enemy["dx"] = (dx / distance) * speed
                    enemy["dy"] = (dy / distance) * speed
                    enemy["x"] += enemy["dx"]
                    enemy["y"] = max(25, min(110, enemy["y"] + enemy["dy"]))  # Keep within bounds
                else:
                    enemy["x"] += enemy["dx"]
                    enemy["dy"] = 0

                if enemy["shoot_delay"] <= 0:
                    self.enemy_bullets.append([enemy["x"], enemy["y"] + 2])
                    enemy["shoot_delay"] = 45
                    if self.sound_enabled:
                        pyxel.play(1, 2)

            elif enemy["type"] == 1:  # Destroyer
                enemy["x"] += enemy["dx"]
                enemy["y"] += enemy["dy"]
                enemy["move_counter"] += 1
                if enemy["move_counter"] >= 20:
                    enemy["dy"] *= -1
                    enemy["move_counter"] = 0
                if enemy["shoot_delay"] <= 0:
                    # Burst fire
                    for i in range(3):
                        self.enemy_bullets.append([enemy["x"], enemy["y"] + 3])
                    enemy["shoot_delay"] = 30
                    if self.sound_enabled:
                        pyxel.play(1, 2)

            elif enemy["type"] == 2:  # Cruiser
                enemy["x"] += enemy["dx"]
                enemy["angle"] += 0.15
                enemy["y"] = 60 + math.sin(enemy["angle"]) * 40
                if enemy["shoot_delay"] <= 0:
                    # Spread shot
                    for i in range(-1, 2):
                        self.enemy_bullets.append([enemy["x"], enemy["y"] + i * 4])
                    enemy["shoot_delay"] = 60
                    if self.sound_enabled:
                        pyxel.play(1, 2)

            elif enemy["type"] == 3:  # Battleship
                enemy["x"] += enemy["dx"]
                if enemy["shoot_delay"] <= 0:
                    # Heavy shot
                    self.enemy_bullets.append([enemy["x"], enemy["y"]])
                    self.enemy_bullets.append([enemy["x"], enemy["y"] + 6])
                    enemy["shoot_delay"] = 90
                    if self.sound_enabled:
                        pyxel.play(1, 2)

            elif enemy["type"] == 4:  # Drone
                enemy["x"] += enemy["dx"]
                enemy["dir_change"] += 1
                if enemy["dir_change"] >= 30:
                    enemy["dy"] = pyxel.rndf(-2, 2)
                    enemy["dir_change"] = 0
                enemy["y"] = max(25, min(110, enemy["y"] + enemy["dy"]))
                if enemy["shoot_delay"] <= 0:
                    self.enemy_bullets.append([enemy["x"], enemy["y"]])
                    enemy["shoot_delay"] = 30
            elif enemy["type"] == 5:  # Bomber
                enemy["x"] += enemy["dx"]
                enemy["y"] += math.sin(enemy["x"] / 30) * 2
                if enemy["shoot_delay"] <= 0:
                    for i in range(-1, 2):
                        self.enemy_bullets.append([enemy["x"], enemy["y"] + i * 5])
                    enemy["shoot_delay"] = 40
            elif enemy["type"] == 6:  # Tank
                enemy["x"] += enemy["dx"] * 0.5  # Slower movement
                if enemy["shoot_delay"] <= 0:
                    for angle in range(-30, 31, 30):
                        dx = math.cos(math.radians(angle)) * -2
                        dy = math.sin(math.radians(angle))
                        self.enemy_bullets.append([enemy["x"], enemy["y"], dx, dy])
                    enemy["shoot_delay"] = 120
                enemy["y"] = max(25, min(110, enemy["y"] + enemy["dy"]))
                if enemy["y"] <= 25 or enemy["y"] >= 110:
                    enemy["dy"] *= -1  # Reverse direction when hitting boundaries
                if enemy["shoot_delay"] <= 0:
                    self.enemy_bullets.append([enemy["x"], enemy["y"]])
                    enemy["shoot_delay"] = 30
                    if self.sound_enabled:
                        pyxel.play(1, 2)

            # Remove enemies that go off screen
            if enemy["x"] < -10:
                self.enemies.remove(enemy)

        # Update enemy bullets with speed multiplier
        for bullet in self.enemy_bullets[:]:
            if len(bullet) == 4:  # Directional bullet
                bullet[0] += bullet[2] * self.game_speed_multiplier
                bullet[1] += bullet[3] * self.game_speed_multiplier
            else:  # Standard bullet
                bullet[0] -= 3 * self.game_speed_multiplier
            if bullet[0] < 0:
                self.enemy_bullets.remove(bullet)

        # Update explosions
        for explosion in self.explosions[:]:
            explosion["timer"] -= 1
            if explosion["timer"] <= 0:
                self.explosions.remove(explosion)

        # Hit detection - Player bullets hitting enemies
        for bullet in self.player_bullets[:]:
            for enemy in self.enemies[:]:
                if (abs(bullet[0] - enemy["x"]) < 8 and 
                    abs(bullet[1] - enemy["y"]) < 8):
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                        self.explosions.append({
                            "x": enemy["x"],
                            "y": enemy["y"],
                            "timer": 10
                        })
                        if self.sound_enabled:
                            pyxel.play(1, 3)  # Play explosion sound
                        self.score += 10

                        # Chance to spawn power-up (20% chance when enemy is destroyed)
                        if pyxel.rndi(0, 100) < 20:
                            powerup_type = pyxel.rndi(0, 2)
                            self.powerups.append({
                                "x": enemy["x"],
                                "y": enemy["y"],
                                "type": powerup_type,
                                "width": 10,
                                "height": 5
                            })

        # Update power-ups
        for powerup in self.powerups[:]:
            powerup["x"] -= 1
            # Check if player collected power-up (using rectangle collision)
            player_rect = {"x": self.player_x, "y": self.player_y, "width": 16, "height": 10}
            powerup_rect = powerup

            if (player_rect["x"] < powerup_rect["x"] + powerup_rect["width"] and
                player_rect["x"] + player_rect["width"] > powerup_rect["x"] and
                player_rect["y"] < powerup_rect["y"] + powerup_rect["height"] and
                player_rect["y"] + player_rect["height"] > powerup_rect["y"]):
                self.activate_powerup(powerup["type"])
                self.powerups.remove(powerup)
            elif powerup["x"] < -10:
                self.powerups.remove(powerup)

        # Update power-up timer
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.deactivate_powerup()

        # Hit detection - Enemy collision and bullets hitting player
        for enemy in self.enemies[:]:
            if (abs(enemy["x"] - self.player_x) < 12 and 
                abs(enemy["y"] - self.player_y) < 12):
                self.player_lives -= 1
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
                    self.explosions.append({
                        "x": enemy["x"],
                        "y": enemy["y"],
                        "timer": 10
                    })
                if self.sound_enabled:
                    pyxel.play(1, 3)
                if self.player_lives <= 0:
                    self.game_state = "GAME_OVER"
                    self.initials = ["A", "A", "A"]
                    self.initial_index = 0
                    self.is_high_score = self.score > min(score["score"] for score in self.high_scores) if self.high_scores else True
                    self.enemies.clear()
                self.enemy_bullets.clear()
                self.player_bullets.clear()
                break

        # Hit detection - Enemy bullets hitting player
        for bullet in self.enemy_bullets[:]:
            if (abs(bullet[0] - self.player_x) < 8 and 
                abs(bullet[1] - self.player_y) < 8):
                self.player_lives -= 1
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)
                if self.sound_enabled:
                    pyxel.play(1, 3)  # Play explosion sound
                # Pause for a moment
                for _ in range(30):  # Pause for 30 frames (0.5 seconds)
                    pyxel.flip()
                if self.player_lives <= 0:
                    if self.sound_enabled:
                        pyxel.stop()  # Stop current music
                        pyxel.play(0, 9)  # Play game over music
                    self.game_state = "GAME_OVER"
                    self.initials = ["A", "A", "A"]  # Default initials
                    self.initial_index = 0  # Current initial being edited
                    self.is_high_score = self.score > min(score["score"] for score in self.high_scores) if self.high_scores else True
                    self.enemies.clear()
                self.enemy_bullets.clear()
                self.player_bullets.clear()

        # Player movement
        if pyxel.btn(pyxel.KEY_UP) and self.player_y > 0:
            self.player_y -= 2
        if pyxel.btn(pyxel.KEY_DOWN) and self.player_y < 112:
            self.player_y += 2
        if pyxel.btn(pyxel.KEY_LEFT) and self.player_x > 0:
            self.player_x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < 152:
            self.player_x += 2

        # Shooting
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.shot_pattern == "spread":
                for angle in range(-20, 21, 20):
                    dx = math.cos(math.radians(angle)) * 4
                    dy = math.sin(math.radians(angle))
                    self.player_bullets.append([self.player_x + 8, self.player_y + 4, dx, dy])
            else:
                self.player_bullets.append([self.player_x + 8, self.player_y + 4, 4, 0])

            if self.partner_active:
                partner_x = self.player_x + self.partner_offset["x"]
                partner_y = self.player_y + self.partner_offset["y"]
                self.player_bullets.append([partner_x + 8, partner_y + 4, 4, 0])

            if self.sound_enabled:
                pyxel.play(1, 1)

        # Update bullets and check boss hits
        for bullet in self.player_bullets[:]:
            if len(bullet) == 4:  # Directional bullet
                bullet[0] += bullet[2]
                bullet[1] += bullet[3]
            else:  # Standard bullet
                bullet[0] += 4

            # Check boss hits
            if self.boss and (120 <= bullet[0] <= 144 and 
                            self.boss["y"] <= bullet[1] <= self.boss["y"] + 11):
                if bullet in self.player_bullets:
                    self.player_bullets.remove(bullet)
                self.boss["hp"] -= 10
                # Add hit flash effect
                self.boss["hit_flash"] = 10  # Flash duration in frames
                if self.boss["hp"] <= 0:
                    # Add explosion effect
                    for i in range(5):
                        self.explosions.append({
                            "x": self.boss["x"] + pyxel.rndi(0, 24),
                            "y": self.boss["y"] + pyxel.rndi(0, 11),
                            "timer": 20
                        })
                    if self.sound_enabled:
                        pyxel.play(1, 3)
                    self.score += 100
                    self.level_complete_timer = 180  # 3 seconds
                    if self.sound_enabled:
                        pyxel.stop(0)  # Stop boss music
                        pyxel.play(0, 5)  # Play victory tune
                    self.score += 100
                    self.level_complete_timer = 180  # 3 seconds
                    self.current_level += 1  # Increment level here
                    self.boss = None
                    self.enemies.clear()
                    self.enemy_bullets.clear()
                    self.player_bullets.clear()
                    # Reset boss trigger score for next level
                    self.boss_trigger_score = self.score + 350
                    return  # Exit the update loop cleanly

            if bullet[0] > 160 or bullet[0] < 0 or bullet[1] < 0 or bullet[1] > 120:
                self.player_bullets.remove(bullet)

        # Update boss
        if self.boss:
            self.boss["y"] += self.boss["dy"]
            if self.boss["y"] <= 10 or self.boss["y"] >= 100:
                self.boss["dy"] *= -1

            # Boss shooting patterns
            self.boss["shoot_timer"] += 1
            shoot_interval = max(10, 30 - (self.current_level * 5))

            if self.boss["shoot_timer"] >= shoot_interval:
                if self.boss["pattern"] == "straight":
                    # Level 1 boss: triple straight shot
                    for offset in [-5, 0, 5]:
                        self.enemy_bullets.append([self.boss["x"], self.boss["y"] + offset])
                elif self.boss["pattern"] == "spread":
                    # Level 2 boss: spread shot
                    for angle in range(-45, 46, 15):
                        dx = math.cos(math.radians(angle)) * -2
                        dy = math.sin(math.radians(angle))
                        self.enemy_bullets.append([self.boss["x"], self.boss["y"], dx, dy])
                else:
                    # Level 3 boss: spiral pattern
                    self.boss["angle"] += 30
                    dx = math.cos(math.radians(self.boss["angle"])) * -3
                    dy = math.sin(math.radians(self.boss["angle"]))
                    self.enemy_bullets.append([self.boss["x"], self.boss["y"], dx, dy])
                    self.enemy_bullets.append([self.boss["x"], self.boss["y"], -dx, -dy])

                self.boss["shoot_timer"] = 0

        # Update background scroll with game speed multiplier
        self.scroll_x = (self.scroll_x + 1 * self.game_speed_multiplier) % 160

    def activate_powerup(self, powerup_type):
        self.current_powerup = powerup_type
        self.powerup_timer = 300  # 5 seconds

        if powerup_type == self.POWERUP_SPREAD:
            self.shot_pattern = "spread"
        elif powerup_type == self.POWERUP_SPEED:
            self.move_speed = 6  # Increased from 4 to 6 for more noticeable speed boost
        elif powerup_type == self.POWERUP_PARTNER:
            self.partner_active = True
            self.partner_offset = {"x": 0, "y": -15}  # Position partner above player

    def deactivate_powerup(self):
        if self.current_powerup == self.POWERUP_SPREAD:
            self.shot_pattern = "normal"
        elif self.current_powerup == self.POWERUP_SPEED:
            self.move_speed = 2
        elif self.current_powerup == self.POWERUP_PARTNER:
            self.partner_active = False

        self.current_powerup = None

    def reset_game(self):
        self.player_x = 20
        self.player_y = 60
        self.player_lives = 3
        self.score = 0
        self.enemies.clear()
        self.enemy_bullets.clear()
        self.player_bullets.clear()
        self.powerups.clear()
        self.current_level = 1
        self.boss = None
        self.boss_trigger_score = 350

    def draw(self):
        pyxel.cls(0)

        # Draw stars with level-specific colors
        for star in self.stars:
            x = (star[0] - self.scroll_x) % 160
            if self.game_state == "GAME":
                if self.current_level == 1:
                    # Blue theme
                    color = 12 if star[1] % 3 == 0 else 6
                    pyxel.pset(x, star[1], color)
                elif self.current_level == 2:
                    # Green theme
                    color = 11 if star[1] % 3 == 0 else 3
                    pyxel.pset(x, star[1], color)
                else:
                    # Red theme
                    color = 8 if star[1] % 3 == 0 else 2
                    pyxel.pset(x, star[1], color)
            else:
                pyxel.pset(x, star[1], 7)

        if self.game_state == "TITLE":
            self.draw_title()
        elif self.game_state == "GAME":
            self.draw_game()
        elif self.game_state == "HIGHSCORE":
            self.draw_highscore()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over()
        elif self.game_state == "SETTINGS":
            self.draw_settings()

    def draw_title(self):
        # Draw title
        pyxel.text(55, 20, "SPACE SHOOTER", pyxel.frame_count % 16)

        # Draw buttons
        button_colors = [5, 5, 5]  # Default colors
        button_colors[self.selected_button] = 6  # Highlight selected button

        pyxel.rect(60, 45, 40, 10, button_colors[0])
        pyxel.text(70, 47, "START", 7)

        pyxel.rect(60, 60, 40, 10, button_colors[1])
        pyxel.text(62, 62, "SCORES", 7)

        pyxel.rect(60, 75, 40, 10, button_colors[2])
        pyxel.text(62, 77, "CONFIG", 7)

        # Navigation hint
        pyxel.text(40, 100, "Use UP/DOWN + ENTER", pyxel.frame_count % 16)

    def draw_game(self):
        if self.level_text_timer > 0:
            if self.level_text_timer == 120 and self.sound_enabled:  # Start of level text
                pyxel.stop(0)  # Stop current music
                pyxel.play(0, 5 + self.current_level, loop=True)  # Play level-specific music
            level_color = 12 if self.current_level == 1 else (11 if self.current_level == 2 else 8)
            pyxel.text(65, 60, f"LEVEL {self.current_level}", level_color)
            self.level_text_timer -= 1
            return

        if self.level_complete_timer > 0:
            if self.level_complete_timer > 120:
                pyxel.text(50, 60, "LEVEL COMPLETED!", pyxel.frame_count % 16)
            else:
                pyxel.cls(0)
            self.level_complete_timer -= 1
            if self.level_complete_timer == 0:
                self.level_text_timer = 120
                self.game_speed_multiplier *= 1.2
                # Clear all game objects
                self.enemies.clear()
                self.enemy_bullets.clear()
                self.player_bullets.clear()
                self.powerups.clear()
                self.explosions.clear()
                self.enemy_spawn_timer = 0
                # Reset player position
                self.player_x = 20
                self.player_y = 60
            return

        # Draw power-ups
        for powerup in self.powerups:
            pyxel.blt(powerup["x"], powerup["y"], 0, 32, 0, 10, 5, 0)

        # Draw partner ship if active
        if self.partner_active:
            partner_x = self.player_x + self.partner_offset["x"]
            partner_y = self.player_y + self.partner_offset["y"]
            pyxel.blt(partner_x, partner_y, 0, 0, 0, 16, 10, 0)

        # Draw enemies
        for enemy in self.enemies:
            sprite_y = enemy["type"] * 8
            pyxel.blt(enemy["x"], enemy["y"], 0, 16, sprite_y, 10, 8, 0)

        # Draw player sprite
        pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 10, 0)

        # Draw player bullets
        for bullet in self.player_bullets:
            pyxel.rect(bullet[0], bullet[1], 4, 2, 10)

        # Draw enemy bullets
        for bullet in self.enemy_bullets:
            pyxel.rect(bullet[0], bullet[1], 4, 2, 8)

        # Draw explosions
        for explosion in self.explosions:
            radius = (10 - explosion["timer"]) // 2
            pyxel.circb(explosion["x"] + 5, explosion["y"] + 4, radius, 8 + explosion["timer"] % 3)

        # Draw score and lives
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)
        pyxel.text(80, 5, f"LIVES: {self.player_lives}", 7)

        # Draw power-up status
        if self.current_powerup is not None:
            # Draw background bar
            pyxel.rect(5, 15, 50, 5, 1)
            # Draw progress bar
            bar_width = int((self.powerup_timer / 300) * 48)
            pyxel.rect(6, 16, bar_width, 3, 11)

            # Draw power-up icon and type
            icon_color = 10 if self.current_powerup == self.POWERUP_SPREAD else (
                9 if self.current_powerup == self.POWERUP_SPEED else 12)
            pyxel.circ(60, 17, 3, icon_color)

            # Draw power-up type text
            power_type = "SPREAD" if self.current_powerup == self.POWERUP_SPREAD else (
                "SPEED" if self.current_powerup == self.POWERUP_SPEED else "PARTNER")
            pyxel.text(65, 15, power_type, icon_color)

        #Draw Boss
        if self.boss:
            # Draw boss with hit flash effect
            if self.boss["hit_flash"] > 0:
                self.boss["hit_flash"] -= 1
                color = 7 if self.boss["hit_flash"] % 2 == 0 else 8
                pyxel.pal(9, color)

            pyxel.blt(self.boss["x"], self.boss["y"], 0, 48, 0, 24, 11, 0)
            pyxel.pal()  # Reset palette

            # Draw boss health bar in top right corner
            bar_width = 40
            health_percent = self.boss["hp"] / self.boss["max_hp"]
            current_health_width = int(bar_width * health_percent)

            # Draw background bar
            pyxel.rect(110, 5, bar_width, 5, 1)
            # Draw health bar
            pyxel.rect(111, 6, current_health_width - 2, 3, 8)
            # Draw "BOSS" text
            pyxel.text(115, 12, f"BOSS: {self.boss['hp']}", 8)


    def draw_highscore(self):
        pyxel.text(55, 30, "HIGH SCORES", 7)
        for i, score_data in enumerate(self.high_scores):
            pyxel.text(45, 45 + i * 10, f"{i+1}. {score_data['initials']} - {score_data['score']}", 7)
        pyxel.text(40, 100, "Press Q to return", 7)

    def draw_game_over(self):
        pyxel.text(60, 30, "GAME OVER", 8)
        pyxel.text(50, 45, f"FINAL SCORE: {self.score}", 7)

        if self.is_high_score:
            pyxel.text(40, 60, "NEW HIGH SCORE!", pyxel.frame_count % 16)
            pyxel.text(30, 70, "ENTER YOUR INITIALS:", 7)
            for i, initial in enumerate(self.initials):
                color = 11 if i == self.initial_index else 7
                pyxel.text(65 + i * 8, 80, initial, color)

        pyxel.rect(30, 95, 40, 10, 5)  # Play Again button
        pyxel.text(35, 97, "PLAY", 7)

        pyxel.rect(90, 95, 40, 10, 5)  # Menu button
        pyxel.text(95, 97, "MENU", 7)

        if self.is_high_score:
            pyxel.text(20, 110, "USE ARROWS + ENTER TO SET INITIALS", 7)
        else:
            pyxel.text(20, 110, "PRESS SPACE/ESC TO CONTINUE", 7)

    def draw_settings(self):
        pyxel.text(55, 30, "SETTINGS", 7)

        # Sound setting
        color = 6 if self.settings_selection == 0 else 7
        sound_text = "ON" if self.sound_enabled else "OFF"
        pyxel.text(40, 50, f"SOUND: {sound_text}", color)

        # Difficulty setting
        color = 6 if self.settings_selection == 1 else 7
        pyxel.text(40, 60, f"DIFFICULTY: {self.difficulty}", color)

        pyxel.text(30, 100, "UP/DOWN to select, ENTER to change", 7)

SpaceShooter()