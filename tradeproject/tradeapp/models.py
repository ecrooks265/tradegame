from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    gains = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    losses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    level = models.IntegerField(default=1)  # User level for each game
    # Additional fields as needed for tracking user performance

    def update_performance(self, trade_result):
        """Update the user's performance based on trade results."""
        # Logic to update points, gains, losses, etc.
        pass

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    skill_type = models.CharField(max_length=50, choices=[
        ('market_prediction', 'Market Prediction'),
        ('enhanced_research', 'Enhanced Research'),
        ('risk_reduction', 'Risk Reduction'),
    ])
    level = models.IntegerField(default=1)  # Skill level

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    unlocked = models.BooleanField(default=False)

    def level_up(self):
        """Logic for leveling up the skill."""
        if self.unlocked:
            self.level += 1
        pass

    def __str__(self):
        return f"{self.profile.user.username}'s {self.skill.name} (Level {self.level})"


class Trade(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='trades')
    stock_symbol = models.CharField(max_length=10)
    trade_type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)  # Whether the trade was successful

    def execute_trade(self):
        """Simulate trade execution and update profile performance."""
        # Logic for executing the trade, possibly adjusting scores
        self.profile.update_performance(self)
        pass

    def __str__(self):
        return f"Trade: {self.trade_type} {self.quantity} of {self.stock_symbol} by {self.profile.user.username}"


class Round(models.Model):
    player1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rounds_as_player1')
    player2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rounds_as_player2')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    winner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_rounds')
    market = models.ForeignKey('SimulatedMarket', on_delete=models.CASCADE)
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)

    def get_duration(self):
        """Calculate the duration of the round."""
        return (self.end_time - self.start_time).total_seconds()

    def __str__(self):
        return f"Round between {self.player1.user.username} and {self.player2.user.username}"


class SkillTree(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='skill_tree')
    current_level = models.IntegerField(default=1)

    def level_up(self):
        """Level up the player's skill tree and potentially unlock new skills."""
        self.current_level += 1
        # Logic to unlock new skills or abilities based on the new level
        pass

    def __str__(self):
        return f"{self.profile.user.username}'s Skill Tree - Level {self.current_level}"


class Leaderboard(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='leaderboard')
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def update_rank(self):
        """Logic to update the rank of the user on the leaderboard."""
        # Implement logic to calculate and update ranks based on total points
        pass

    def __str__(self):
        return f"{self.profile.user.username} - Rank {self.rank} with {self.total_points} points"


class MarketEvent(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    impact_factor = models.DecimalField(max_digits=5, decimal_places=2)
    event_type = models.CharField(max_length=50, choices=[
        ('earnings', 'Earnings'),
        ('regulation', 'Regulation'),
        ('news', 'News'),
    ])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SimulatedMarket(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    events = models.ManyToManyField(MarketEvent, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    def simulate_market(self):
        """Simulate market changes based on events and user influence."""
        # Logic to simulate market behavior
        pass

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=100)  # Name of the game
    duration = models.PositiveIntegerField()  # Duration of the game in minutes
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # User who created the game
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the game was created

    def __str__(self):
        return self.name