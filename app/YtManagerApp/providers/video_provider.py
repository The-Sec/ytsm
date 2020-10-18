from abc import abstractmethod, ABC
from enum import Enum
from typing import Dict, Iterable, List, Any

from django.forms import Field

from YtManagerApp.models import Subscription, Video


class VideoProviderState(Enum):
    NOT_CONFIGURED = 0
    OK = 1
    ERROR = 2


class ProviderValidationError(ValueError):
    """
    Exception type thrown when validating configurations.
    """
    def __init__(self, field_messages: Dict[str, str], *args, **kwargs):
        """
        Constructor
        :param field_messages: A dictionary which maps field names to errors, which will be displayed to the user.
        """
        super().__init__(*args, **kwargs)
        self.field_messages = field_messages


class InvalidURLError(ValueError):
    """
    Invalid URL exception type
    """
    pass


class VideoProvider(ABC):
    """
    Identifier
    """
    id: str = ""
    """
    Display name, shown to users
    """
    name: str = ""
    """
    Description, shown to users
    """
    description: str = ""
    """
    Dictionary containing fields necessary for configuring
    """
    settings: Dict[str, Field] = {}

    def __init__(self):
        self.state = VideoProviderState.NOT_CONFIGURED

    @abstractmethod
    def configure(self, configuration: Dict[str, Any]) -> None:
        """
        Configures the video provider
        :param configuration: A dictionary containing key-value pairs based on the settings defined.
        :return: None
        """
        pass

    @abstractmethod
    def unconfigure(self) -> None:
        """
        Destroys video provider configuration
        :return:
        """
        pass

    @abstractmethod
    def validate_configuration(self, configuration: Dict[str, Any]) -> None:
        """
        Validates the given configuration. This is executed when validating the settings form from the UI.
        :param configuration: Dictionary containing key-value pairs, based on the settings defined.
        :except ConfigurationValidationError Thrown if there are validation errors
        """
        pass

    @abstractmethod
    def get_subscription_url(self, subscription: Subscription) -> str:
        """
        Builds an URL that links to the given subscription.
        :param subscription: The subscription
        :return: URL
        """
        pass

    @abstractmethod
    def validate_subscription_url(self, url: str) -> None:
        """
        Validates given URL. Throws InvalidURLError if not valid.
        :param url: URL to validate
        :except InvalidURLError Thrown if the URL is not valid
        """
        pass

    @abstractmethod
    def fetch_subscription(self, url: str) -> Subscription:
        """
        Fetches a subscription using given URL
        :param url: Subscription URL
        :return: Subscription
        :except InvalidURLError Thrown if the URL is not valid
        """
        pass

    @abstractmethod
    def get_video_url(self, video: Video) -> str:
        """
        Builds an URL that links to the given video.
        :param video: The video
        :return: URL
        """
        pass

    @abstractmethod
    def fetch_videos(self, subscription: Subscription) -> Iterable[Video]:
        """
        Fetches all the subscription items from the given subscription.
        The method only needs to fetch the minimum amount of details, the update_videos method
        is used to obtain additional information (such as likes/dislikes and other statistics)
        :param subscription:
        :return:
        """
        pass

    @abstractmethod
    def update_videos(self, videos: List[Video], update_metadata=False, update_statistics=False) -> None:
        """
        Updates the metadata for all the videos in the list.
        :param videos: Videos
        :param update_metadata: If true, video metadata (name, description) will be updated
        :param update_statistics: If true, statistics (likes/dislikes, view count) will be updated.
        :return:
        """
        pass


