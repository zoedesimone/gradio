"""gr.StackedSlider() component."""

from __future__ import annotations

import math
import random
from typing import Any, Callable, Literal

from gradio_client.documentation import document, set_documentation_group
from gradio_client.serializing import NumberSerializable

from gradio.components.base import IOComponent
from gradio.events import Changeable, Inputable, Releaseable


set_documentation_group("component")


@document()
class StackedSlider(
    Changeable,
    Inputable,
    Releaseable,
    IOComponent
):
    """
    Creates a slider that ranges from 0 to 100 with multiple.
    Preprocessing: passes slider `values` as a {list[float]} into the function.
    passes category `labels` as a {list[str]} into the function
    Postprocessing: expects {list[float]} returned from function and sets slider value to it as long as it is within range.
    Examples-format: A {list[float]} representing the slider's value.

    Demos: 
    Guides: 
    """

    def __init__(
        self,
        values: list[float] | Callable | None = None,
        *,
        interactive: bool | None = None,
        elem_id: str | None = None,
        category_labels : list[str],
        **kwargs,
    ):
        """
        Parameters:
            values: default thumb values to provide to the slider.
            interactive: if True, will be rendered as an editable slider; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.
            category_labels: slider range labels to provide to the slider.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
        """

        self.values = self.postprocess(values)
        self.cleared_value = [0,10]
        self.test_input = values
        IOComponent.__init__(
            self,
            interactive=interactive,
            elem_id=elem_id,
            category_labels = category_labels,
            **kwargs,
        )

    def get_config(self):
        return {
            "values": self.values,
            "category_labels": self.category_labels,
            **IOComponent.get_config(self),
        }

    def get_random_values(self):
        n_categories = len(self.category_labels)
        range_length = 100 / n_categories
        ranges = [( i * range_length, (i + 1) * range_length) for i in range(n_categories)]
        thumbs = [int((i + 1) * range_length) for i in range(n_categories -1)] #Round to int so that UI doesn't display long decimals
        return thumbs


    @staticmethod
    def update(
        values: list[float] | None = None,
        interactive: bool | None = None,
        elem_id: str | None = None,
        category_labels : list[str] | None = None,
    ):
        return {
            "values": values,
            "interactive": interactive,
            "category_labels": category_labels,
            "__type__": "update",
        }

    def postprocess(self, thumb_positions: list[float] ) -> list[tuple(float,float)]:
        """
        Any postprocessing needed to be performed on function output.
        Parameters:
            y: a list of slider thumbs positions
        Returns:
            numeric range for each of the slider thumbs
        """
        thumb_positions.sort()  # Ensure thumb positions are in ascending order
        thumb_positions = [0] + thumb_positions + [100]
        ranges = []
        
        for i in range(len(thumb_positions) - 1):
            range_start = thumb_positions[i]
            range_end = thumb_positions[i + 1]
            ranges.append((range_start, range_end))
        
        return ranges