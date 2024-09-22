class DataIngestionError(Exception):
    """Exception raised for errors in the data ingestion process."""
    pass


class PreprocessingError(Exception):
    """Exception raised for errors in the preprocessing step."""
    pass


class AnalysisError(Exception):
    """Exception raised for errors in the analysis step."""
    pass


class IntegrationError(Exception):
    """Exception raised for errors in the data integration step."""
    pass


class ReportingError(Exception):
    """Exception raised for errors in the reporting step."""
    pass
