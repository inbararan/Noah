import os
import openpyxl
from reader import Candidate, ExerciseType
from typing import List, Dict
import identify
import paths


def _extract_evaluators(candidates: List[Candidate]) -> List[str]:
    """
    Accepts a list of candidates, and returns a sorted list of
    evaluators which have evaluated at least one of the candidates
    """
    evaluators = set()
    for candidate in candidates:
        for evaluation in candidate.evaluations:
            evaluators.add(evaluation.evaluator_name)
    if len(evaluators) > 4:
        print(f"WARNING: Too much evaluators for single team: {evaluators}")
    return sorted(evaluators)


def _write_file_for_team(team_name: str, candidates: List[Candidate], exercise_name):
    # Plan is: load template, modify it, and save to a new file
    wb = openpyxl.load_workbook(paths.HAZANOTOMAT_TEMPLATE)
    learning_sheet = wb[wb.sheetnames[0]]
    summary_sheet = wb[wb.sheetnames[1]]

    learning_sheet.cell(1, 1, exercise_name)
    summary_sheet.cell(1, 1, exercise_name)

    evaluators = _extract_evaluators(candidates)

    # Fill in evaluator names
    for evaluator_index, evaluator in enumerate(evaluators):
        col_index = 2 + evaluator_index * 2
        learning_sheet.cell(1, col_index, evaluator)
        summary_sheet.cell(1, col_index, evaluator)

    # Fill in name and evaluation for each candidate
    for candidate_index, candidate in enumerate(candidates):
        row_index = candidate_index + 2

        candidate_name = identify.get_private_name(candidate.uuid)
        learning_sheet.cell(row_index, 1, candidate_name)
        summary_sheet.cell(row_index, 1, candidate_name)
        for evaluation in candidate.evaluations:
            evaluator_index = evaluators.index(evaluation.evaluator_name)
            col_index_num = 2 + evaluator_index * 2
            col_index_text = col_index_num + 1

            learning_sheet.cell(row_index, col_index_num, evaluation.learning_ability.num)
            learning_sheet.cell(row_index, col_index_text, evaluation.learning_ability.text)

            summary_sheet.cell(row_index, col_index_num, evaluation.summary.num)
            summary_sheet.cell(row_index, col_index_text, evaluation.summary.text)

    # Indicate progression - have we got all evaluations for this team? Are we close?
    if len(evaluators) > 3:
        print(f"FINISHED (4/4): {team_name}")
    elif len(evaluators) > 2:
        print(f"CLOSE TO FINISHING (3/4): {team_name}")

    os.makedirs(os.path.join(paths.HAZANOTOMAT_OUTPUT, exercise_name), exist_ok=True)  # Make sure directory exists
    wb.save(os.path.join(paths.HAZANOTOMAT_OUTPUT, exercise_name, f"צוות {team_name}.xlsx"))


def _filter_evaluations(candidate: Candidate, exercise_name: str) -> Candidate:
    """
    Accepts a candidate and an exercise name.
    Returns a similar candidate with evaluations which are only of the specified exercise.
    """
    return Candidate(
        candidate.uuid,
        [evaluation for evaluation in candidate.evaluations if evaluation.exercise_name == exercise_name]
    )


def write(teams: Dict[str, List[Candidate]]):
    print("Writing...")
    for team_name, candidates_in_team in teams.items():
        for exercise in ExerciseType.all():
            candidates = [_filter_evaluations(candidate, exercise.name) for candidate in candidates_in_team]
            _write_file_for_team(team_name, candidates, exercise.name)
