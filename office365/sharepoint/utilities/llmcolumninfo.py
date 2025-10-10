from office365.runtime.client_value import ClientValue


class LLMColumnInfo(ClientValue):

    def __init__(
        self,
        analyze_image_detail_level: str = None,
        analyze_image_with_vision: bool = None,
        autofill_column_type: str = None,
        custom_model_id: str = None,
        custom_parameters_json: str = None,
        is_enabled: bool = None,
        prompt: str = None,
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
