from __future__ import annotations
from pathlib import Path

if False:
    from logic.image_buffer import ImageBuffer


class QueueManager:
    def __init__(self, image_buffer: "ImageBuffer") -> None:
        self._queue: list[Path] = []
        self._last_curant: Path | None = None
        self._image_buffer = image_buffer

    def update(self) -> None:
        if not self._queue:
            self._last_curant = None
            return
        head = self._queue[0]
        if self._last_curant != head:
            self._image_buffer.load_image(head)
            self._last_curant = head

    def set_paths(self, paths: list[Path | str]) -> None:
        seen: set[Path] = set()
        unique: list[Path] = []
        for p in paths:
            q = Path(p)
            if q not in seen:
                seen.add(q)
                unique.append(q)
        self._queue = unique
        self.update()

    def get_all(self) -> list[Path]:
        return list(self._queue)

    def set_curant(self, path: Path | str) -> None:
        p = Path(path)
        try:
            self._queue.remove(p)
        except ValueError:
            pass
        self._queue.insert(0, p)
        self.update()

    def get_curant(self) -> Path | None:
        return self._queue[0] if self._queue else None

    def advance(self) -> None:
        if self._queue:
            self._queue.pop(0)
            self.update()

    def add(self, path: Path | str) -> None:
        p = Path(path)
        if p not in self._queue:
            self._queue.append(p)
            self.update()

    def remove(self, path: Path | str) -> None:
        p = Path(path)
        try:
            self._queue.remove(p)
            self.update()
        except ValueError:
            pass
