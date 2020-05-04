from django.apps import AppConfig


class ExpenseTrackerConfig(AppConfig):
    name = 'expense_tracker'
    def ready(self):
        import expense_tracker.signals
