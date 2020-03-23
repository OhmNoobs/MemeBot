from typing import List, Any
from emoji_data_python import get_emoji_regex
MAX_WIDTH = 12


class ToiletPaper:

    def __init__(self, args):
        self.core = "".join(args)

    def wrap(self) -> str:
        core_rows = self._prepare_core_for_wrapping()
        return self._wrap_core(core_rows)

    def _prepare_core_for_wrapping(self):
        clean_core = self._clean_core(self.core)
        core_rows = list(self._chunks(clean_core, MAX_WIDTH))
        self._pad_last_row_when_necessary(core_rows)
        return core_rows

    @staticmethod
    def _wrap_core(core_rows):
        top_and_bottom = "".join(["🧻" for _ in range(len(core_rows[0]) + 2)])
        result = top_and_bottom
        for core_row in core_rows:
            clean_core_row = "".join(core_row)
            result += f"\n🧻{clean_core_row}🧻"
        return f"{result}\n{top_and_bottom}"

    @staticmethod
    def _pad_last_row_when_necessary(core_rows: List) -> None:
        if len(core_rows) > 1 and len(core_rows[-1]) < MAX_WIDTH:
            core_rows[-1] += ["🧻" for _ in range(MAX_WIDTH - len(core_rows[-1]))]

    @staticmethod
    def _clean_core(core: str) -> List[str]:
        clean_core = get_emoji_regex().findall(core)
        if len(clean_core) < 1:
            clean_core = "🧻"
        return clean_core

    @staticmethod
    def _chunks(l: List[Any], n: int):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]
