from event_pipeline.base import EventBase
from typing import Tuple
class DummyEvent(EventBase):
    def process(self, *args, **kwargs) -> Tuple[bool, int]:
        print("Dummy Event")
        return True,1 
