import time
import tkinter as tk
from enum import StrEnum, auto
from threading import Thread
from typing import Callable, Final

import pyautogui
from pyautogui import Point


class MouseLocationMonitor(Thread):
    def __init__(
        self,
        transfer_position_to: Callable,
        *,
        daemon: bool | None = None,
    ) -> None:
        super().__init__(target=self._check_pos, daemon=daemon)
        self.get_mouse_pos = transfer_position_to
        self.__running = True

    def _check_pos(self) -> None:
        while self.__running:
            self.get_mouse_pos(pyautogui.position())

    def exit(self) -> None:
        self.__running = False


class AutoClicker:
    def __init__(
        self,
        work_time: float | str | None = None,
        timeout_before: float = 1.0,
        clicks: int = 1,
        interval: float = 0.0,
        button: str = pyautogui.PRIMARY,
        duration: float = 0.0,
        sleep: float = 0.0,
    ) -> None:
        self.work_time = work_time
        self._mouse_monitor = None
        self._execution_time_thread = None
        self.__global_start_time = time.perf_counter()
        self.__global_execution_time = 0.0
        self._exit_thread()
        self.timeout_before = timeout_before
        self.clicks = clicks
        self.interval = interval
        self.button = button
        self.duration = duration
        self.sleep = sleep
        self._start_time = 0.0
        self._click_counter = 0
        self._speed_cps = 0.0

    def click(self, position: Point) -> None:
        pyautogui.click(
            *position,
            clicks=self.clicks,
            interval=self.interval,
            button=self.button,
            duration=self.duration,
        )
        self._click_counter += 1
        self._check_speed()
        print(
            f"Click counter: {self._click_counter * self.clicks}; "
            f"speed (clicks / second): {self._speed_cps * self.clicks:.2f}; "
            f"mouse position: ({position.x};{position.y})"
        )
        pyautogui.sleep(self.sleep) if self.sleep else None

    def _check_speed(self) -> None:
        current_time = time.perf_counter()
        self._speed_cps = 1 / ((current_time - self._start_time) / self._click_counter)

    def start(self) -> None:
        time.sleep(self.timeout_before)
        self._start_time = time.perf_counter()
        self._mouse_monitor = MouseLocationMonitor(transfer_position_to=self.click)
        self._mouse_monitor.start()

    def _exit_thread(self) -> None:
        if not self.work_time:
            return None
        self._execution_time_thread = Thread(target=self._wait_timeout, daemon=True)
        self._execution_time_thread.start()

    def _wait_timeout(self) -> None:
        while (
            current_time := (time.perf_counter() - self.__global_start_time)
            <= self.work_time
        ):
            self.__global_execution_time = current_time
        self._mouse_monitor.exit()


class Color(StrEnum):
    BLACK = auto()
    WHITE = auto()


class AutoClickerGUI(tk.Tk):
    TITLE: Final[str] = "Auto Clicker v0.1"
    MIN_SIZE: Final[list[int, int]] = 640, 480

    def __init__(self, clicker: AutoClicker) -> None:
        super().__init__()
        self._startup_configure()
        self._init_ui()
        self._place_widgets()
        self._clicker = clicker

    def _startup_configure(self) -> None:
        self.title(self.TITLE)
        self.minsize(*self.MIN_SIZE)
        self.configure(background="gray")

    def _init_ui(self) -> None:
        self.input_frame = self.black_frame(self)
        self.work_time_label = self.black_label(
            self.input_frame, text="Enter execution time for clicker:"
        )
        self.work_time_input = tk.Entry(self.input_frame)
        self.work_time_measurement_label = self.black_label(
            self.input_frame, text="Select time measurement units:"
        )
        self.work_time_menu = tk.OptionMenu(self.input_frame, tk.StringVar(), "h")
        # self.timeout_before_label = tk.Label(self.input_frame)
        self.timeout_before_input = tk.Entry(self.input_frame)
        self.clicks_input = tk.Entry(self.input_frame)
        self.interval_input = tk.Entry(self.input_frame)
        self.button_menu = tk.OptionMenu(
            self.input_frame, tk.StringVar(), pyautogui.PRIMARY
        )
        self.duration_input = tk.Entry(self.input_frame)

        self.button_frame = self.black_frame(self)
        self.start_clicker_button = tk.Button(self.button_frame, text="Start")
        self.stop_clicker_button = tk.Button(self.button_frame, text="Stop")

    def _place_widgets(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=8)
        self.grid_rowconfigure(1, weight=1)

        self._build_grid_frame(
            frame=self.input_frame,
            frame_placement=(0, 0),
            widgets=[
                self.work_time_label,
                self.work_time_input,
                self.work_time_measurement_label,
                self.work_time_menu,
                self.timeout_before_input,
                self.clicks_input,
                self.interval_input,
                self.button_menu,
                self.duration_input,
            ],
            row_size=4,
        )

        self._build_grid_frame(
            frame=self.button_frame,
            frame_placement=(1, 0),
            widgets=[
                self.start_clicker_button,
                self.stop_clicker_button,
                self.timeout_before_input,
                self.clicks_input,
                self.interval_input,
                self.button_menu,
                self.duration_input,
            ],
        )

    @staticmethod
    def _build_grid_frame(
        frame: tk.Frame,
        frame_placement: tuple[int, int],
        widgets: list[tk.Widget],
        *,
        row_size: int = 2,
    ) -> None:
        frame.grid_configure(
            row=frame_placement[0], column=frame_placement[1], sticky=tk.NSEW
        )

        for index, widget in enumerate(widgets):
            row_number = index // row_size
            col_number = index % row_size
            padx = (
                (5 if col_number == 0 or index % row_size == 0 else (0, 5))
                if col_number == 0 or col_number == row_size - 1
                else (0, 5)
            )
            widget.grid_configure(
                row=row_number,
                column=col_number,
                columnspan=(
                    row_size
                    if len(widgets) % 2 != 0 and index == len(widgets) - 1
                    else 1
                ),
                sticky=tk.NSEW,
                padx=padx,
                pady=5,
            )
            frame.grid_columnconfigure(col_number, weight=1)

    @staticmethod
    def black_frame(*args, **kwargs) -> tk.Frame:
        return tk.Frame(*args, **kwargs, background=Color.BLACK)

    @staticmethod
    def black_label(*args, **kwargs) -> tk.Label:
        return tk.Label(*args, **kwargs, background=Color.BLACK, foreground=Color.WHITE, height=2)
