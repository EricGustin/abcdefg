from arcade.sdk import ToolCatalog
from arcade.sdk.eval import (
    EvalRubric,
    EvalSuite,
    SimilarityCritic,
    tool_eval,
)

import arcade_abcdefg
from arcade_abcdefg.tools.hello import say_hello

# Evaluation rubric
rubric = EvalRubric(
    fail_threshold=0.85,
    warn_threshold=0.95,
)


catalog = ToolCatalog()
catalog.add_module(arcade_abcdefg)


@tool_eval()
def abcdefg_eval_suite() -> EvalSuite:
    suite = EvalSuite(
        name="abcdefg Tools Evaluation",
        system_message=(
            "You are an AI assistant with access to abcdefg tools. "
            "Use them to help the user with their tasks."
        ),
        catalog=catalog,
        rubric=rubric,
    )

    suite.add_case(
        name="Saying hello",
        user_message="He's actually right here, say hi to him!",
        expected_tool_calls=[(say_hello, {"name": "John Doe"})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="name", weight=0.5),
        ],
        additional_messages=[
            {"role": "user", "content": "My friend's name is John Doe."},
            {"role": "assistant", "content": "It is great that you have a friend named John Doe!"},
        ],
    )

    return suite
