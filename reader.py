# Used for ExerciseType
# see https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
from __future__ import annotations
import os
import xlrd
from identify import get_uuid, get_team
from typing import List, Dict, NamedTuple
import paths


class ExerciseType(NamedTuple):
    name: str
    sheet_index: int

    @staticmethod
    def all() -> List[ExerciseType]:
        """
        The script can operate on only one of the two tests at a single time.
        The decision at the start of the script changes the global variable CURRENT_TEST which is used across the script
        """
        return [ExerciseType('חקר ביצועים', 1), ExerciseType('Solution', 0)]


class Attribute(NamedTuple):
    """A single evaluation attribute, containing a numeric part and a textual part"""
    num: str
    text: str


class Evaluation(NamedTuple):
    """A single evaluation for a candidate, containing who made it (evaluator) and relevant attributes"""
    evaluator_name: str
    exercise_name: str
    learning_ability: Attribute
    personal: Attribute
    interpersonal: Attribute
    leader: Attribute
    summary: Attribute


class Record(NamedTuple):
    """A raw record read from the excel files, holding candidate (private) name and team and the actual evaluation.
    Multiple such records may exist for a single candidate"""
    candidate_name: str
    team: str
    evaluation: Evaluation


class Candidate(NamedTuple):
    """All evaluation for a single candidate.
    One object per candidate.
    Used at team context, so team name isn't needed."""
    uuid: str
    evaluations: List[Evaluation]


def _sanitize_num(value: str) -> str:
    """Remove annoying '.0' from numeric values which should all be integers (1-5, actuall)"""
    return f"{int(value)}" if isinstance(value, float) else ""


def _sanitize_team(team_name: str) -> str:
    """Remove tick so that e.g. א and א' are interpreted the same (as א)"""
    return team_name.replace("'", "")


def _read_attribute(sheet, row, col):
    """
    Return the attribute at specified coordinates
    """
    return Attribute(
        num=_sanitize_num(sheet.cell_value(row, col)),
        text=sheet.cell_value(row + 1, col)
    )


def _read_sheet(sheet: xlrd.sheet.Sheet, exercise_name: str) -> List[Record]:
    """
    Return all candidate records in given sheet
    """
    records = []
    # 5 is the candidate count
    for candidate_index in range(5):
        row = 5 + candidate_index * 2
        evaluator_name = sheet.cell_value(5, 1)
        candidate_name = sheet.cell_value(row, 4)
        team_name = _sanitize_team(sheet.cell_value(5, 2))
        evaluation = Evaluation(
            evaluator_name=evaluator_name,
            exercise_name=exercise_name,
            learning_ability=_read_attribute(sheet, row, 5),
            personal=_read_attribute(sheet, row, 10),
            interpersonal=_read_attribute(sheet, row, 15),
            leader=_read_attribute(sheet, row, 20),
            summary=_read_attribute(sheet, row, 25)
        )
        if candidate_name == "":
            continue
        if team_name == "":
            print(f"ERROR No Team (evaluator is {evaluator_name})")
        records.append(Record(candidate_name, team_name, evaluation))
    return records


def _read_all_files(filepaths: List[str]) -> Dict[str, List[Evaluation]]:
    """
    Reads evaluations from all specified file paths.
    Returns a dictionary mapping uuid to "candidate tuple"s
    A "candidate tuple" maps evaluator name to an AttributeSet objects (which holds all
    """
    evaluations_for_candidate = {}
    for filepath in filepaths:
        print(f"Reading file {filepath}")
        src_wb = xlrd.open_workbook(filepath)
        for exercise in ExerciseType.all():
            sheet = src_wb.sheet_by_index(exercise.sheet_index)

            # This is a handy test - most evaluators tend to write their names in the name of the file they upload
            # This check can help find files which have incorrect evaluator names
            evaluator = sheet.cell_value(5, 1)
            if evaluator not in filepath:
                print(f"WARNING: evaluator name {evaluator} not in file path {filepath}\n\tIt may be incorrect")

            for record in _read_sheet(sheet, exercise.name):
                uuid = get_uuid(record.team, record.candidate_name)
                if uuid is None:
                    continue  # Candidate not found, identify module is responsible to report to user
                if uuid not in evaluations_for_candidate:
                    evaluations_for_candidate[uuid] = []
                evaluations_for_candidate[uuid].append(record.evaluation)
    return evaluations_for_candidate


def _sort_to_teams(all_candidates: Dict[str, List[Evaluation]]) -> Dict[str, List[Candidate]]:
    """
    Accepts a dictionary mapping uuid of a candidate to a list of evaluations for this candidate.
    Returns a dictionary mapping name of a team to a list of candidates in this team.
    """
    # Map team name to list of candidates in that team
    teams = {}
    for uuid, evaluations in all_candidates.items():
        team_name = get_team(uuid)
        if team_name not in teams:
            teams[team_name] = []
        teams[team_name].append(Candidate(uuid, evaluations))
    # In each team, we want the candidates sorted by uuid
    for team_name in teams:
        teams[team_name].sort(key=lambda candidate: candidate.uuid)
    return teams


def read() -> Dict[str, List[Candidate]]:
    # Get all full file paths for files in SRC directory
    filepaths = [os.path.join(paths.INPUT, filename) for filename in os.listdir(paths.INPUT)]
    all_candidates = _read_all_files(filepaths)
    print(f"Read totally {len(filepaths)} files")
    return _sort_to_teams(all_candidates)
