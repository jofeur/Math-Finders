class GameLevel:
    def __init__(self, level_number, description, difficulty):
        """Initialize a GameLevel node with level number, description, and difficulty."""
        self.level_number = level_number
        self.description = description
        self.difficulty = difficulty
        self.children = []  # Child levels, to be used for next levels in the game tree

    def add_child(self, child_level):
        """Add a child level (next level) to the current level."""
        self.children.append(child_level)

    def __repr__(self):
        return f"Level {self.level_number}: {self.description} (Difficulty: {self.difficulty})"


class GameTree:
    def __init__(self):
        """Initialize the game tree with level 1 as the root."""
        self.root = GameLevel(level_number=1, description="Math Finders", difficulty="Easy")
        self._build_game_tree(self.root)

    def _build_game_tree(self, node):
        """Build the entire tree structure with 5 levels."""
        level_data = [
            ("Level 1", "Easy"),
            ("Level 2", "Medium"),
            ("Level 3", "Hard"),
            ("Level 4", "Very Hard"),
            ("Level 5", "Expert")
        ]

        for level_number, (description, difficulty) in enumerate(level_data, 2):
            new_level = GameLevel(level_number, description, difficulty)
            node.add_child(new_level)
            node = new_level  # Move to the next level to add the next child

    def traverse_levels(self):
        """Traverse the tree from level 1 to level 5 and print out details."""
        level = self.root
        while level:
            print(level)
            if level.children:
                level = level.children[0]  # Move to the next level
            else:
                break


# Example usage
if __name__ == "__main__":
    game_tree = GameTree()

    # Traverse and display all levels from 1 to 5
    game_tree.traverse_levels()
