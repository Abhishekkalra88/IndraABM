import lib.actions as acts
import lib.model as mdl

MODEL_NAME = "wolfsheep"
TIME_TO_REPRO = "time_to_repr"
WOLF_GRP_NM = "wolf"
SHEEP_GRP_NM = "sheep"

# Constants for the model
TOO_CROWDED = 6
CROWDING_EFFECT = 1
MAX_ENERGY = 3

# Can be changed by user
DEFAULT_TIME_TO_REPRO = 5
WOLF_TIME_TO_REPRO = 4
SHEEP_TIME_TO_REPRO = 7
PREY_DIST = 8


def is_agent_dead(agent, **kwargs):
    # Die if the agent runs out of duration
    if agent.duration <= 0:
        agent.die()
        return True


def reproduce(agent, reproduction_period, **kwargs):
    # Check if it is time to produce
    if agent.get_attr(TIME_TO_REPRO) == 0:
        if acts.DEBUG.debug:
            print(str(agent.name) + " is having a baby!")

        # Create babies: need group name here!
        acts.get_model().add_child(agent.prim_group_nm())

        # Reset ttr
        agent.set_attr(TIME_TO_REPRO, reproduction_period)


def eat_sheep(agent, **kwargs):
    prey = acts.get_neighbor(agent=agent, size=PREY_DIST)

    if prey is not None:
        if acts.DEBUG.debug:
            print(str(agent) + " is eating " + str(prey))

        agent.duration += min(prey.duration, MAX_ENERGY)
        prey.die()

    else:
        agent.duration /= 2


def handle_ttr(agent, **kwargs):
    """
    This function adjusts the time to reproduce for a wolf or a sheep.
    An individual gets this parameter from its species.
    """
    if agent.get_attr(TIME_TO_REPRO) is None:
        if agent.prim_group_nm() == WOLF_GRP_NM:
            agent.set_attr(TIME_TO_REPRO, WOLF_TIME_TO_REPRO)
        elif agent.prim_group_nm() == SHEEP_GRP_NM:
            agent.set_attr(TIME_TO_REPRO, SHEEP_TIME_TO_REPRO)
        else:
            agent.set_attr(TIME_TO_REPRO, DEFAULT_TIME_TO_REPRO)
    # Decrease ttr
    agent.set_attr(TIME_TO_REPRO, agent.get_attr(TIME_TO_REPRO) - 1)


def sheep_action(agent, **kwargs):
    """
    This is what a sheep does every period.
    """
    if is_agent_dead(agent):
        return acts.DONT_MOVE
    handle_ttr(agent)
    if acts.get_num_of_neighbors(agent, size=10) > TOO_CROWDED:
        agent.duration -= CROWDING_EFFECT
    # Reproduce if it is the right time
    reproduce(agent, SHEEP_TIME_TO_REPRO)
    return acts.MOVE


def wolf_action(agent, **kwargs):
    if is_agent_dead(agent):
        return acts.DONT_MOVE
    eat_sheep(agent)
    # Handle time to reproduce attribute
    handle_ttr(agent)
    # Check neighbor count
    if acts.get_num_of_neighbors(agent, size=10) > TOO_CROWDED:
        agent.duration -= CROWDING_EFFECT
    # Reproduce if it is the right time
    reproduce(agent, WOLF_TIME_TO_REPRO)
    return acts.MOVE


def create_sheep(name, i, action=sheep_action, **kwargs):
    """
    Create a new sheep.
    """
    return acts.create_agent(name, i, action=action, **kwargs)


def create_wolf(name, i, action=wolf_action, **kwargs):
    """
    Create a new sheep.
    """
    return acts.create_agent(name, i, action=action, **kwargs)


wolfsheep_grps = {
    SHEEP_GRP_NM: {
        mdl.MBR_CREATOR: create_sheep,
        mdl.MBR_ACTION: sheep_action,
        mdl.NUM_MBRS_PROP: "num_sheep",
        mdl.COLOR: acts.GRAY,
    },
    WOLF_GRP_NM: {
        mdl.MBR_CREATOR: create_wolf,
        mdl.MBR_ACTION: wolf_action,
        mdl.NUM_MBRS_PROP: "num_wolves",
        mdl.COLOR: acts.TAN,
    },
}


class WolfSheep(mdl.Model):
    """
    This class should just create a basic model that runs, has
    some agents that move around, and allows us to test if
    the system as a whole is working.
    It turns out that so far, we don't really need to subclass anything!
    """

    def handle_props(self, props):
        super().handle_props(props)
        prey_dist = self.props.get("prey_dist")
        wolf_time_to_repro = self.props.get("repr_wolves")
        sheep_time_to_repro = self.props.get("repr_sheep")
        self.grp_struct[WOLF_GRP_NM]["prey_dist"] = prey_dist
        self.grp_struct[WOLF_GRP_NM]["wolf_time_to_repro"] = wolf_time_to_repro
        self.grp_struct[SHEEP_GRP_NM]["prey_dist"] = prey_dist
        self.grp_struct[SHEEP_GRP_NM][
            "sheep_time_to_repro"
        ] = sheep_time_to_repro


def create_model(serial_obj=None, props=None, create_for_test=False):
    """
    This is for the sake of the API server:
    """
    return WolfSheep(MODEL_NAME, grp_struct=wolfsheep_grps,
                     props=props, create_for_test=create_for_test)


def main():
    model = create_model()
    model.run()

    return 0


if __name__ == "__main__":
    main()
