"""
This model illustrates the spontaneous synronization of large crowds without a
central central clock or synronization tool. In this model, the agents
(fireflies) start chaning color (blinkin) at random frequencies. However, at
each simulation run, the agents increase or decrease the frequencies based on
the average ofneighborung agents' blinkin frequencies. After a certain number
of simulation runs, we see that all of the agents are blinking at the pretty
much same frequency.

A related video that explains this phenomena:
https://www.youtube.com/watch?v=t-_VPRCtiUg

Another good website to understand this model:
https://1000fireflies.net/about
"""

import random
from lib.agent import MOVE
from lib.display_methods import LIMEGREEN, GRAY
from lib.model import Model, NUM_MBRS, MBR_ACTION, COLOR
from lib.utils import Debug
from registry.registry import save_reg, TEST_EXEC_KEY, get_model

DEBUG = Debug()

MODEL_NAME = "firefly"
DEF_NUM_FIREFLY = 50
DEF_MIN_BLINK_FREQUENCY = 1
DEF_MAX_BLINK_FREQUENCY = 10
FIREFLY_ON = "Firefly ON"
FIREFLY_OFF = "Firefly OFF"
BLINK_FREQUENCY = "blink_frequency"
LAST_BLINKED_AT = "last_blinked_at"


def firefly_blink(agent, **kwargs):
    """
    Blinks the given firefly agent by chaning its group. If the firefly is
    already ON, this function turns if OFF. Otherwise, checks if the
    the time passed since last blink time of the firefly agent is
    greater than the agent's blinking frequency.
    """
    # Calculate the blink parameter
    blink_frequency = agent.get_attr(BLINK_FREQUENCY)
    time_since_last_blink = agent.get_attr(LAST_BLINKED_AT) - agent.duration

    # Get the previous group name
    old_group = agent.group_name()

    # Turn OFF if the firefly is ON
    if old_group == FIREFLY_ON:
        agent.set_prim_group(FIREFLY_OFF)

    # Turn ON if the blinking time has arrived
    elif time_since_last_blink >= blink_frequency:
        agent.set_prim_group(FIREFLY_ON)
        # Reset the attribute
        agent.set_attr(LAST_BLINKED_AT, agent.duration)

    # Perform the actual switch
    get_model(agent.exec_key).add_switch(
        str(agent), old_group, agent.group_name()
    )


def adjust_blink_frequency(agent, **kwargs):
    """
    Inreases or decreases the agent's blinking frequency based on the average
    of its neighbors. If the blinking frequency is not initialized for this
    agent, it assigns a random frequency value within the specified range.
    """
    # Initialize the blink frequency if not initialized before
    if agent.get_attr(BLINK_FREQUENCY) is None:
        frequency = random.randint(
            DEF_MIN_BLINK_FREQUENCY, DEF_MAX_BLINK_FREQUENCY
        )
        time = agent.duration
        agent.set_attr(BLINK_FREQUENCY, frequency)
        agent.set_attr(LAST_BLINKED_AT, time)

        if DEBUG.debug:
            print(f"Set {agent}'s blink frequency to {frequency}")
            print(f"Set {agent}'s last blinked at time to {time}")

    # Get the average blinking frequency of the neighbours
    else:
        # Will be implemented once the required function exists in the library
        pass


def firefly_action(agent, **kwargs):
    """
    A simple default agent action.
    """
    adjust_blink_frequency(agent, **kwargs)

    firefly_blink(agent, **kwargs)

    return MOVE


firefly_grps = {
    FIREFLY_OFF: {
        MBR_ACTION: firefly_action,
        NUM_MBRS: DEF_NUM_FIREFLY,
        COLOR: GRAY,
    },
    FIREFLY_ON: {
        NUM_MBRS: 0,
        COLOR: LIMEGREEN,
    },
}


class Firefly(Model):
    """
    This class should just create a Firefly model that runs, has
    some agents that move around, and allows us to test if
    the system as a whole is working.
    It turns out that so far, we don't really need to subclass anything!
    """

    def handle_props(self, props):
        super().handle_props(props)
        height = self.props.get("grid_height")
        width = self.props.get("grid_width")
        density = self.props.get("density")
        num_agents = int(height * width * density)
        self.grp_struct[FIREFLY_OFF]["num_mbrs"] = num_agents


def create_model_for_test(props=None):
    """
    This set's up the Firefly model at exec_key 0 for testing.
    This method is to be called from registry only. Props may be
    overridden here for testing but the conventional api would be the correct
    way to do that.
    :param props: None
    :return: Firefly
    """
    return Firefly(
        MODEL_NAME, grp_struct=firefly_grps, props=props, create_for_test=True
    )


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return Firefly(serial_obj=serial_obj)
    else:
        return Firefly(MODEL_NAME, grp_struct=firefly_grps, props=props)


def setup_test_model():
    """
    Set's up the Firefly model at exec_key = 0 for testing purposes.
    :return: None
    """
    create_model_for_test(props=None)
    save_reg(TEST_EXEC_KEY)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
