from src.engine import LogisticsEngine

engine = LogisticsEngine()

# Setup Data
engine.add_location("Downtown_Central")
engine.add_location("North_Station")
engine.add_driver("Driver_Alpha", (2, 2))
engine.add_driver("Driver_Beta", (5, 5))

# Test Case 1: Valid Request
print("--- Request 1 ---")
print(engine.find_best_driver("user_123", "Downtown_Central", (0, 0)))

# Test Case 2: Security Flagging
print("\n--- Request 2 (Blacklisted) ---")
engine.blacklist_user("hacker_01")
print(engine.find_best_driver("hacker_01", "Downtown_Central", (0, 0)))