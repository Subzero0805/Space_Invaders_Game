# Space_Invaders_Game

### Programming Language/Libaries: Python3| Pygame | Random

This game enabled me to become familiar with creating games using the "pygame" library.
I was able to develop my understanding of Object Orientated Programming (OOP) and class's can be used to reduce repetative code.

### Current Features:
- Main Menu:
  
  ![image](https://user-images.githubusercontent.com/68710182/155002715-5fbbb94b-a1e3-48c2-a1e6-ba41a3551a78.png)
- Player/Head Up Display (HUD):
  
  ![image](https://user-images.githubusercontent.com/68710182/155002982-d0383128-7c43-4c55-9211-0067aa955376.png)
  - Player Spaceship
  - Player Health Bar
  - Level Counter
  - Lives Counter
  - Player Actions: Up, Down, Left, Right, Shoot (Diagonal movement is allowed)
- Enemies:

  ![image](https://user-images.githubusercontent.com/68710182/155003413-c5dcb3ef-821e-4b92-8ac4-0497bd7bf9d0.png)
  - 3 Enemy Types (Currently all enemy types have the same properties):
    - Basic (White bullets)
    - Fast (Blue bullets)
    - Gunner (Red bullets)
  - Spawn at random locations
  - Move down the screen
  - Shoot at the player, reducing health by 10
  - If enemies reach the bottom of the screen, player lives are reduced by 1.
  - If enemies collide with the player ship, player health is reduced by 20 and the enemy is destroyed.
 
### Improvements:
As I further develop my understanding of OOP, I plan to add more features to the game, such as:
- Alien type:
  - Fast Aliens: The ability to shoot faster bullets that deal less damage, but have a lower amount of health.
  - Gunner Aliens: Aliens that shoot slower and deal more damage, but have a higher amount of health.
- Player Power Ups:
  - Burst Fire: The player can now shoot in bursts of 3.
  - Damage Increase: The players bullets now deal more damage.
  - Health restore: Restores the player's health to full.
- Sound:
  - SFX: Add sounds when bullets are fired, power ups are collected and bullets hit enemies.
