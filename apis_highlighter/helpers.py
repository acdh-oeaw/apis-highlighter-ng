import logging
import re
from math import inf

from apis_highlighter.models import AnnotationProject

from django.conf import settings

logger = logging.getLogger(__name__)


def calculate_word_dict(text, direction):
    word_list = re.split(" |\\n", text)
    word_list = [w for w in word_list if w != ""]

    word_dict = {}

    if word_list != []:
        value_step = 1 / len(word_list)
        value_current = 1
        for word in word_list[::direction]:
            word_value = word_dict.get(word, 0)
            word_dict[word] = word_value + value_current
            value_current -= value_step

    return word_dict


def calculate_context_weights(text, i_start, i_end):
    text_left = text[:i_start]
    text_right = text[i_end:]
    word_dict_left = calculate_word_dict(text=text_left, direction=-1)
    word_dict_right = calculate_word_dict(text=text_right, direction=1)

    return {
        "word_dict_left": word_dict_left,
        "word_dict_right": word_dict_right,
    }


def make_diff(word_dict_a, word_dict_b):
    words_all = set(word_dict_a.keys()).union(set(word_dict_b.keys()))
    diff_all = 0
    for word in words_all:
        word_value_a = word_dict_a.get(word, 0)
        word_value_b = word_dict_b.get(word, 0)
        diff_all += abs(word_value_a - word_value_b)

    return diff_all


def correlate_annotations(text_old, text_new, annotations_old):
    for ann in annotations_old:
        i_old_start = ann.start
        i_old_end = ann.end
        context_weights_dict_old = calculate_context_weights(
            text=text_old, i_start=i_old_start, i_end=i_old_end
        )
        ann_text = text_old[ann.start : ann.end]
        diff_min = inf
        i_new_start = None
        i_new_end = None
        for i in re.finditer(f"(?={re.escape(ann_text)})", text_new):
            i_candidate_start = i.start()
            i_candidate_end = i_candidate_start + len(ann_text)
            context_weights_dict_new = calculate_context_weights(
                text=text_new, i_start=i_candidate_start, i_end=i_candidate_end
            )
            diff_left = make_diff(
                context_weights_dict_new["word_dict_left"],
                context_weights_dict_old["word_dict_left"],
            )
            diff_right = make_diff(
                context_weights_dict_new["word_dict_right"],
                context_weights_dict_old["word_dict_right"],
            )
            diff_current = diff_left + diff_right
            if diff_current < diff_min:
                diff_min = diff_current
                i_new_start = i_candidate_start
                i_new_end = i_candidate_end

        if diff_min != inf:
            ann.start = i_new_start
            ann.end = i_new_end
            logging.info(f"Updated annotation {ann} on {ann.text_content_object}")
            ann.save()
        else:
            ann.delete()  # TODO: we might want to delete relations as well.


def get_annotation_project(request=None):
    if request is not None:
        if selected_project := request.GET.get("highlighter_project"):
            if hasattr(request, "session"):
                request.session["apis_highlighter_project_id"] = selected_project
            return selected_project

    default_project = getattr(
        settings,
        "DEFAULT_HIGHLIGTHER_PROJECT",
        AnnotationProject.objects.first().id,
    )

    if hasattr(request, "session"):
        return request.session.get("apis_highlighter_project_id", default_project)

    return default_project
