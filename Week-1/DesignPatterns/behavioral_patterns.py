"""Week-1 behavioral pattern examples for beginner-friendly Python training."""

# =====================================================================
# Observer Pattern
# =====================================================================
# Notify many objects when one object changes state.


class Subscriber:
    def update(self, news: str) -> None:
        print(f"Subscriber received: {news}")


class NewsAgency:
    def __init__(self) -> None:
        self.subscribers = []
        self.news = ""

    def subscribe(self, subscriber: Subscriber) -> None:
        self.subscribers.append(subscriber)

    def set_news(self, news: str) -> None:
        self.news = news
        self.notify()

    def notify(self) -> None:
        for subscriber in self.subscribers:
            subscriber.update(self.news)


# =====================================================================
# Strategy Pattern
# =====================================================================
# Swap algorithms or behaviors at runtime.


class PaymentStrategy:
    def pay(self, amount: float) -> None:
        raise NotImplementedError


class CardStrategy(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paid ${amount:.2f} by card")


class UpiStrategy(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paid ${amount:.2f} by UPI")


class PaymentContext:
    def __init__(self, strategy: PaymentStrategy) -> None:
        self.strategy = strategy

    def execute_payment(self, amount: float) -> None:
        self.strategy.pay(amount)


# =====================================================================
# Command Pattern
# =====================================================================
# Turn a request into a reusable object.


class Light:
    def on(self) -> None:
        print("Light is ON")

    def off(self) -> None:
        print("Light is OFF")


class LightOnCommand:
    def __init__(self, light: Light) -> None:
        self.light = light

    def execute(self) -> None:
        self.light.on()


class LightOffCommand:
    def __init__(self, light: Light) -> None:
        self.light = light

    def execute(self) -> None:
        self.light.off()


class RemoteControl:
    def __init__(self) -> None:
        self.command = None

    def set_command(self, command) -> None:
        self.command = command

    def press_button(self) -> None:
        if self.command is not None:
            self.command.execute()


def demo_observer() -> None:
    print("\nObserver demo")
    agency = NewsAgency()
    agency.subscribe(Subscriber())
    agency.subscribe(Subscriber())
    agency.set_news("Python training starts today")


def demo_strategy() -> None:
    print("\nStrategy demo")
    for strategy in [CardStrategy(), UpiStrategy()]:
        PaymentContext(strategy).execute_payment(120)


def demo_command() -> None:
    print("\nCommand demo")
    light = Light()
    remote = RemoteControl()
    remote.set_command(LightOnCommand(light))
    remote.press_button()
    remote.set_command(LightOffCommand(light))
    remote.press_button()


if __name__ == "__main__":
    demo_observer()
    demo_strategy()
    demo_command()
