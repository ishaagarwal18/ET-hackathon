"""Attack chain visualization payload builder."""


def build_attack_chain_visualization(*, current_stage: str, prediction: dict, previous_activities: list[str]) -> dict:
    """Return graph-style visualization data for frontend rendering."""
    nodes = [
        {"id": "previous_activity", "label": "Previous Activities", "type": "evidence", "status": "observed"},
        {"id": current_stage, "label": current_stage.replace("_", " ").title(), "type": "stage", "status": "current"},
        {
            "id": prediction["next_stage"],
            "label": prediction["next_stage"].replace("_", " ").title(),
            "type": "stage",
            "status": "predicted",
        },
    ]
    edges = [
        {"source": "previous_activity", "target": current_stage, "label": "supports"},
        {"source": current_stage, "target": prediction["next_stage"], "label": "likely progression"},
    ]
    annotations = [
        {"label": "Likely Next Attack", "value": prediction["likely_next_attack"]},
        {"label": "Probability", "value": prediction["probability"]},
        {"label": "Evidence Count", "value": len(previous_activities)},
    ]
    return {"nodes": nodes, "edges": edges, "annotations": annotations}
