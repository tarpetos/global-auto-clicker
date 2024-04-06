from auto_clicker import AutoClicker, AutoClickerGUI


def main() -> None:
    clicker = AutoClicker()
    app = AutoClickerGUI(clicker)
    app.mainloop()


if __name__ == "__main__":
    main()
