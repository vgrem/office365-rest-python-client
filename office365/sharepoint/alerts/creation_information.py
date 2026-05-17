from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class AlertCreationInformation(ClientValue):
    """An object that contain the properties used to create a new SP.Alert"""

    def __init__(
        self,
        alert_frequency,
        template_name,
        alert_type,
        alert_template_name: Optional[str] = None,
        alert_time: datetime = datetime.min,
        always_notify: Optional[bool] = None,
        delivery_channels: Optional[int] = None,
        event_type: Optional[int] = None,
        event_type_bitmask: Optional[int] = None,
        filter_: Optional[str] = None,
        properties: Optional[dict] = None,
        status: Optional[int] = None,
        title: Optional[str] = None,
    ):
        """
        :param int alert_frequency: Gets or sets the time interval for sending the alert.
        :param int alert_type: Gets or sets the alert type.
        """
        super().__init__()
        self.AlertFrequency = alert_frequency
        self.AlertTemplateName = template_name
        self.AlertType = alert_type
        self.AlertTemplateName = alert_template_name
        self.AlertTime = alert_time
        self.AlwaysNotify = always_notify
        self.DeliveryChannels = delivery_channels
        self.EventType = event_type
        self.EventTypeBitmask = event_type_bitmask
        self.Filter = filter_
        self.Properties = properties
        self.Status = status
        self.Title = title
