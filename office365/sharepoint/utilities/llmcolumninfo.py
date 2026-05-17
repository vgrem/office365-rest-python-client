from office365.runtime.client_value import ClientValue
from typing import Optional


class LLMColumnInfo(ClientValue):
    def __init__(
        self,
        analyze_image_detail_level: Optional[str] = None,
        analyze_image_with_vision: Optional[bool] = None,
        autofill_column_type: Optional[str] = None,
        custom_model_id: Optional[str] = None,
        custom_parameters_json: Optional[str] = None,
        is_enabled: Optional[bool] = None,
        prompt: Optional[str] = None,
    ):
        self.AnalyzeImageDetailLevel = analyze_image_detail_level
        self.AnalyzeImageWithVision = analyze_image_with_vision
        self.AutofillColumnType = autofill_column_type
        self.CustomModelId = custom_model_id
        self.CustomParametersJson = custom_parameters_json
        self.IsEnabled = is_enabled
        self.Prompt = prompt

    @property
    def entity_type_name(self):
        return "SP.Utilities.LLMColumnInfo"
