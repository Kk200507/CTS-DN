"""Week-1 creational pattern examples for beginner-friendly Python training."""

# =====================================================================
# Singleton Pattern
# =====================================================================
# Ensure a class has only one instance.


class AppConfig:
    _instance = None

    def __new__(cls) -> "AppConfig":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.app_name = "Training App"
        return cls._instance


# =====================================================================
# Factory Pattern
# =====================================================================
# Create objects without exposing the creation logic.


class Notification:
    def send(self, message: str) -> None:
        raise NotImplementedError


class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Email sent: {message}")


class SmsNotification(Notification):
    def send(self, message: str) -> None:
        print(f"SMS sent: {message}")


class NotificationFactory:
    @staticmethod
    def create(notification_type: str) -> Notification:
        if notification_type == "email":
            return EmailNotification()
        if notification_type == "sms":
            return SmsNotification()
        raise ValueError("Unsupported notification type")


# =====================================================================
# Builder Pattern
# =====================================================================
# Build a complex object step by step.


class Burger:
    def __init__(self) -> None:
        self.bun = ""
        self.patty = ""
        self.sauce = ""
        self.toppings = []

    def __str__(self) -> str:
        return (
            f"Burger(bun={self.bun}, patty={self.patty}, "
            f"sauce={self.sauce}, toppings={self.toppings})"
        )


class BurgerBuilder:
    def __init__(self) -> None:
        self.burger = Burger()

    def add_bun(self, bun: str) -> "BurgerBuilder":
        self.burger.bun = bun
        return self

    def add_patty(self, patty: str) -> "BurgerBuilder":
        self.burger.patty = patty
        return self

    def add_sauce(self, sauce: str) -> "BurgerBuilder":
        self.burger.sauce = sauce
        return self

    def add_topping(self, topping: str) -> "BurgerBuilder":
        self.burger.toppings.append(topping)
        return self

    def build(self) -> Burger:
        return self.burger


def demo_singleton() -> None:
    print("\nSingleton demo")
    config1 = AppConfig()
    config2 = AppConfig()
    print(config1.app_name)
    print(f"Same instance: {config1 is config2}")


def demo_factory() -> None:
    print("\nFactory demo")
    notification = NotificationFactory.create("email")
    notification.send("Your order has been placed")


def demo_builder() -> None:
    print("\nBuilder demo")
    burger = (
        BurgerBuilder()
        .add_bun("Sesame")
        .add_patty("Veggie")
        .add_sauce("Mayo")
        .add_topping("Lettuce")
        .add_topping("Tomato")
        .build()
    )
    print(burger)


if __name__ == "__main__":
    demo_singleton()
    demo_factory()
    demo_builder()
