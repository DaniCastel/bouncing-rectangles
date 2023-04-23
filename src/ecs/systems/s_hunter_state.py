import esper
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_animation import CAnimation
from src.ecs.systems import s_animation


def system_hunter_state(world: esper.World, player_entity, hunter_config: dict):
    components = world.get_components(
        CVelocity, CAnimation, CTransform, CHunterState)
    player_transform = world.component_for_entity(player_entity, CTransform)

    for _, (c_v, c_a, c_hunter_transform, c_pst) in components:
        if c_pst.state == HunterState.IDLE:
            _do_idle_state(c_v, c_a, c_hunter_transform,
                           c_pst, player_transform, hunter_config)
        elif c_pst.state == HunterState.ATTACKING:
            _do_attacking_state(c_v, c_a, c_hunter_transform,
                                c_pst, player_transform, hunter_config)
        elif c_pst.state == HunterState.RETURNING:
            _do_returning_state(c_v, c_a, c_hunter_transform,
                                c_pst, player_transform, hunter_config)


def _do_idle_state(c_v: CVelocity, c_a: CAnimation, c_hunter_transform: CTransform, c_pst: CHunterState, player_transform: CTransform, hunter_config: dict):
    _set_animation(c_a, 1)
    # "distance_start_chase": 100,
    # "distance_start_return": 200
    c_v.vel.x = 0
    c_v.vel.y = 0
    if c_hunter_transform.pos.distance_to(player_transform.pos) < hunter_config["distance_start_chase"]:
        c_pst.state = HunterState.ATTACKING


def _do_attacking_state(c_v: CVelocity, c_a: CAnimation, c_hunter_transform: CTransform, c_pst: CHunterState, player_transform: CTransform, hunter_config: dict):
    _set_animation(c_a, 0)
    c_v.vel = (player_transform.pos - c_hunter_transform.pos).normalize() * \
        hunter_config["velocity_chase"]
    hunter_distance = c_hunter_transform.origin.distance_to(
        c_hunter_transform.pos)
    print(c_hunter_transform.origin)
    print(c_hunter_transform.pos)
    if hunter_distance >= hunter_config["distance_start_return"]:
        c_pst.state = HunterState.RETURNING


def _do_returning_state(c_v: CVelocity, c_a: CAnimation, c_hunter_transform: CTransform, c_pst: CHunterState, player_transform: CTransform, hunter_config: dict):
    _set_animation(c_a, 0)
    c_v.vel = (c_hunter_transform.origin - c_hunter_transform.pos).normalize() * \
        hunter_config["velocity_return"]
    hunter_origin_distance = c_hunter_transform.origin.distance_to(
        c_hunter_transform.pos)
    if hunter_origin_distance == 0:
        c_hunter_transform.pos.xy = c_hunter_transform.origin.xy
        c_pst.state = HunterState.IDLE


def _set_animation(c_a: CAnimation, num_anim: int):
    if c_a.curr_anim == num_anim:
        return

    c_a.curr_anim = num_anim
    c_a.curr_anim_time = 0
    c_a.curr_frame = c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start
