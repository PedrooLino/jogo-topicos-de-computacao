from scenes.DeathMenu import DeathMenu


class Collisions:

    @staticmethod
    def check_enemy_projectile_player(game_world):

        player_rect = game_world.player.rect

        for proj in game_world.enemy_projectiles[:]:
            if proj.rect.colliderect(player_rect):
                game_world.next_scene = DeathMenu()
                return True

        return False

    @staticmethod
    def check_player_enemy(game_world):

        player_rect = game_world.player.rect
        
        for enemy in game_world.enemies:
            if player_rect.colliderect(enemy.rect):
                game_world.next_scene = DeathMenu()
                return True

        return False

    @staticmethod
    def check_player_projectiles(game_world):
        
        for proj in game_world.player_projectiles[:]:
            hit = False
            for enemy in game_world.enemies:
                if proj.rect.colliderect(enemy.rect):
                    enemy.take_damage(1)
                    hit = True
                    if not enemy.alive:
                        drop = enemy.try_drop()
                        if drop:
                            game_world.drops.append(drop)
                    break

            if hit and proj in game_world.player_projectiles:
                game_world.player_projectiles.remove(proj)

    @staticmethod
    def check_projectile_platforms(game_world):

        for proj in game_world.player_projectiles[:]:
            for plat in game_world.platforms:
                if proj.rect.colliderect(plat.rect):
                    if proj in game_world.player_projectiles:
                        game_world.player_projectiles.remove(proj)
                    break

        for proj in game_world.enemy_projectiles[:]:
            for plat in game_world.platforms:
                if proj.rect.colliderect(plat.rect):
                    if proj in game_world.enemy_projectiles:
                        game_world.enemy_projectiles.remove(proj)
                    break

    @staticmethod
    def check_player_drops(game_world):
        player_rect = game_world.player.rect
        for drop in game_world.drops[:]:
            if drop.rect.colliderect(player_rect):
                game_world.drops.remove(drop)

    @staticmethod
    def remove_dead_enemies(game_world):
        game_world.enemies = [
            enemy for enemy in game_world.enemies
            if enemy.alive
        ]
