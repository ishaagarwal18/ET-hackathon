"""Reusable MongoDB schema fragments."""

OBJECT_ID_PATTERN = "^[a-fA-F0-9]{24}$"

OBJECT_ID = {
    "bsonType": "objectId",
}

OBJECT_ID_REF = {
    "bsonType": "object",
    "required": ["id", "collection"],
    "additionalProperties": False,
    "properties": {
        "id": {"bsonType": "objectId"},
        "collection": {"bsonType": "string", "minLength": 1},
        "display_name": {"bsonType": "string"},
    },
}

TIMESTAMPS = {
    "created_at": {"bsonType": "date"},
    "updated_at": {"bsonType": "date"},
    "deleted_at": {"bsonType": ["date", "null"]},
}

STATUS = {
    "status": {
        "bsonType": "string",
        "enum": ["active", "inactive", "pending", "archived", "deleted"],
    },
}

METADATA = {
    "metadata": {
        "bsonType": "object",
        "description": "Non-authoritative extension data for integrations and enrichment.",
    },
}

AUDIT_FIELDS = {
    "created_by": OBJECT_ID_REF,
    "updated_by": OBJECT_ID_REF,
}

TENANT_ID = {
    "tenant_id": {
        "bsonType": "objectId",
        "description": "Owning organization or tenant boundary.",
    },
}

SEVERITY = {
    "bsonType": "string",
    "enum": ["informational", "low", "medium", "high", "critical"],
}

CONFIDENCE = {
    "bsonType": "int",
    "minimum": 0,
    "maximum": 100,
}

TAGS = {
    "bsonType": "array",
    "items": {"bsonType": "string", "minLength": 1},
    "uniqueItems": True,
}
