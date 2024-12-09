class ProficiencyHashTable:
    def __init__(self):
        """Initialize the hash table."""
        self.table = {}

    def get_proficiency(self, wrong_answers):
        """Return the proficiency level based on the number of wrong answers."""
        if wrong_answers <= 2:
            return "Beginner"
        elif wrong_answers <= 5:
            return "Intermediate"
        elif wrong_answers <= 8:
            return "Expert"
        else:
            return "Master"

    def add_player(self, player_name, wrong_answers):
        """Add a player to the hash table with their proficiency level."""
        proficiency = self.get_proficiency(wrong_answers)
        self.table[player_name] = proficiency

    def get_player_proficiency(self, player_name):
        """Retrieve a player's proficiency level."""
        return self.table.get(player_name, "Player not found")

    def update_proficiency(self, player_name, wrong_answers):
        """Update a player's proficiency level based on new wrong answers."""
        proficiency = self.get_proficiency(wrong_answers)
        if player_name in self.table:
            self.table[player_name] = proficiency
        else:
            print(f"Player {player_name} not found.")

    def remove_player(self, player_name):
        """Remove a player from the hash table."""
        if player_name in self.table:
            del self.table[player_name]
        else:
            print(f"Player {player_name} not found.")

    def display(self):
        """Display all players and their proficiency levels."""
        for player_name, proficiency in self.table.items():
            print(f"Player: {player_name}, Proficiency Level: {proficiency}")

# Example usage
if __name__ == "__main__":
    proficiency_table = ProficiencyHashTable()

    # Add players with their wrong answers
    proficiency_table.add_player("Player1", 1)
    proficiency_table.add_player("Player2", 4)
    proficiency_table.add_player("Player3", 7)
    proficiency_table.add_player("Player4", 10)

    # Display all players and their proficiency levels
    proficiency_table.display()

    # Retrieve proficiency of a specific player
    print(f"Proficiency of Player2: {proficiency_table.get_player_proficiency('Player2')}")

    # Update proficiency based on new wrong answers
    proficiency_table.update_proficiency("Player2", 6)
    print(f"Updated Proficiency of Player2: {proficiency_table.get_player_proficiency('Player2')}")

    # Remove a player
    proficiency_table.remove_player("Player1")
    proficiency_table.display()
