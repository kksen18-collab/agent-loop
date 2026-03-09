mark_complete_json = {
    "name": "mark_complete",
    "description": "Mark complete the todo at the given position (starting from 1) and return the full list",
    "parameters": {
        "properties": {
            "index": {
                "description": "The 1-based index of the todo to mark as complete",
                "title": "Index",
                "type": "integer",
            },
            "completion_notes": {
                "description": "Notes about how you completed the todo in rich console markup",
                "title": "Completion Notes",
                "type": "string",
            },
        },
        "required": ["index", "completion_notes"],
        "type": "object",
        "additionalProperties": False,
    },
}
