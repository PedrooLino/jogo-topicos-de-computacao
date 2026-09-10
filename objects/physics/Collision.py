"""
Módulo de colisão.

Toda a lógica de "quem colide com quem" e "como resolver a colisão"
vive aqui, separada da física de movimento (Physicsbody) e das
entidades do jogo. Isso permite que qualquer objeto que tenha:

    - .pos            (Vector2)
    - .width, .height (int/float)
    - .hitbox_offset   (Vector2, opcional -> default (0, 0))
    - .hitbox_size     (tupla (w, h), opcional -> default (width, height))

participe da colisão, sem precisar herdar de nenhuma classe específica.

A "hitbox" é genérica: por padrão ela é igual ao retângulo do sprite,
mas qualquer entidade pode definir um hitbox menor/maior/deslocado
apenas setando `self.hitbox_offset` e `self.hitbox_size` (veja
GameObject), sem precisar mexer neste módulo.
"""

import pygame


def get_hitbox(entity):
    """Retorna o pygame.Rect de colisão de uma entidade (não o rect do sprite)."""
    offset = getattr(entity, "hitbox_offset", None)
    offset_x = offset.x if offset is not None else 0
    offset_y = offset.y if offset is not None else 0

    size = getattr(entity, "hitbox_size", None)
    width, height = size if size is not None else (entity.width, entity.height)

    return pygame.Rect(
        int(entity.pos.x + offset_x),
        int(entity.pos.y + offset_y),
        int(width),
        int(height),
    )


def check_collision(entity_a, entity_b):
    """Colisão genérica entre duas entidades (usa hitbox, não o rect do sprite)."""
    return get_hitbox(entity_a).colliderect(get_hitbox(entity_b))


def check_collision_rect(entity, rect):
    """Colisão entre a hitbox de uma entidade e um pygame.Rect qualquer."""
    return get_hitbox(entity).colliderect(rect)


def _skip(entity, plat):
    """Permite que a própria entidade decida se ignora certa plataforma
    (ex: Enemy nunca ignora plataformas quebráveis, Player/Drop ignoram
    as que já estão abrindo)."""
    skip_fn = getattr(entity, "_skip_platform", None)
    if skip_fn is not None:
        return skip_fn(plat)
    return False


def resolve_horizontal(entity, platforms):
    """Resolve colisão no eixo X contra uma lista de plataformas, usando hitbox."""
    offset_x = getattr(entity, "hitbox_offset", None)
    offset_x = offset_x.x if offset_x is not None else 0

    hitbox = get_hitbox(entity)

    for plat in platforms:
        if _skip(entity, plat):
            continue

        if hitbox.colliderect(plat.rect):
            if entity.vel.x > 0:
                entity.pos.x = plat.rect.left - hitbox.width - offset_x
            elif entity.vel.x < 0:
                entity.pos.x = plat.rect.right - offset_x

            hitbox = get_hitbox(entity)


def resolve_vertical(entity, platforms, ground_y=None):
    """Resolve colisão no eixo Y contra plataformas e o chão. Retorna se está no chão."""
    on_ground = False

    offset_y = getattr(entity, "hitbox_offset", None)
    offset_y = offset_y.y if offset_y is not None else 0

    hitbox = get_hitbox(entity)

    for plat in platforms:
        if _skip(entity, plat):
            continue

        if hitbox.colliderect(plat.rect):
            if entity.vel.y > 0:
                entity.pos.y = plat.rect.top - hitbox.height - offset_y
                entity.vel.y = 0
                on_ground = True

                on_land = getattr(entity, "_on_land", None)
                if on_land is not None:
                    on_land(plat)

            elif entity.vel.y < 0:
                entity.pos.y = plat.rect.bottom - offset_y
                entity.vel.y = 0

            hitbox = get_hitbox(entity)

    if ground_y is not None and hitbox.bottom >= ground_y:
        entity.pos.y = ground_y - hitbox.height - offset_y
        entity.vel.y = 0
        on_ground = True

    return on_ground
