import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion


def system_clean_explosion(world: esper.World):
    components = world.get_components(CTagExplosion, CAnimation)
    for explosion_entity,  (c_tag, c_a) in components:
        if c_a.curr_frame == c_a.animations_list[c_a.curr_anim].end:
            world.delete_entity(explosion_entity)
