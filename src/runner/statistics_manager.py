import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Union, Tuple

@dataclass
class Statistics:
    corrects: Dict[str, List[Tuple[str, str]]] = field(default_factory=dict)
    incorrects: Dict[str, List[Tuple[str, str]]] = field(default_factory=dict)
    errors: Dict[str, List[Union[Tuple[str, str], Tuple[str, str, str]]]] = field(default_factory=dict)
    total: Dict[str, int] = field(default_factory=dict)
    recall: Dict[str, List[Tuple[str, str, float]]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Dict[str, Union[Dict[str, int], List[Tuple[str, str]], float]]]:
        """
        Converts the statistics data to a dictionary format.

        Returns:
            Dict[str, Dict[str, Union[Dict[str, int], List[Tuple[str, str]], float]]]: The statistics data as a dictionary.
        """
        return {
            "counts": {
                key: {
                    "correct": len(self.corrects.get(key, [])),
                    "incorrect": len(self.incorrects.get(key, [])),
                    "error": len(self.errors.get(key, [])),
                    "total": self.total.get(key, 0),
                    "recall": self.recall.get(key, 0)
                }
                for key in self.total
            },
            "ids": {
                key: {
                    "correct": sorted(self.corrects.get(key, [])),
                    "incorrect": sorted(self.incorrects.get(key, [])),
                    "error": sorted(self.errors.get(key, []))
                }
                for key in self.total
            }
        }

class StatisticsManager:
    def __init__(self, result_directory: str):
        """
        Initializes the StatisticsManager.

        Args:
            result_directory (str): The directory to store results.
        """
        self.result_directory = Path(result_directory)
        self.statistics = Statistics()

        # Ensure the statistics file exists
        self.statistics_file_path = self.result_directory / "-statistics.json"
        if not self.statistics_file_path.exists():
            self.statistics_file_path.touch()
            self.dump_statistics_to_file()

    def update_stats(self, db_id: str, question_id: str, validation_for: str, result: Dict[str, Any]):
        """
        Updates the statistics based on the validation result.

        Args:
            db_id (str): The database ID.
            question_id (str): The question ID.
            validation_for (str): The validation context.
            result (Dict[str, Any]): The validation result.
        """
        exec_res = result["exec_res"]
        exec_err = result["exec_err"]

        self.statistics.total[validation_for] = self.statistics.total.get(validation_for, 0) + 1

        if exec_res == 1:
            if validation_for not in self.statistics.corrects:
                self.statistics.corrects[validation_for] = []
            self.statistics.corrects[validation_for].append((db_id, question_id))
        else:
            if exec_err == "incorrect answer":
                if validation_for not in self.statistics.incorrects:
                    self.statistics.incorrects[validation_for] = []
                self.statistics.incorrects[validation_for].append((db_id, question_id))
            else:
                if validation_for not in self.statistics.errors:
                    self.statistics.errors[validation_for] = []
                self.statistics.errors[validation_for].append((db_id, question_id, exec_err))
                
    def update_recall(self, db_id: str, question_id: str, validation_for: str, result: Dict[str, Any]):
        """
        Updates the recall based on the validation result.

        Args:
            db_id (str): The database ID.
            question_id (str): The question ID.
            validation_for (str): The validation context.
            result (Dict[str, Any]): The validation result.
        """
        ground_truth_sqls = set()
        for key in result.keys():
            if key.startswith("revise_") and "GOLD_SQL" in result[key]:
                ground_truth_sqls.add(result[key]["GOLD_SQL"])
                
        correct_predictions = {sql: False for sql in ground_truth_sqls}
        
        for key in result.keys():
            if key.startswith("revise_") and "GOLD_SQL" in result[key] and "exec_res" in result[key]:
                ground_truth_sql = result[key]["GOLD_SQL"]
                if result[key]["exec_res"] == 1:
                    correct_predictions[ground_truth_sql] = True
        
        num_ground_truth = len(ground_truth_sqls)
        num_correct = sum(correct_predictions.values())
        recall = num_correct / num_ground_truth if num_ground_truth > 0 else 0.0
        
        if validation_for not in self.statistics.recall:
            self.statistics.recall[validation_for] = 0
        self.statistics.recall[validation_for] = recall
        
    def dump_statistics_to_file(self):
        """
        Dumps the current statistics to a JSON file.
        """
        with self.statistics_file_path.open('w') as f:
            json.dump(self.statistics.to_dict(), f, indent=4)
