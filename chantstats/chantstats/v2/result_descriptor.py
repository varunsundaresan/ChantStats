import os
from chantstats.v2.repertoire_and_genre import RepertoireAndGenreType
from chantstats.v2.analysis_functions import AnalysisType
from chantstats.v2.unit import UnitType


class ResultDescriptor:
    def __init__(self, rep_and_genre, analysis, unit, modal_category):
        self.rep_and_genre = RepertoireAndGenreType(rep_and_genre)
        self.analysis = AnalysisType(analysis)
        self.unit = UnitType(unit)
        self.modal_category = modal_category

        self.sep = "__"
        self.output_dirname = os.path.join(
            self.rep_and_genre.output_path_stub_1,
            self.analysis.output_path_stub,
            self.rep_and_genre.output_path_stub_2,
            self.unit.output_path_stub,
        )

    def get_output_dir(self, output_root_dir):
        return os.path.join(output_root_dir, self.output_dirname)

    def get_output_filename(self, filename_prefix, filename_suffix, filetype=".png"):
        output_filename = self.sep.join(
            [
                filename_prefix,
                # self.modal_category.output_path_stub_1,
                self.modal_category.output_path_stub_2,
                filename_suffix + filetype,
            ]
        )
        return output_filename

    def get_full_output_path(self, output_root_dir, *, filename_prefix, filename_suffix, filetype=".png"):
        output_dir = self.get_output_dir(output_root_dir)
        output_filename = self.get_output_filename(filename_prefix, filename_suffix, filetype=filetype)
        return os.path.join(output_dir, output_filename)

    def __repr__(self):
        result_descriptor_stubs = (
            self.rep_and_genre.output_path_stub_1,
            self.analysis.output_path_stub,
            self.rep_and_genre.output_path_stub_2,
            self.unit.output_path_stub,
            self.modal_category.output_path_stub_1,
            self.modal_category.output_path_stub_2,
        )
        return f"<{result_descriptor_stubs}>"
