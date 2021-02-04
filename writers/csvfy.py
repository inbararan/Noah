import csv
from reader import Candidate
from typing import Dict, List
import paths


def write(teams: Dict[str, List[Candidate]]):
    rows = []
    for team_name, candidates in teams.items():
        for candidate in candidates:
            for evaluation in candidate.evaluations:
                for axis in ["learning_ability", "personal", "interpersonal", "leader", "summary"]:
                    attribute = getattr(evaluation, axis)
                    rows.append({
                        "id_num": candidate.uuid,
                        "evaluated_by": evaluation.evaluator_name,
                        "exercise": evaluation.exercise_name,
                        "axis": axis,
                        "verbal_eval": attribute.text,
                        "numeric_eval": attribute.num
                    })

    # Regarding "newline" keyword parameter, see:
    # https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row
    with open(paths.CSV_OUTPUT, "w", newline='') as f:
        fields = ["id_num", "evaluated_by", "exercise", "axis", "verbal_eval", "numeric_eval"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
