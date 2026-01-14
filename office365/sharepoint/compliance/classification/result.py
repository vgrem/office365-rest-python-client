from office365.runtime.client_value import ClientValue


class ClassificationResult(ClientValue):
    def __init__(
        self,
        confidence_score: float = None,
        content_type_id: str = None,
        content_type_name: str = None,
        error: str = None,
        metas: dict = None,
        model_id: str = None,
        model_version: str = None,
        retention_label_flags: int = None,
        retention_label_name: str = None,
        retry_count: int = None,
        sensitivity_label: str = None,
        table_metas: dict = None,
    ):
        self.confidence_score = confidence_score
        self.content_type_id = content_type_id
        self.content_type_name = content_type_name
        self.error = error
        self.metas = metas
        self.model_id = model_id
        self.model_version = model_version
        self.retention_label_flags = retention_label_flags
        self.retention_label_name = retention_label_name
        self.retry_count = retry_count
        self.sensitivity_label = sensitivity_label
        self.table_metas = table_metas
