# Python utils
import json
import fileinput


def get_event_list_from_stdin():
    """
    Get operation from stdin input
    :return: List, operation list to validate and execute. e.g.
        {"account": {"active-card": true, "available-limit": 100}}
        {"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}
    """
    operations = []
    for line in fileinput.input():
        try:
            operations.append(json.loads(line.rstrip()))
        except Exception:
            pass

    return operations
