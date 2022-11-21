from dataclasses import dataclass

@dataclass
class DataIngestingArtifacts:
    trained_file_path: str
    test_file_path: str