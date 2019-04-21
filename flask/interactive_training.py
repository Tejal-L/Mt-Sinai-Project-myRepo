# from core import get_tracker, replace_events, add_message
import core
from rasa_core.training import interactive
from rasa_core.events import (
    ActionExecuted, BotUttered, Event, Restarted, UserUttered)
from typing import (Any, Callable, Dict, List, Optional, Text, Tuple, Union)


def validate_user_text(tracker):
    latest_message = interactive.latest_user_message(tracker.get('events', []))
    parse_data = latest_message.get("parse_data", {})
    text = interactive._as_md_message(parse_data)
    intent = parse_data.get("intent", {}).get("name")
    entities = parse_data.get("entities", [])

    if entities:
        message = ("Is the intent '{}' correct for '{}' and are "
                   "all entities labeled correctly?"
                   .format(text, intent))
    else:
        message = ("Your NLU model classified '{}' with intent '{}'"
                   " and there are no entities, is this correct?"
                   .format(text, intent))

    return message

def make_intents_block(sender_id):
    tracker = core.get_tracker(sender_id)
    latest_message = interactive.latest_user_message(tracker.get('events', []))
    predictions = latest_message.get(
        "parse_data", {}).get("intent_ranking", [])
    predicted_intents = {p["name"] for p in predictions}

    # this code will add intents that were not predicted to the drop down. will depend on a new argument not implemented
    # for i in intents:
    #     if i not in predicted_intents:
    #         predictions.append({"name": i, "confidence": 0.0})

    options = []
    counter = 0
    for i in predicted_intents:
        options.append({
            "text": {
                "type": "plain_text",
                        "text": i,
                        "emoji": False
            },
            "value": "value-" + str(counter)
        })
        counter += 1
    return options


def make_corrected_nlu(corrected_intent, sender_id, latest_message):
    tracker = core.get_tracker(sender_id)
    evts = tracker.get("events", [])

    corrected_nlu = {
        "intent": corrected_intent,
        "entities": tracker.get("entities", []),
        "text": latest_message.get("text")
    }
    return corrected_nlu


def _correct_wrong_nlu(corrected_nlu: Dict[Text, Any], evts: List[Dict[Text, Any]], sender_id: Text):
    """A wrong NLU prediction got corrected, update core's tracker."""

    latest_message = interactive.latest_user_message(evts)
    corrected_events = interactive.all_events_before_latest_user_msg(evts)

    latest_message["parse_data"] = corrected_nlu

    replaced_events_tracker = core.replace_events(
        endpoint, sender_id, corrected_events)

    added_message_tracker = core.add_message(
        sender_id, latest_message.get("text"), latest_message.get("parse_data"))

    return added_message_tracker


# def latest_user_message(evts):
#     """Return most recent user message."""

#     for i, e in enumerate(reversed(evts)):
#         if e.get("event") == UserUttered.type_name:
#             return e
#     return None


# def all_events_before_latest_user_msg(
#     evts: List[Dict[Text, Any]]
# ) -> List[Dict[Text, Any]]:
#     """Return all events that happened before the most recent user message."""

#     for i, e in enumerate(reversed(evts)):
#         if e.get("event") == UserUttered.type_name:
#             return evts[:-(i + 1)]
#     return evts
