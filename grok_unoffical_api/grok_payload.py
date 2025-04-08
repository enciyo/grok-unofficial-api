from dataclasses import dataclass

@dataclass
class GrokPayload:
    temporary: bool = False
    modelName: str = "grok-2"
    message: str = ""
    fileAttachments: list = None
    imageAttachments: list = None
    disableSearch: bool = False
    enableImageGeneration: bool = True
    returnImageBytes: bool = False
    returnRawGrokInXaiRequest: bool = False
    enableImageStreaming: bool = True
    imageGenerationCount: int = 2
    forceConcise: bool = False
    toolOverrides: dict = None
    enableSideBySide: bool = True
    isPreset: bool = False
    sendFinalMetadata: bool = True
    customInstructions: str = ""
    deepsearchPreset: str = ""
    isReasoning: bool = False


