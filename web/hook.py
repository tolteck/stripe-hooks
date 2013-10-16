from flask import Blueprint, request
from shared.helpers import jsonify_with_status, ParseHookFailure
from shared.parser import parse_hook

hook = Blueprint("hook", __name__)


@hook.route("/recieve", methods=["POST"])
def receieve_hook():
    """
    Path:       /webhook/recieve
    Method:     POST
    """
    # Abort if we're not sent JSON
    if not request.json:
        return jsonify_with_status(406, {'error': 'Requires application/json'})

    # If the event doesn't have a id, it's not an event
    # https://stripe.com/docs/api#events
    if not request.json.get("id"):
        return jsonify_with_status(406, {'error': 'Does not have an id'})

    try:
        parse_hook(request.json)
    except ParseHookFailure as e:
        # If the hook failed to parse, send back why to stripe
        # This will be visible in your dashboard
        return jsonify_with_status(406, {'error': str(e)})

    return jsonify_with_status(200, {'success': True})