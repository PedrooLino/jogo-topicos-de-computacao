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

    return get_hitbox(entity_a).colliderect(get_hitbox(entity_b))


def check_collision_rect(entity, rect):

    return get_hitbox(entity).colliderect(rect)


def _skip(entity, plat):

    skip_fn = getattr(entity, "_skip_platform", None)
    if skip_fn is not None:
        return skip_fn(plat)
    return False


def resolve_horizontal(entity, platforms):

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
