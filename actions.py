# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
import re

from typing import Any, Text, Dict, List, Union
from rasa_sdk import Tracker, Action
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.forms import FormAction


class ContactForm(FormAction):
    """Collects contact information and adds it to the spreadsheet"""

    def name(self):
        return "contact_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return [
            "name",
            "email",
            "phone",
            "message"
        ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
        - an extracted entity
        - intent: value pairs
        - a whole message
        or a list of them, where a first match will be picked"""
        return {
            "name": [self.from_entity(entity="name"), self.from_text()],
            "email": [self.from_entity(entity="email"), self.from_text()],
            "phone": [self.from_entity(entity="phone"), self.from_text()],
            "message": [self.from_entity(entity="message"), self.from_text()],
        }

    def validate_phone(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate phone value."""

        if value.isdigit() and len(value) == 10:
            return {"phone": value}
        else:
            dispatcher.utter_message(template="utter_wrong_phone")
            # validation failed, set slot to None
            return {"phone": None}

    def validate_email(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate email value."""

        if re.match(r"[^@]+@[^@]+\.[^@]+", value):
            return {"email": value}
        else:
            dispatcher.utter_message(template="utter_wrong_email")
            # validation failed, set slot to None
            return {"email": None}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_submit")
        return []


class ActionGreetUser(Action):
    """Revertible mapped action for utter_greet"""
    def name(self):
        return "action_greet"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_greet", tracker)
        return [UserUtteranceReverted()]
